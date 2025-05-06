import os
import csv
import json
from datetime import datetime

def load_changes(device_id):
    file_path = os.path.expanduser(f"~/integrity_checker/hashes/{device_id}_comparison.json")
    if not os.path.exists(file_path):
        print(f"[-] Comparison file not found: {file_path}")
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_csv_report(changes, device_id):
    csv_file = os.path.expanduser(f"~/integrity_checker/reports/{device_id}_report.csv")
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "File", "Before (metadata)", "After (metadata)"])

        for file in changes["new_files"]:
            writer.writerow(["NEW", file, "-", "-"])

        for file in changes["deleted_files"]:
            writer.writerow(["DELETED", file, "-", "-"])

        for file in changes["modified"]:
            writer.writerow(["MODIFIED", file, "-", "-"])

        for entry in changes["metadata_changed"]:
            writer.writerow([
                "METADATA_CHANGED",
                entry["file"],
                json.dumps(entry["before"]),
                json.dumps(entry["after"])
            ])

    print(f"[+] CSV report saved to: {csv_file}")

def generate_txt_summary(changes, device_id):
    txt_file = os.path.expanduser(f"~/integrity_checker/reports/{device_id}_report.txt")
    with open(txt_file, 'w') as f:
        f.write(f"=== Integrity Report for {device_id} ===\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        for key in changes:
            f.write(f"--- {key.upper()} ({len(changes[key])}) ---\n")
            if key == "metadata_changed":
                for entry in changes[key]:
                    f.write(f"{entry['file']}\n")
                    f.write(f"  BEFORE: {entry['before']}\n")
                    f.write(f"  AFTER : {entry['after']}\n")
            else:
                for file in changes[key]:
                    f.write(f"{file}\n")
            f.write("\n")

    print(f"[+] TXT summary saved to: {txt_file}")

def run(device_number, formats):
    print("[DEBUG] Starting report.run()")
    device_id = f"device_{device_number.zfill(3)}"

    changes = load_changes(device_id)
    if not changes:
        return

    if "csv" in formats:
        generate_csv_report(changes, device_id)

    if "txt" in formats:
        generate_txt_summary(changes, device_id)
