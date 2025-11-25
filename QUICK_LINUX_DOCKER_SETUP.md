# Quick Setup: Native Linux Docker in WSL2

## Step-by-Step Instructions

### 1. Install Ubuntu in WSL2

```powershell
# Install Ubuntu 22.04 (recommended)
wsl --install -d Ubuntu-22.04

# Wait for installation to complete
# It will prompt you to create a username and password
```

### 2. Open Ubuntu Terminal

After installation, Ubuntu terminal will open automatically. If not:
```powershell
wsl -d Ubuntu-22.04
```

### 3. Install Docker Engine in Ubuntu

Run these commands in the Ubuntu terminal:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose

# Add your user to docker group (replace 'username' with your Ubuntu username)
sudo usermod -aG docker $USER

# Start Docker
sudo service docker start

# Test Docker
docker --version
docker compose version
```

### 4. Copy Project Files to Linux Filesystem

```bash
# In Ubuntu terminal
cd ~
mkdir -p projects
cp -r /mnt/c/Users/Barchok/FluxAgent ~/projects/
cd ~/projects/FluxAgent

# Verify files are there
ls -la
```

### 5. Run Docker Compose

```bash
cd ~/projects/FluxAgent

# Build and start all services
docker compose up --build -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### 6. Access Your Application

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Langfuse: http://localhost:3001

## Quick Access Later

To access Ubuntu quickly:
```powershell
wsl -d Ubuntu-22.04
```

Or pin Ubuntu to your Start Menu after first use.

## Benefits

✅ Native Linux Docker (faster, more reliable)
✅ Direct file system access
✅ No Docker Desktop overhead
✅ Standard Linux Docker commands

