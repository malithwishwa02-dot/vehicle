import os
import zipfile

PROJECT_NAME = "chronos-vehicle"

def build_zip():
    zip_name = f"{PROJECT_NAME}.zip"
    if os.path.exists(zip_name):
        os.remove(zip_name)
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_NAME):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, PROJECT_NAME)
                zipf.write(file_path, arcname)
    print(f"[+] Created {zip_name}")

if __name__ == '__main__':
    build_zip()
