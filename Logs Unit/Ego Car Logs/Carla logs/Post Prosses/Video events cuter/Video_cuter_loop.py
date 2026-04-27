import subprocess
import os
import pandas as pd
import re
from pathlib import Path


# =========================
# SETTINGS
# =========================
SYNCED_LOG_FILE = r"C:\Users\LAB-OREN3\Desktop\Voice\synced_logs\c:\Users\LAB-OREN3\Desktop\Voice\calc_events_with_transcription_Accompanied_post_scy.csv"
CALC_CSV_FILE = r"C:\Users\LAB-OREN3\Desktop\Voice\calc_simulator_and_corresponding_physiological_files.csv"

OUTPUT_DIR = r"C:\Users\LAB-OREN3\Desktop\Voice\cut_videos_by_synctime"

TIME_COLUMN = "SyncTime_sec"


# =========================
# Find video path from calc CSV - fallback only
# =========================
def find_kinematic_path(csv_path, obj_id, scenario, condition, triggered_by):
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    df["Id"] = df["Id"].astype(str).str.strip()
    df["Scenario"] = df["Scenario"].astype(str).str.strip()
    df["Condition"] = df["Condition"].astype(str).str.strip()
    df["triggered_by"] = df["triggered_by"].astype(str).str.strip()

    filtered = df[
        (df["Id"] == str(obj_id).strip()) &
        (df["Scenario"].str.lower() == str(scenario).lower().strip()) &
        (df["Condition"].str.lower() == str(condition).lower().strip()) &
        (df["triggered_by"].str.lower() == str(triggered_by).lower().strip())
    ]

    if filtered.empty:
        raise ValueError("No matching row found in calc CSV")

    original_path = str(filtered.iloc[0]["PhysiologicalFile"]).strip()

    if original_path[:2].lower() == "h:":
        original_path = "G:" + original_path[2:]

    folder_path = Path(original_path)

    if folder_path.suffix:
        folder_path = folder_path.parent

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    mp4_files = sorted(folder_path.glob("*.mp4"))

    if not mp4_files:
        raise FileNotFoundError(f"No MP4 file found in: {folder_path}")

    return str(mp4_files[0])


# =========================
# Cut video by SyncTime_sec
# =========================
def cut_video_only(input_path, start_time, end_time, suffix=""):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Video not found: {input_path}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    safe_suffix = re.sub(r'[\\/:*?"<>| ]+', "_", str(suffix)).strip("_")

    output_mp4 = os.path.join(
        OUTPUT_DIR,
        f"{base_name}_{safe_suffix}_cut.mp4"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ss", str(start_time),
        "-to", str(end_time),

        # יותר מדויק מ-c copy לזמנים עם עשיריות שנייה
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",

        output_mp4
    ]

    subprocess.run(cmd, check=True)

    print("Saved:", output_mp4)


# =========================
# Extract valid sections using SyncTime_sec
# =========================
def extract_sections(df):
    df = df.copy()

    df["Event_Name_clean"] = (
        df["Event_Name"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    sections = {}

    patterns = [
        r"^start (traffic light \d+)$",
        r"^end (traffic light \d+)$",

        r"^start section (walker\d+)$",
        r"^end section (walker\d+)$",

        r"^start (overtake)$",
        r"^end (overtake)$",

        r"^egocar start (gap acceptance)$",
        r"^egocar end (gap acceptance)$",
    ]

    for _, row in df.iterrows():
        name = row["Event_Name_clean"]

        for pattern in patterns:
            match = re.match(pattern, name)

            if match:
                section = match.group(1)

                if "start" in name:
                    event_type = "start"
                elif "end" in name:
                    event_type = "end"
                else:
                    continue

                if section not in sections:
                    sections[section] = {"start": None, "end": None}

                sections[section][event_type] = row[TIME_COLUMN]

    return sections


# =========================
# Get Triggered_By column name safely
# =========================
def get_triggered_by_column(df):
    if "Triggered_By" in df.columns:
        return "Triggered_By"
    if "triggered_by" in df.columns:
        return "triggered_by"
    raise KeyError("No Triggered_By / triggered_by column")


# =========================
# MAIN PROCESS
# =========================
def process_all_events(synced_log_path, calc_csv_path=None):
    df = pd.read_csv(synced_log_path, encoding="utf-8-sig")

    required_cols = [
        "Id",
        "Scenario",
        "Condition",
        "Event_Name",
        TIME_COLUMN
    ]

    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column in all_synced_logs.csv: {col}")

    df["Id"] = df["Id"].astype(str).str.strip()
    df["Scenario"] = df["Scenario"].astype(str).str.strip()
    df["Condition"] = df["Condition"].astype(str).str.strip()
    df["Event_Name"] = df["Event_Name"].astype(str).str.strip()
    df[TIME_COLUMN] = pd.to_numeric(df[TIME_COLUMN], errors="coerce")

    trig_col = get_triggered_by_column(df)
    df[trig_col] = df[trig_col].astype(str).str.strip()

    # אם all_synced_logs.csv כולל VideoPath, נשתמש בו ישירות
    if "VideoPath" in df.columns:
        df["VideoPath"] = df["VideoPath"].astype(str).str.strip()
        group_cols = ["Id", "Scenario", "Condition", trig_col, "VideoPath"]
    else:
        group_cols = ["Id", "Scenario", "Condition", trig_col]

    for run_key, sub in df.groupby(group_cols, sort=False):

        if "VideoPath" in df.columns:
            obj_id, scenario, condition, triggered_by, video_file = run_key
        else:
            obj_id, scenario, condition, triggered_by = run_key

            if calc_csv_path is None:
                raise ValueError("VideoPath missing, and calc_csv_path was not provided")

            video_file = find_kinematic_path(
                calc_csv_path,
                obj_id,
                scenario,
                condition,
                triggered_by
            )

        print("\n" + "=" * 70)
        print("Processing:")
        print("ID:", obj_id)
        print("Scenario:", scenario)
        print("Condition:", condition)
        print("Triggered by:", triggered_by)
        print("Video:", video_file)

        sections = extract_sections(sub)

        if not sections:
            print("No matching event sections found")
            continue

        for section_name, times in sections.items():
            start_time = times["start"]
            end_time = times["end"]

            print(f"\n--- {section_name} ---")

            if start_time is None or end_time is None:
                print("Skipped: missing start/end")
                continue

            if pd.isna(start_time) or pd.isna(end_time):
                print("Skipped: invalid SyncTime_sec")
                continue

            if end_time <= start_time:
                print("Skipped: bad range")
                continue

            try:
                print(f"Cutting by {TIME_COLUMN}: {start_time} → {end_time}")

                suffix = f"{obj_id}_{scenario}_{condition}_{triggered_by}_{section_name}"

                cut_video_only(
                    input_path=video_file,
                    start_time=start_time,
                    end_time=end_time,
                    suffix=suffix
                )

            except Exception as e:
                print("Error:", e)


# =========================
# Usage
# =========================
process_all_events(
    synced_log_path=SYNCED_LOG_FILE,
    calc_csv_path=CALC_CSV_FILE
)