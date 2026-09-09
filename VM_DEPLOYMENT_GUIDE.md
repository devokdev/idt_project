# Production Linux VM & Cloud Deployment Guide
> **Comprehensive Manual for Deploying "AI Project Mentor" on Ubuntu/Debian Linux Virtual Machines, AWS EC2, GCP Compute Engine, and Azure VMs.**

---

## 1. Virtual Machine Specifications

### Recommended Hardware Tier
- **OS**: Ubuntu 22.04 LTS (x86_64) or Debian 12
- **vCPU**: Minimum 4 vCPUs (8 vCPUs recommended for multi-model concurrent inference)
- **RAM**: Minimum 16 GB (32 GB recommended if hosting 7B quantized models in system RAM)
- **Disk**: 50 GB SSD / NVMe storage
- **GPU (Optional but Recommended)**: NVIDIA T4, A10G, RTX 3060/4090 (with CUDA 12.0+ drivers)

---

## 2. Linux System Provisioning & Prerequisite Setup

Execute the following commands on the remote VM via SSH:

```bash
# Update OS packages
sudo apt update && sudo apt upgrade -y

# Install build essentials, Git, and Python 3.11
sudo apt install -y build-essential curl wget git python3.11 python3.11-venv python3-pip

# Install Docker and Docker Compose plugin
sudo apt install -y apt-transport-https ca-certificates gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Enable Docker for non-root user
sudo usermod -aG docker $USER
newgrp docker
```

---

## 3. Ollama Installation & Systemd Service Configuration

### 3.1 Direct Installation
```bash
# Install Ollama via official installer
curl -fsSL https://ollama.com/install.sh | sh
```

### 3.2 Configure Systemd Service for Network Binding
By default, Ollama only listens on `127.0.0.1:11434`. To ensure Docker and local services can communicate across containers:

```bash
# Create systemd override directory
sudo mkdir -p /etc/systemd/system/ollama.service.d/

# Create environment configuration override
sudo tee /etc/systemd/system/ollama.service.d/environment.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"
Environment="OLLAMA_KEEP_ALIVE=24h"
Environment="OLLAMA_NUM_PARALLEL=4"
EOF

# Reload and restart Ollama service
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl enable ollama
```

### 3.3 Pull Model Weights
```bash
# Download the benchmarked academic mentor models
ollama pull codellama:latest
ollama pull starcoder2:latest
ollama pull phi3:latest
```

---

## 4. Application Deployment (Native Systemd & Gunicorn)

### 4.1 Clone Repository & Setup Virtual Environment
```bash
cd /opt
sudo git clone <YOUR_REPO_URL> IDT_LabProject
sudo chown -R $USER:$USER /opt/IDT_LabProject
cd /opt/IDT_LabProject

# Create and populate virtualenv
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run initial knowledge base ingestion
python scripts/ingest_knowledge_base.py
```

### 4.2 Create Systemd Unit File for FastAPI Backend
```bash
sudo tee /etc/systemd/system/mentor-backend.service > /dev/null <<EOF
[Unit]
Description=AI Project Mentor FastAPI Application Service
After=network.target ollama.service

[Service]
User=$USER
WorkingDirectory=/opt/IDT_LabProject
Environment="PATH=/opt/IDT_LabProject/venv/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONPATH=/opt/IDT_LabProject"
ExecStart=/opt/IDT_LabProject/venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

# Start and enable the service
sudo systemctl daemon-reload
sudo systemctl start mentor-backend
sudo systemctl enable mentor-backend
```

---

## 5. Reverse Proxy Configuration with NGINX

To serve the Web UI and secure the API under port 80/443:

```bash
# Install NGINX
sudo apt install -y nginx

# Configure NGINX reverse proxy & static site
sudo tee /etc/nginx/sites-available/mentor.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Serve static frontend web application
    location / {
        root /opt/IDT_LabProject/frontend;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # Proxy API requests to FastAPI backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 180s;
        proxy_connect_timeout 60s;
    }

    # OpenAPI interactive documentation
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
    }
}
EOF

# Activate configuration
sudo ln -sf /etc/nginx/sites-available/mentor.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## 6. Docker Compose Deployment (Alternative)

If preferred, deploy the entire stack using Docker Compose:

```bash
cd /opt/IDT_LabProject/docker
docker compose up -d --build

# Check status
docker compose ps
```

---

## 7. GPU Pass-Through & CPU Fallback Verification

To verify that the system correctly leverages the GPU (or falls back cleanly on CPU machines):

```bash
# Check if NVIDIA driver and CUDA are available
nvidia-smi

# Check Ollama GPU layer offloading
curl -s http://localhost:11434/api/ps | jq .
```

If no GPU is present, PyTorch and Ollama will automatically utilize CPU vectorization (`AVX2` / `AVX-512`), and SentenceTransformers will automatically map to `device="cpu"`.
