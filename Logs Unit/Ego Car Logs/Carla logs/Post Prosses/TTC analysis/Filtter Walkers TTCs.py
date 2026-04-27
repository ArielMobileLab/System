import pandas as pd
from pathlib import Path

# =========================
# מציאת כל קבצי EGO_OBJFile
# =========================
def get_ego_rows(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    df["Scenario"] = df["Scenario"].astype(str).str.strip()
    df["triggered_by"] = df["triggered_by"].astype(str).str.strip()
    df["EGO_OBJFile"] = df["EGO_OBJFile"].astype(str).str.strip()
    df["Map"] = df["Map"].astype(str).str.strip()  # הוספת עמודת Map

    filtered = df[
        (df["Scenario"].str.lower() == "accompanied") &
        (df["triggered_by"].str.lower() == "egocar")
    ]

    rows_data = []

    for _, row in filtered.iterrows():
        path_str = row["EGO_OBJFile"]

        if not path_str or path_str.lower() == "nan":
            continue

        # תיקון H ל-G
        if path_str[:2].lower() == "h:":
            path_str = "G:" + path_str[2:]

        path_obj = Path(path_str)

        if path_obj.exists():
            rows_data.append({
                "Id": row["Id"],
                "Scenario": row["Scenario"],
                "Condition": row["Condition"],
                "Map": row["Map"],           # שמירה של Map
                "EGO_OBJFile": str(path_obj)
            })
        else:
            print(f"Not found: {path_obj}")

    return rows_data


# =========================
# מציאת מינימום TTC ל-walkers
# =========================
def find_min_ttc_for_walkers(csv_path):
    df = pd.read_csv(csv_path)
    df["ID"] = df["ID"].astype(str).str.strip()

    walkers_df = df[df["ID"].str.lower().str.startswith("walker")].copy()
    
    if walkers_df.empty:
        return None, None

    # המרה למספרים
    walkers_df["TTC"] = pd.to_numeric(walkers_df["TTC"], errors='coerce')

    # סינון ערכים לא חוקיים
    walkers_df = walkers_df.dropna(subset=["TTC"])

    if walkers_df.empty:
        return None, None

    min_ttc_row = walkers_df.loc[walkers_df["TTC"].idxmin()]

    return min_ttc_row["ID"], min_ttc_row["TTC"]


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    master_csv = r"C:\Users\LAB-OREN3\Desktop\TTCMIN\calc_simulator_and_corresponding_physiological_files.csv"
    output_csv = r"C:\Users\LAB-OREN3\Desktop\TTCMIN\Summary_Output.csv"

    ego_rows = get_ego_rows(master_csv)
    results = []

    for row in ego_rows:
        obj_id, min_ttc = find_min_ttc_for_walkers(row["EGO_OBJFile"])

        if obj_id is None:
            results.append({
                "Id": row["Id"],
                "Scenario": row["Scenario"],
                "Condition": row["Condition"],
                "Map": row["Map"],
                "TTC": "",
                "min object id": "",
                "Note": "No valid TTC or walkers missing"
            })
        else:
            results.append({
                "Id": row["Id"],
                "Scenario": row["Scenario"],
                "Condition": row["Condition"],
                "Map": row["Map"],
                "TTC": min_ttc,
                "min object id": obj_id,
                "Note": ""
            })

    # שמירה ל-CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)

    print(f"\n✅ Summary file created at: {output_csv}")
