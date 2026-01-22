# PROMETHEUS-CORE v3.3 :: VPS DEPLOYMENT PROTOCOL
AUTHORITY: Dva.13 | TARGET: UBUNTU 24.04 (Recommended)
STATUS: EXOE_BUILD_ACTIVE

This guide will deploy the full Hermit Crab stack v3.3 (Exoe Build):
- **Backend:** Python/Flask Engine (Behavioral Inference Engine + MLX Replication).
- **Frontend:** React GUI (Exoe Dashboard with Lifestyle Matrix).
- **Infrastructure:** Docker Compose (Orchestration).

## 1. SERVER INITIALIZATION

Login to your VPS as root:
```bash
ssh root@your_vps_ip
```

Update & Install Core Dependencies:
```bash
apt update && apt upgrade -y
apt install -y docker.io docker-compose git nodejs npm unzip
```

Verify Docker is running:
```bash
systemctl start docker
systemctl enable docker
```

## 2. FILE STRUCTURE SETUP

Create the project directory and the required subfolders:
```bash
mkdir -p /root/prometheus_v3/backend
mkdir -p /root/prometheus_v3/frontend
mkdir -p /root/prometheus_v3/output
cd /root/prometheus_v3
```

## 3. BACKEND DEPLOYMENT (Python Core v3.3)

### Step 3.1: Create the Backend Files

Navigate to the backend folder:
```bash
cd /root/prometheus_v3/backend
```

Create `requirements.txt`:
```bash
nano requirements.txt
```
Paste content:
```text
Flask==2.3.2
Flask-Cors==4.0.0
requests==2.31.0
```

Create `app.py`:
```bash
nano app.py
```
*(Paste the "PROMETHEUS-CORE v3.3 :: THE EXOE BUILD" Python code provided in the project)*

Create `Dockerfile`:
```bash
nano Dockerfile
```
Paste content:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install SQLite and System Utils
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
# Create necessary dirs
RUN mkdir -p output logs templates/mlx_clean

EXPOSE 5000

CMD ["python", "app.py"]
```

## 4. FRONTEND DEPLOYMENT (React GUI v3.3)

### Step 4.1: Initialize React App

Navigate to the frontend folder:
```bash
cd /root/prometheus_v3/frontend
```

Initialize a blank React project:
```bash
npx create-react-app . --template \
    && npm install lucide-react \
    && npm install -D tailwindcss postcss autoprefixer \
    && npx tailwindcss init -p
```

### Step 4.2: Configure Tailwind

Edit `tailwind.config.js`:
```bash
nano tailwind.config.js
```
Replace content `[]` with:
```javascript
content: [
    "./src/**/*.{js,jsx,ts,tsx}",
],
```

Edit `src/index.css`:
```bash
nano src/index.css
```
Add to the top:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 4.3: Inject the GUI Code

Edit `src/App.js`:
```bash
nano src/App.js
```
*(Paste the "PROMETHEUS v3.3 // EXOE FINAL" React code. IMPORTANT: Change API_URL line to your VPS IP or Domain.)*
Example:
```javascript
const API_URL = "http://YOUR_VPS_IP:5000"; 
// OR keep "http://localhost:5000" if using SSH tunneling.
```

## 5. DOCKER ORCHESTRATION

Navigate back to root project folder:
```bash
cd /root/prometheus_v3
```

Create `docker-compose.yml`:
```bash
nano docker-compose.yml
```
Paste content:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: prometheus_core
    ports:
      - "5000:5000"
    volumes:
      - ./output:/app/output
    restart: always

  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    container_name: prometheus_gui
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: always
```

Create Frontend `Dockerfile` (for Production Build):
```bash
nano frontend/Dockerfile
```
Paste content:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
```

## 6. LAUNCH SEQUENCE

Build and Run:
```bash
cd /root/prometheus_v3
docker-compose up --build -d
```

Verify Running Containers:
```bash
docker ps
```
You should see `prometheus_core` on port 5000 and `prometheus_gui` on port 3000.

## 7. ACCESS & USAGE

- **Open Browser:** Navigate to `http://YOUR_VPS_IP:3000`.
- **Interface:** You will see the PROMETHEUS-CORE v3.3 Console.
- **Execute:**
    1. **Identity:** Enter Fullz (Name, Address, CC).
    2. **Chronos:** Set Profile Age (e.g., 90 Days).
    3. **AI Matrix:** Click "INITIATE GENESIS". The system will first calculate the Lifestyle Matrix (Active Hours, Abandonment Rates) before generating the profile.
- **Download:** Once the terminal says "SUCCESS", click DOWNLOAD MLX PROFILE.

### Troubleshooting

Firewall: Ensure ports 3000 and 5000 are open.
```bash
ufw allow 3000
ufw allow 5000
```

CORS Error: If the GUI cannot talk to the backend, ensure `flask-cors` is installed in backend and `API_URL` in React points to the correct IP.

**MISSION STATUS: EXOE_READY.**
