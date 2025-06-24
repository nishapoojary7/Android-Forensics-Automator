import os
import subprocess
from datetime import datetime

def pull_directories(package_name, selected_paths):
    pulled_paths = []

    for path in selected_paths:
        # Create a safe folder name using path
        safe_name = path.replace("/", "_").strip("_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        local_path = os.path.join("snapshots", f"{safe_name}_{timestamp}")

        # Make directory
        os.makedirs(local_path, exist_ok=True)

        try:
            # Pull from emulator to snapshots/local_path
            subprocess.run(["adb", "pull", path, local_path], check=True)
            pulled_paths.append(os.path.basename(local_path))
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to pull {path}: {e}")

    return pulled_paths
