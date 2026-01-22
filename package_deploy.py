import zipfile
import os

def zip_deployment():
    zip_name = "PROMETHEUS_V3_EXOE_FINAL.zip"
    print(f"Creating {zip_name}...")
    
    files_to_include = [
        "docker-compose.yml",
        "deploy_prometheus.sh",
        "VPS_DEPLOYMENT.md",
        "prometheus_system_verifier.py"
    ]
    
    dirs_to_include = [
        "prometheus_v3",
        "genesis_gui"
    ]
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add individual files
        for f in files_to_include:
            if os.path.exists(f):
                zf.write(f, f)
                print(f"  + {f}")
        
        # Add directories
        for d in dirs_to_include:
            for root, _, files in os.walk(d):
                # Skip node_modules and output dirs to keep it clean
                if "node_modules" in root or "output" in root or ".git" in root:
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.getcwd())
                    # Ensure we don't zip the zip itself
                    if file == zip_name: continue
                    
                    zf.write(file_path, arcname)
                    # print(f"  + {arcname}")
    
    print(f"\nSUCCESS. Package size: {os.path.getsize(zip_name) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    zip_deployment()
