import os
import hashlib
import stat
import subprocess
from datetime import datetime

def sha256_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def collect_metadata(file_path):
    stat_info = os.stat(file_path)
    return {
        "size": stat_info.st_size,
        "permissions": oct(stat.S_IMODE(stat_info.st_mode)),
        "owner": stat_info.st_uid,
        "group": stat_info.st_gid,
        "last_accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
        "last_modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat()
    }

def check_adb_device():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    connected = [line for line in lines[1:] if 'device' in line and not 'unauthorized' in line]
    return connected[0].split('\t')[0] if connected else None

def adb_pull(device_serial, remote_dir, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    subprocess.run(["adb", "-s", device_serial, "pull", remote_dir, local_dir], check=True)
