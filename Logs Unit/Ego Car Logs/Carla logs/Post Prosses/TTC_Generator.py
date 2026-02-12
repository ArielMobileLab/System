# -*- coding: utf-8 -*-
import json
import math
import os
import re
from collections import defaultdict

# =========================
# Files input output
# =========================
OBJECTS_FILE = r"C:\Users\ALEX\Desktop\Work\TTC\last version\Objects_Simulation_Avatar_MapB_2025-03-17_19-18-22.json"
EGO_FILE     = r"C:\Users\ALEX\Desktop\Work\TTC\last version\EgoCar_Simulation_Avatar_MapB_2025-03-17_19-18-22.json"
OUTPUT_FILE  = r"C:\Users\ALEX\Desktop\Work\TTC\frame_log_full.json"

MAX_DISTANCE_TO_CALC_TTC = 200.0

# =========================
# Extract name from map
# =========================
def extract_map_name(path):
    fname = os.path.basename(path)
    m = re.search(r"_Map([^_]+)_", fname)
    return m.group(1) if m else "Unknown"

map_name = extract_map_name(OBJECTS_FILE)

# =========================
# Log loading
# =========================
with open(OBJECTS_FILE, "r", encoding="utf-8") as f:
    objects_log = json.load(f)

with open(EGO_FILE, "r", encoding="utf-8") as f:
    ego_log = json.load(f)

# =========================
# Insert Ego log
# =========================
ego_samples = []

for e in ego_log["Logs"]:
    if e.get("Type") != "GPS":
        continue
    if "SimulationPosition" not in e:
        continue

    ego_samples.append({
        "t": float(e["SimulationTime"]),
        "x": float(e["SimulationPosition"]["x"]),
        "y": float(e["SimulationPosition"]["y"]),
        "lat": float(e.get("Latitude", 0.0)),
        "lon": float(e.get("Longitude", 0.0)),
        "speed": float(e.get("Speed", 0.0)) / 3.6,
        "yaw": float(e["Orientation"]["y"])
    })

ego_samples.sort(key=lambda s: s["t"])

# =========================
# Insert all Objects
# =========================
all_objects = defaultdict(list)

for e in objects_log["Logs"]:

    obj_type = e.get("Type")
    name = e.get("Name")

    if not name:
        continue

    # All besides Traffic lights
    if obj_type == "GPS" and "SimulationPosition" in e:
        all_objects[name].append({
            "type": "dynamic",
            "t": float(e["SimulationTime"]),
            "x": float(e["SimulationPosition"]["x"]),
            "y": float(e["SimulationPosition"]["y"]),
            "lat": float(e.get("Latitude", 0.0)),
            "lon": float(e.get("Longitude", 0.0))
        })

    # Traffic lights
    elif obj_type == "TrafficLight" and "Position" in e:
        all_objects[name].append({
            "type": "static",
            "t": float(e["SimulationTime"]),
            "x": float(e["Position"]["x"]),
            "y": float(e["Position"]["y"]),
            "lat": float(e.get("Latitude", 0.0)),
            "lon": float(e.get("Longitude", 0.0))
        })

for name in all_objects:
    all_objects[name].sort(key=lambda s: s["t"])

# =========================
# TTC Vectors
# =========================
def compute_ttc_dynamic(s, min_dist=2.0, eps=1e-8):
    
    # position vector from ego to object
    rx = s["obj_x"] - s["ego_x"]
    ry = s["obj_y"] - s["ego_y"]

    # Ego speed
    yaw = math.radians(s["ego_yaw"])
    ego_vx = s["ego_speed"] * math.cos(yaw)
    ego_vy = s["ego_speed"] * math.sin(yaw)

    # Relative speed
    vrel_x = s["obj_vx"] - ego_vx
    vrel_y = s["obj_vy"] - ego_vy

    # | r + v_rel * t |^2 = min_dist^2 - Calculating TTC assuming constant speeds # משוואה ריבועית

    a = vrel_x*vrel_x + vrel_y*vrel_y # relative speed squared
    b = 2 * (rx * vrel_x + ry * vrel_y) # if disntace closing or get bigger
    c = rx*rx + ry*ry - min_dist*min_dist # initial distance safety radius squared

    # Already inside safety radius
    if c <= 0:
        return 0.0

    # no relative speed (no TTC)
    if abs(a) < eps:
        return float("inf")

    disc = b*b - 4*a*c
    if disc < 0:
        return float("inf")

    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)

    # Keep only future times (t > 0)
    t_candidates = [t for t in (t1, t2) if t > eps]

    # Return earliest future collision time
    return min(t_candidates) if t_candidates else float("inf")

