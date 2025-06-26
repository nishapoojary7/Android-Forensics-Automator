import subprocess
import re

AAPT_PATH = r"C:\Users\nisha\AppData\Local\Android\Sdk\build-tools\35.0.0\aapt.exe"

def analyze_manifest(apk_path):
    try:
        output = subprocess.check_output([AAPT_PATH, "dump", "badging", apk_path], encoding='utf-8', errors='ignore')
        package_match = re.search(r"package: name='(.*?)'", output)
        if not package_match:
            return {"error": "Could not extract package name"}

        package_name = package_match.group(1)
        private_dir = f"/data/data/{package_name}"

        permissions_output = subprocess.check_output([AAPT_PATH, "dump", "permissions", apk_path], encoding='utf-8', errors='ignore')
        permissions = permissions_output.splitlines()

        additional_dirs = []
        if any("WRITE_EXTERNAL_STORAGE" in perm for perm in permissions):
            additional_dirs = ["/sdcard/Download", "/sdcard/Documents"]

        return {
            "package_name": package_name,
            "private_folder": private_dir,
            "additional_folders": additional_dirs
        }

    except Exception as e:
        return {"error": str(e)}
