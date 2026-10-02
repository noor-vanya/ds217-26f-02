#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from copy import error
from dbm import error
from pathlib import Path

from attrs import fields

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """TODO: describe what one usable encounter looks like.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    List of usable encounters: [{'patient_id': 'P001', 'visit_date': '2026-03-02', 'systolic': 118}, {'patient_id': 'P002', 'visit_date': '2026-03-02', 'systolic': 142}, {'patient_id': 'P003', 'visit_date': '2026-03-02', 'systolic': 126}, {'patient_id': 'P005', 'visit_date': '2026-03-02', 'systolic': 134}, {'patient_id': 'P006', 'visit_date': '2026-03-03', 'systolic': 151}, {'patient_id': 'P007', 'visit_date': '2026-03-03', 'systolic': 108}, {'patient_id': 'P009', 'visit_date': '2026-03-03', 'systolic': 138}, {'patient_id': 'P010', 'visit_date': '2026-03-03', 'systolic': 124}, {'patient_id': 'P011', 'visit_date': '2026-03-04', 'systolic': 163}, {'patient_id': 'P012', 'visit_date': '2026-03-04', 'systolic': 119}, {'patient_id': 'P014', 'visit_date': '2026-03-04', 'systolic': 145}, {'patient_id': 'P015', 'visit_date': '2026-03-04', 'systolic': 131}, {'patient_id': 'P017', 'visit_date': '2026-03-05', 'systolic': 122}, {'patient_id': 'P018', 'visit_date': '2026-03-05', 'systolic': 186}, {'patient_id': 'P020', 'visit_date': '2026-03-05', 'systolic': 137}, {'patient_id': 'P006', 'visit_date': '2026-03-05', 'systolic': 148}, {'patient_id': 'P021', 'visit_date': '2026-03-06', 'systolic': 115}, {'patient_id': 'P022', 'visit_date': '2026-03-06', 'systolic': 140}, {'patient_id': 'P023', 'visit_date': '2026-03-06', 'systolic': 133}, {'patient_id': 'P024', 'visit_date': '2026-03-06', 'systolic': 127}, {'patient_id': 'P025', 'visit_date': '2026-03-06', 'systolic': 158}, {'patient_id': 'P011', 'visit_date': '2026-03-06', 'systolic': 169}, {'patient_id': 'P026', 'visit_date': '2026-03-06', 'systolic': 121}, {'patient_id': 'P027', 'visit_date': '2026-03-06', 'systolic': 98}, {'patient_id': 'P028', 'visit_date': '2026-03-06', 'systolic': 144}]
    Skipped: 2
    """
    # TODO: read the rows and skip the header line.
    # TODO: keep a row only when it has three fields, int() can read the
    #       systolic field, and the reading is plausible.
    # TODO: count every other data row as skipped, the blank line included,
    #       and print one line per skipped row so you can see what dropped out.
    # TODO: end with `return encounters, skipped`.
    encounters = []
    skipped = 0
    with open(data_path) as file:
        rows = file.readlines()   
    for row in rows[1:]:                      
        if not row.strip():                   
            print("Skipping a blank row.")
            skipped += 1
            continue
        fields = row.strip().split(",")
        if len(fields) != 3:                  
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, systolic = fields
        try:
            systolic = int(systolic)
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
        else:
            if 60 <= systolic <= 250:
                encounters.append({"patient_id": patient_id, "visit_date": visit_date,"systolic": systolic})

            else:
                print(f"Skipping {patient_id}: blood pressure recording error.")
                skipped += 1
    return encounters, skipped

def main():
    """TODO: describe the two artifacts this writes."""
    encounters, skipped = read_encounters(DATA_PATH)

    # TODO: build the six report lines and write them to output/vitals_report.txt.
    # TODO: read the file back and print it, so you can see what was saved.
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.

    readings = systolic_readings(encounters)

    average = mean_systolic(readings)

    patient_count = count_patients(encounters)

    highest = max(readings)

    lowest = min(readings)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {patient_count}",
        f"Mean systolic: {average:.1f} mmHg",
        f"Highest systolic: {highest} mmHg",
        f"Lowest systolic: {lowest} mmHg",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)

    report_path = OUTPUT_DIR / "vitals_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        for line in report_lines:
            file.write(line + "\n")

    with open(report_path) as file:
        print(file.read())
    cutoff = 130
    flagged_ids = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            flagged_ids.append(encounter["patient_id"])
    flagged_ids = set(flagged_ids)
    followup_path = OUTPUT_DIR / "followup_list.txt"
    with open(followup_path, "w", encoding="utf-8") as file:
        file.write(f"Cutoff: {cutoff}\n")
        file.write("Reason: Systolic blood pressure at or above cutoff\n")
        for patient_id in flagged_ids:
            file.write(f"{patient_id}\n")

if __name__ == "__main__":
    main()