# =========================
# TTC Static obj (traffic lights)
# =========================
def compute_ttc_static(ego, obj_x, obj_y):

    # position vector from ego to object
    rx = obj_x - ego["x"]
    ry = obj_y - ego["y"]

    #distance between ego and static object
    distance = math.hypot(rx, ry)

    # If already extremely close ? treat as immediate contact
    if distance < 1e-6:
        return 0.0

    # Ego speed X Y
    yaw = math.radians(ego["yaw"])
    ego_vx = ego["speed"] * math.cos(yaw)
    ego_vy = ego["speed"] * math.sin(yaw)

    #Project ego velocity onto line-of-sight direction
    closing_speed = (rx * ego_vx + ry * ego_vy) / distance

    #if closing_speed <= 0 ? ego is moving away or perpendicular
    if closing_speed <= 0:
        return float("inf")

    #Classical TTC = distance / radial closing speed
    return distance / closing_speed

# =========================
# יצירת לוג מלא
# =========================
all_frames = []

for name, samples in all_objects.items():

    for i in range(1, len(samples)):

        prev = samples[i-1]
        curr = samples[i]

        for ego in ego_samples:

            # Check the closest frame for both ego and obj
            if abs(curr["t"] - ego["t"]) > 0.05:
                continue

            distance = math.hypot(curr["x"] - ego["x"],
                                  curr["y"] - ego["y"])

            if distance > MAX_DISTANCE_TO_CALC_TTC:
                continue

            # term for relevant Traffic lights from events
            if curr["type"] == "static":
                ttc = compute_ttc_static(ego, curr["x"], curr["y"])
                obj_speed = 0.0
            else:
                dt = curr["t"] - prev["t"]
                if dt <= 0:
                    continue

                obj_vx = (curr["x"] - prev["x"]) / dt
                obj_vy = (curr["y"] - prev["y"]) / dt
                obj_speed = math.hypot(obj_vx, obj_vy)

                # skip static walkers
                if obj_speed < 0.2:
                  continue

                s = {
                    "ego_x": ego["x"],
                    "ego_y": ego["y"],
                    "ego_speed": ego["speed"],
                    "ego_yaw": ego["yaw"],
                    "obj_x": curr["x"],
                    "obj_y": curr["y"],
                    "obj_vx": obj_vx,
                    "obj_vy": obj_vy
                }

                ttc = compute_ttc_dynamic(s)

            frame_log = {
                "MAP": map_name,
                "Condition": "Close",
                "ID": name,
                "SimulationTime": curr["t"],
                "EGO": {
                    "Speed": ego["speed"],
                    "X": ego["x"],
                    "Y": ego["y"],
                    "Latitude": ego["lat"],
                    "Longitude": ego["lon"],
                    "Yaw": ego["yaw"]
                },
                "OBJ": {
                    "Speed": obj_speed,
                    "X": curr["x"],
                    "Y": curr["y"],
                    "Latitude": curr["lat"],
                    "Longitude": curr["lon"],
                    "Yaw": None
                },
                "Distance": distance,
                "TTC": None if math.isinf(ttc) else ttc
            }

            all_frames.append(frame_log)

# =========================
# שמירה
# =========================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"Logs": all_frames}, f, indent=2)

print("Full TTC log exported:", OUTPUT_FILE)
