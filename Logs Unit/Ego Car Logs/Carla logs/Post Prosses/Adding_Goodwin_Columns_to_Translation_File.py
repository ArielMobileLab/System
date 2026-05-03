from pathlib import Path
from datetime import datetime, time, timedelta
import csv
import re
import unicodedata
from openpyxl import load_workbook


# Files
MAPPING_CSV = Path("calc_simulator_and_corresponding_physiological_files.csv")
CAT_CSV = Path("combined_cat_class.csv")

# Output
OUTPUT_SUFFIX = "_completed_with_categories.xlsx"

# Path correction: H drive -> G drive
OLD_PATH = r"H:\My Drive\Ariel Uni"
NEW_PATH = r"G:\My Drive\Ariel Uni"


def clean_text(value):
    """Normalize text for comparison."""
    if value is None:
        return ""

    value = str(value)
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u200f", "").replace("\u200e", "").replace("\ufeff", "")
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def fix_path(path):
    """Replace H drive with G drive."""
    path = clean_text(path).strip('"')

    if path.lower().startswith(OLD_PATH.lower()):
        path = NEW_PATH + path[len(OLD_PATH):]

    return path


def clean_time(value):
    """Convert time to HH:MM:SS format."""
    if value is None:
        return ""

    if isinstance(value, datetime):
        value = value.time()

    if isinstance(value, time):
        return f"{value.hour:02}:{value.minute:02}:{value.second:02}"

    if isinstance(value, timedelta):
        seconds = round(value.total_seconds())
        return seconds_to_time(seconds)

    if isinstance(value, (int, float)):
        if 0 <= value < 1:
            seconds = round(value * 24 * 3600)  # Excel time format
        else:
            seconds = round(value)

        return seconds_to_time(seconds)

    value = str(value).strip().replace(".", ":")
    parts = value.split(":")

    try:
        if len(parts) == 3:
            h, m, s = parts
            return f"{int(h):02}:{int(m):02}:{int(float(s)):02}"

        if len(parts) == 2:
            h, m = parts
            return f"{int(h):02}:{int(m):02}:00"

    except ValueError:
        pass

    return value


def seconds_to_time(seconds):
    """Convert seconds to HH:MM:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02}:{m:02}:{s:02}"


def read_csv_file(path):
    """Read CSV file. In this project, cp1255 reads the Hebrew correctly."""
    with open(path, "r", encoding="cp1255", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return reader.fieldnames, rows


def find_time_and_text_columns(ws):
    """Find the Excel columns named זמן and טקסט."""
    for row in range(1, min(ws.max_row, 30) + 1):
        headers = {}

        for col in range(1, ws.max_column + 1):
            header = clean_text(ws.cell(row=row, column=col).value)

            if header:
                headers[header] = col

        if "זמן" in headers and "טקסט" in headers:
            return row, headers["זמן"], headers["טקסט"]

    raise ValueError("Could not find 'זמן' and 'טקסט' columns")


def column_is_empty(ws, col):
    """Check if an entire Excel column is empty."""
    for row in range(1, ws.max_row + 1):
        if ws.cell(row=row, column=col).value not in (None, ""):
            return False

    return True


def find_empty_columns(ws, number_of_columns):
    """Find the first block of empty columns."""
    for start_col in range(1, ws.max_column + number_of_columns + 50):
        empty_block = True

        for col in range(start_col, start_col + number_of_columns):
            if not column_is_empty(ws, col):
                empty_block = False
                break

        if empty_block:
            return start_col

    raise ValueError("Could not find empty columns")


def make_category_lookup(cat_rows, cat_headers, filename):
    """
    Build lookup table from combined_cat_class.csv.

    Key:
    time_shira + text_shira

    Value:
    category columns D:N
    """
    category_headers = cat_headers[3:14]  # CSV columns D:N
    lookup = {}

    for row in cat_rows:
        if clean_text(row.get("filename")) != clean_text(filename):
            continue

        key = (
            clean_time(row.get("time_shira")),
            clean_text(row.get("text_shira")),
        )

        values = []
        for header in category_headers:
            value = row.get(header)

            if value is None or str(value).strip() == "":
                values.append(None)
            elif str(value).strip().isdigit():
                values.append(int(value))
            else:
                values.append(value)

        lookup[key] = values

    return category_headers, lookup


def process_transcript(xlsx_path, cat_rows, cat_headers):
    """Add category columns to one transcript Excel file."""
    xlsx_path = Path(xlsx_path)

    if not xlsx_path.exists():
        print(f"[SKIP] File not found: {xlsx_path}")
        return False

    output_path = xlsx_path.with_name(xlsx_path.stem + OUTPUT_SUFFIX)

    # Safety: never overwrite the original or an existing output file
    if output_path.resolve() == xlsx_path.resolve():
        raise RuntimeError("Output path is identical to source path")

    if output_path.exists():
        raise FileExistsError(f"Output already exists, not overwriting: {output_path}")

    wb = load_workbook(xlsx_path)
    ws = wb.active

    header_row, time_col, text_col = find_time_and_text_columns(ws)

    category_headers, lookup = make_category_lookup(
        cat_rows,
        cat_headers,
        xlsx_path.name,
    )

    start_col = find_empty_columns(ws, len(category_headers))

    # Write category headers
    for i, header in enumerate(category_headers):
        ws.cell(row=header_row, column=start_col + i).value = header

    matched = 0

    # Fill matching rows
    for row in range(header_row + 1, ws.max_row + 1):
        key = (
            clean_time(ws.cell(row=row, column=time_col).value),
            clean_text(ws.cell(row=row, column=text_col).value),
        )

        if key not in lookup:
            continue

        for i, value in enumerate(lookup[key]):
            ws.cell(row=row, column=start_col + i).value = value

        matched += 1

    wb.save(output_path)

    print(f"Saved: {output_path}")
    print(f"Matched rows: {matched}")

    return True


def main():
    # Read input files
    _, mapping_rows = read_csv_file(MAPPING_CSV)
    cat_headers, cat_rows = read_csv_file(CAT_CSV)

    # Collect unique transcript paths from mapping table
    transcript_paths = []

    for row in mapping_rows:
        path = fix_path(row.get("TranscriptionManualFile"))

        if path and path not in transcript_paths:
            transcript_paths.append(path)

    print(f"Transcript files found: {len(transcript_paths)}")

    # Process each transcript file
    processed = 0

    for path in transcript_paths:
        try:
            if process_transcript(path, cat_rows, cat_headers):
                processed += 1

        except Exception as e:
            print(f"[ERROR] {path}")
            print(e)

    print(f"Done. Processed files: {processed}")


if __name__ == "__main__":
    main()
