import pandas as pd
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta


def get_triggered_by_column(df):
    if "Triggered_By" in df.columns:
        return "Triggered_By"
    if "triggered_by" in df.columns:
        return "triggered_by"
    raise KeyError("No Triggered_By / triggered_by column found")


def get_log_start_end_from_df(df_run):
    reason = df_run["Reason"].astype(str).str.strip()

    start_rows = df_run.loc[reason == "Start", "WorldTime"].dropna()
    end_rows = df_run.loc[reason.isin(["EndPoint", "End"]), "WorldTime"].dropna()

    if start_rows.empty:
        raise ValueError("No Start row found")

    if end_rows.empty:
        raise ValueError("No EndPoint / End row found")

    return start_rows.iloc[0], end_rows.iloc[-1]


def find_video_path(calc_csv_path, obj_id, scenario, condition, triggered_by):
    df = pd.read_csv(calc_csv_path, encoding="utf-8-sig")

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


def get_video_duration_seconds(video_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def get_video_start_end(video_path):
    video_path = Path(video_path)

    match = re.search(
        r"(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})-(\d{2})",
        video_path.name
    )

    if not match:
        raise ValueError(f"Could not find date/time in video filename: {video_path.name}")

    video_start = datetime.strptime(
        f"{match.group(1)} {match.group(2)}:{match.group(3)}:{match.group(4)}",
        "%Y-%m-%d %H:%M:%S"
    )

    video_duration = get_video_duration_seconds(video_path)
    video_end = video_start + timedelta(seconds=video_duration)

    return video_start, video_end, video_duration


def log_worldtime_to_datetime(worldtime, base_dt):
    if pd.isna(worldtime):
        return pd.NaT

    worldtime = str(worldtime).strip()

    if worldtime == "" or worldtime.lower() == "nan":
        return pd.NaT

    parts = worldtime.split(":")

    try:
        if len(parts) == 3:
            hour = int(parts[0])
            minute = int(parts[1])
            second = float(parts[2])

        elif len(parts) == 2:
            hour = base_dt.hour
            minute = int(parts[0])
            second = float(parts[1])

        else:
            return pd.NaT

        sec_int = int(second)
        micro = int(round((second - sec_int) * 1_000_000))

        if micro == 1_000_000:
            sec_int += 1
            micro = 0

        return base_dt.replace(
            hour=hour,
            minute=minute,
            second=sec_int,
            microsecond=micro
        )

    except Exception:
        return pd.NaT


def sync_one_run(df_run, video_path):
    log_start, log_end = get_log_start_end_from_df(df_run)

    video_start, video_end, video_duration = get_video_start_end(video_path)

    log_start_dt = log_worldtime_to_datetime(log_start, video_start)
    log_end_dt = log_worldtime_to_datetime(log_end, video_start)

    if pd.isna(log_start_dt) or pd.isna(log_end_dt):
        raise ValueError("Invalid log start/end time")

    while log_end_dt <= log_start_dt:
        log_end_dt += timedelta(hours=1)

    sync_start = max(log_start_dt, video_start)
    sync_end = min(log_end_dt, video_end)

    if sync_end <= sync_start:
        raise ValueError("No overlap between LOG and VIDEO")

    df_run = df_run.copy()

    def convert_time(x):
        dt = log_worldtime_to_datetime(x, video_start)

        if pd.isna(dt):
            return pd.NaT

        while dt < log_start_dt:
            dt += timedelta(hours=1)

        return dt

    df_run["WorldTime_dt"] = df_run["WorldTime"].apply(convert_time)
    df_run = df_run.dropna(subset=["WorldTime_dt"]).copy()

    synced = df_run[
        (df_run["WorldTime_dt"] >= sync_start) &
        (df_run["WorldTime_dt"] <= sync_end)
    ].copy()

    synced["SyncTime_sec"] = (
        synced["WorldTime_dt"] - sync_start
    ).dt.total_seconds()

    synced["VideoOriginalTime_sec"] = (
        synced["WorldTime_dt"] - video_start
    ).dt.total_seconds()

    synced["VideoPath"] = str(video_path)
    synced["VideoFile"] = Path(video_path).name

    synced["LogStart_dt"] = log_start_dt
    synced["LogEnd_dt"] = log_end_dt
    synced["VideoStart_dt"] = video_start
    synced["VideoEnd_dt"] = video_end
    synced["SyncStart_dt"] = sync_start
    synced["SyncEnd_dt"] = sync_end
    synced["SyncDuration_sec"] = (sync_end - sync_start).total_seconds()

    return synced


def make_safe_name(text):
    text = str(text)
    text = re.sub(r'[\\/:*?"<>| ]+', "_", text)
    return text.strip("_")


def process_all_runs(test_csv_path, calc_csv_path, output_folder):
    df = pd.read_csv(test_csv_path, encoding="utf-8-sig")

    trig_col = get_triggered_by_column(df)

    group_cols = ["Id", "Scenario", "Condition", trig_col]

    for col in group_cols:
        df[col] = df[col].astype(str).str.strip()

    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_synced = []
    summary = []

    for run_key, df_run in df.groupby(group_cols, sort=False):
        obj_id, scenario, condition, triggered_by = run_key

        print("\n" + "=" * 70)
        print("Processing:", obj_id, scenario, condition, triggered_by)

        try:
            video_path = find_video_path(
                calc_csv_path,
                obj_id,
                scenario,
                condition,
                triggered_by
            )

            synced_log = sync_one_run(df_run, video_path)

            safe_name = make_safe_name(
                f"{obj_id}_{scenario}_{condition}_{triggered_by}"
            )

            output_csv = output_dir / f"{safe_name}_synced_log.csv"
            synced_log.to_csv(output_csv, index=False, encoding="utf-8-sig")

            all_synced.append(synced_log)

            summary.append({
                "Id": obj_id,
                "Scenario": scenario,
                "Condition": condition,
                "triggered_by": triggered_by,
                "Status": "OK",
                "VideoFile": Path(video_path).name,
                "SyncedRows": len(synced_log),
                "SyncDuration_sec": synced_log["SyncDuration_sec"].iloc[0],
                "OutputCSV": str(output_csv)
            })

            print("Saved:", output_csv)

        except Exception as e:
            print("FAILED:", e)

            summary.append({
                "Id": obj_id,
                "Scenario": scenario,
                "Condition": condition,
                "triggered_by": triggered_by,
                "Status": "FAILED",
                "Error": str(e)
            })

    summary_df = pd.DataFrame(summary)
    summary_path = output_dir / "sync_summary.csv"
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")

    if all_synced:
        all_synced_df = pd.concat(all_synced, ignore_index=True)
        combined_path = output_dir / "all_synced_logs.csv"
        all_synced_df.to_csv(combined_path, index=False, encoding="utf-8-sig")
        print("\nCombined file saved:", combined_path)
    else:
        all_synced_df = pd.DataFrame()
        print("\nNo synced logs were created")

    print("Summary saved:", summary_path)

    return all_synced_df, summary_df


TEST_CSV_FILE = r"C:\Users\LAB-OREN3\Desktop\Voice\Test.csv"
CALC_CSV_FILE = r"C:\Users\LAB-OREN3\Desktop\Voice\calc_simulator_and_corresponding_physiological_files.csv"
OUTPUT_FOLDER = r"C:\Users\LAB-OREN3\Desktop\Voice\synced_logs"

all_synced_df, summary_df = process_all_runs(
    TEST_CSV_FILE,
    CALC_CSV_FILE,
    OUTPUT_FOLDER
)