# 🚀 FluxAgent - Start Here (Linux Docker Setup)

## Quick Setup (5 minutes)

### Step 1: Install Ubuntu in WSL2

Run in PowerShell:
```powershell
wsl --install -d Ubuntu-22.04
```

**Wait for installation** - it will prompt for username/password.

### Step 2: Open Ubuntu Terminal

After installation, Ubuntu opens automatically. If not:
```powershell
wsl -d Ubuntu-22.04
```

### Step 3: Setup Docker

In Ubuntu terminal, run:
```bash
# Copy the setup script to Ubuntu
cp /mnt/c/Users/Barchok/FluxAgent/setup-wsl-docker.sh ~/

# Make it executable
chmod +x ~/setup-wsl-docker.sh

# Run it
~/setup-wsl-docker.sh
```

**OR** run commands manually:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
sudo service docker start
docker --version
```

### Step 4: Activate Docker Group

```bash
# Log out and back in, OR run:
newgrp docker
```

### Step 5: Copy Project & Run

```bash
# Copy project to Linux filesystem (faster than Windows mount)
cp -r /mnt/c/Users/Barchok/FluxAgent ~/FluxAgent
cd ~/FluxAgent

# Build and start
docker compose up --build -d

# Check status
docker compose ps
```

### Step 6: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Langfuse UI**: http://localhost:3001

## Why This Works Better

✅ **Native Linux Docker** - No VM overhead  
✅ **Faster builds** - Direct filesystem access  
✅ **More reliable** - Standard Linux Docker  
✅ **Better performance** - No Docker Desktop layer  

## Troubleshooting

**Docker not starting?**
```bash
sudo service docker start
sudo service docker status
```

**Permission denied?**
```bash
newgrp docker
# Or log out/in to WSL2
```

**Ports in use?**
```bash
docker compose down
docker compose up -d
```

## Quick Commands

```bash
# Enter Ubuntu
wsl -d Ubuntu-22.04

# Navigate to project
cd ~/FluxAgent

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart services
docker compose restart

# Stop all
docker compose down
```

