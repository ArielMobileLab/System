import subprocess
import os
import pandas as pd
from pathlib import Path



# =========================
# Find video path from CSV
# =========================



def find_kinematic_path(csv_path, obj_id, scenario, condition, triggered_by):
    df = pd.read_csv(csv_path)

    # ניקוי עמודות
    df["Id"] = df["Id"].astype(str).str.strip()
    df["Scenario"] = df["Scenario"].astype(str).str.strip()
    df["Condition"] = df["Condition"].astype(str).str.strip()
    df["triggered_by"] = df["triggered_by"].astype(str).str.strip()

    # סינון שורה מתאימה
    filtered = df[
        (df["Id"] == str(obj_id).strip()) &
        (df["Scenario"].str.lower() == scenario.lower().strip()) &
        (df["Condition"].str.lower() == condition.lower().strip()) &
        (df["triggered_by"].str.lower() == triggered_by.lower().strip())
    ]

    if filtered.empty:
        raise ValueError("No matching row found in CSV")

    original_path = str(filtered.iloc[0]["PhysiologicalFile"]).strip()
    folder_path = Path(original_path)

    # אם הגיע קובץ → קח את התיקייה שלו
    if folder_path.suffix:
        folder_path = folder_path.parent

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    # חיפוש mp4 בתוך התיקייה בלבד (לא recursive)
    mp4_files = list(folder_path.glob("*.mp4"))

    if not mp4_files:
        raise FileNotFoundError(f"No MP4 file found in: {folder_path}")

    # מחזיר את הקובץ הראשון
    return str(mp4_files[0])


# =========================
# Cut video + extract audio
# =========================
def cut_video_and_audio(input_path, start_time, end_time):

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Video not found: {input_path}")

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.dirname(input_path)

    output_mp4 = os.path.join(output_dir, f"{base_name}_cut.mp4")
    output_mp3 = os.path.join(output_dir, f"{base_name}_cut.mp3")

    cut_video_cmd = [
    "ffmpeg",
    "-y",
    "-ss", str(start_time),
    "-to", str(end_time),
    "-i", input_path,
    "-c", "copy",
    output_mp4
]

    subprocess.run(cut_video_cmd, check=True)

    extract_audio_cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-to", str(end_time),
        "-i", input_path,
        "-vn",
        "-acodec", "mp3",
        output_mp3
    ]

    subprocess.run(extract_audio_cmd, check=True)

    print("MP4 saved to:", output_mp4)
    print("MP3 saved to:", output_mp3)


# =========================
# Usage
# =========================

#calc_simulator_and_corresponding_physiological_files flie path:"
CSV_FILE = r"G:\My Drive\Ariel Uni\Readme\calc_simulator_and_corresponding_physiological_files.csv"

# Tersms for the mp4 file:
ID = "C4_129899"
SCENARIO = "Accompanied"
CONDITION = "Avatar"
TRIGGERED_BY = "Egocar"

START_TIME = "00:01:10"
END_TIME   = "00:01:40"

VIDEO_FILE = find_kinematic_path(
    CSV_FILE,
    ID,
    SCENARIO,
    CONDITION,
    TRIGGERED_BY
)

print("Found video path:")
print(VIDEO_FILE)

#cut_video_and_audio(VIDEO_FILE, START_TIME, END_TIME)