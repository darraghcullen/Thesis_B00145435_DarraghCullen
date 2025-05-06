import os
import subprocess
import hashlib
import json
import stat
from datetime import datetime

from file_checker.utils import sha256_hash, collect_metadata, check_adb_device, adb_pull

def process_directory(base_path):
    snapshot = {}
    for root, _, files in os.walk(base_path):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, base_path)
            snapshot[rel_path] = {
                "sha256": sha256_hash(abs_path),
                "metadata": collect_metadata(abs_path)
            }
    return snapshot

def run(device_number, remote_dir):
    device_id = f"device_{device_number.zfill(3)}"

    local_dir = os.path.expanduser(f"~/integrity_checker/device_snapshots/{device_id}/DCIM")
    output_file = os.path.expanduser(f"~/integrity_checker/hashes/{device_id}_snapshot.json")

    print(f"\n[+] Extracting from device {device_id}")
    print(f"[+] Pulling from {remote_dir} to {local_dir}")

    device_serial = check_adb_device()
    if not device_serial:
        print("[-] No authorized Android device found.")
        return

    adb_pull(device_serial, remote_dir, local_dir)
    print(f"[+] Files saved to: {local_dir}")

    snapshot = process_directory(local_dir)

    with open(output_file, 'w') as f:
        json.dump(snapshot, f, indent=4)

    print(f"[+] Snapshot saved to: {output_file}")
