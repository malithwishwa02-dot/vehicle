AGENT TASK: LUCID EMPIRE CONSTRUCTION
OBJECTIVE: Build the Sovereign Browser Environment
TARGET: lucid-browser:v1 (Docker Image)

Follow this protocol exactly to create the artifact.

PHASE 1: ASSET ACQUISITION
Initialize Workspace:
mkdir -p lucid_empire/engine
cd lucid_empire
Clone Targets:
Clone the browser engine (Camoufox) into the engine directory.
Clone the runtime (Vehicle) to extract the Docker logic.
git clone [https://github.com/daijro/camoufox.git](https://github.com/daijro/camoufox.git) engine/camoufox_src
git clone [https://github.com/malithwishwa02-dot/vehicle.git](https://github.com/malithwishwa02-dot/vehicle.git) vehicle_src

PHASE 2: SURGICAL MODIFICATION ("THE LOBOTOMY")
GOAL: Remove probabilistic randomness. Enforce deterministic injection.
TARGET FILE: engine/camoufox_src/camoufox/sync_api.py
INSTRUCTION SET:
Open sync_api.py.
Locate the import: from browserforge.fingerprints import FingerprintGenerator
ACTION: Delete the line.
Locate the __init__ method of the Camoufox class.
Find: self.fingerprint_generator = FingerprintGenerator()
ACTION: Replace with:
# LUCID MODIFICATION: Static Injection
self.fingerprint_generator = None 
self.fingerprint_config = config.get('fingerprint_payload', {}) # Load from input
Locate the _get_fingerprint method.
ACTION: Rewrite it to return self.fingerprint_config directly, bypassing the generator.

PHASE 3: CONTAINER FUSION
GOAL: Merge vehicle capabilities (Time/Network) with camoufox execution.
Create docker/Dockerfile.sovereign.
Copy the content provided in the Dockerfile.sovereign file block of this task.
Ensure it installs:
libfaketime (For temporal manipulation)
xvfb (For headless rendering)
ffmpeg (For session recording)
python3-pip

PHASE 4: ORCHESTRATOR DEPLOYMENT
Create core/lucid_orchestrator.py using the code provided in this task.
Dependencies: Ensure flask, docker, requests, and playwright are in requirements.txt.

PHASE 5: THE BUILD
Execute the final build command:
docker build -t lucid-empire:v1 -f docker/Dockerfile.sovereign .

TASK COMPLETE.
