import os
import json

def load_snapshot(path):
    with open(path, 'r') as f:
        return json.load(f)

def compare_snapshots(snapshot1, snapshot2):
    changes = {
        "modified": [],
        "new_files": [],
        "deleted_files": [],
        "metadata_changed": []
    }

    files1 = set(snapshot1.keys())
    files2 = set(snapshot2.keys())

    changes["new_files"] = sorted(list(files2 - files1))
    changes["deleted_files"] = sorted(list(files1 - files2))

    keys_to_check = ["size", "permissions", "owner", "group"]

    for file in files1 & files2:
        file1 = snapshot1[file]
        file2 = snapshot2[file]

        if file1["sha256"] != file2["sha256"]:
            changes["modified"].append(file)
        else:
            meta1 = file1["metadata"]
            meta2 = file2["metadata"]
            if any(meta1[k] != meta2[k] for k in keys_to_check):
                changes["metadata_changed"].append({
                    "file": file,
                    "before": {k: meta1[k] for k in keys_to_check},
                    "after": {k: meta2[k] for k in keys_to_check}
                })

    return changes

def run(device_number):
    print("[DEBUG] Starting compare.run()")
    device_id = f"device_{device_number.zfill(3)}"

    base_file = os.path.expanduser(f"~/integrity_checker/hashes/{device_id}_snapshot.json")
    new_file = os.path.expanduser(f"~/integrity_checker/hashes/{device_id}_snapshot_new.json")
    output_file = os.path.expanduser(f"~/integrity_checker/hashes/{device_id}_comparison.json")

    if not os.path.exists(base_file) or not os.path.exists(new_file):
        print("[-] One or both snapshot files not found.")
        print(f"Expected:\n{base_file}\n{new_file}")
        return

    base_snapshot = load_snapshot(base_file)
    new_snapshot = load_snapshot(new_file)

    changes = compare_snapshots(base_snapshot, new_snapshot)

    # Display summary
    for k, v in changes.items():
        print(f"\n=== {k.upper()} ({len(v)}) ===")
        if k == "metadata_changed":
            for item in v:
                print(f"- {item['file']}")
                print(f"  BEFORE: {item['before']}")
                print(f"  AFTER : {item['after']}")
        else:
            for file in v:
                print(f"- {file}")

    # Save to JSON for reporting
    with open(output_file, 'w') as f:
        json.dump(changes, f, indent=4)
    print(f"\n[+] Comparison results saved to: {output_file}")
