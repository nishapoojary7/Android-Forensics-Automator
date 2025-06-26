import subprocess
import re
import time

def analyze_logs():
    time.sleep(2)

    try:
        dumpsys_output = subprocess.check_output(["adb", "shell", "dumpsys", "activity", "intents"], encoding='utf-8', errors='ignore')
    except subprocess.CalledProcessError:
        return {"error": "ADB dumpsys failed"}

    accessed_dirs = set()
    path_patterns = [
        r'/sdcard/\S+',
        r'/storage/emulated/\d+/\S+',
        r'/data/data/\S+',
        r'/mnt/\S+'
    ]

    for line in dumpsys_output.splitlines():
        for pattern in path_patterns:
            match = re.search(pattern, line)
            if match:
                accessed_dirs.add(match.group())

    return {
        "ec_folders": sorted(accessed_dirs)
    }
