# Running Docker Compose in WSL2 (Linux)

## Option 1: Use Existing WSL2 (Quick Try)

You can access your project from within WSL2 and run Docker there:

```powershell
# Enter WSL2
wsl

# Navigate to your project (Windows files are at /mnt/c/)
cd /mnt/c/Users/Barchok/FluxAgent

# Try building
docker compose up --build -d
```

## Option 2: Install Ubuntu/Debian in WSL2 with Native Docker (Recommended)

### Step 1: Install Ubuntu in WSL2

```powershell
# List available distributions
wsl --list --online

# Install Ubuntu (latest)
wsl --install -d Ubuntu

# Or install Ubuntu 22.04 specifically
wsl --install -d Ubuntu-22.04
```

After installation, you'll be prompted to create a username/password.

### Step 2: Install Docker Engine in Ubuntu

```bash
# Open Ubuntu terminal (it will open automatically after install)
# Or run: wsl -d Ubuntu

# Update packages
sudo apt update
sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo service docker start

# Enable Docker to start on boot
sudo systemctl enable docker

# Verify Docker works
docker --version
docker compose version
```

### Step 3: Copy Project to WSL2 (Optional but Recommended)

Copying to Linux filesystem is faster than using Windows mount:

```bash
# From Ubuntu WSL2
# Copy from Windows to Linux filesystem
cp -r /mnt/c/Users/Barchok/FluxAgent ~/FluxAgent
cd ~/FluxAgent

# Or clone from Git if you've pushed it
# git clone <your-repo-url>
# cd FluxAgent
```

### Step 4: Run Docker Compose

```bash
cd ~/FluxAgent
docker compose up --build -d
```

## Option 3: Access WSL2 Docker from Windows

If Docker is running in WSL2, you can still use it from Windows PowerShell by pointing to WSL2:

```powershell
# Set environment variable to use WSL2 Docker
$env:DOCKER_HOST = "tcp://localhost:2375"

# Then run normally
docker compose up --build -d
```

## Troubleshooting

### If Docker service won't start:
```bash
# In WSL2 Ubuntu
sudo service docker status
sudo service docker start

# Or use systemctl (if available)
sudo systemctl status docker
sudo systemctl start docker
```

### If permission denied:
```bash
# Log out and back into WSL2 after adding user to docker group
# Or run commands with sudo (not ideal)
```

### If Windows path issues:
- Use Linux filesystem (`~/FluxAgent`) instead of Windows mount (`/mnt/c/...`)
- Copy files from Windows to Linux: `cp -r /mnt/c/Users/Barchok/FluxAgent ~/`

## Benefits of Native Linux Docker

1. **Faster builds** - No VM overhead
2. **More reliable** - Native Linux kernel
3. **Better performance** - Direct file system access
4. **Easier debugging** - Standard Linux Docker logs

