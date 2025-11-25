#!/bin/bash
# Setup script for Ubuntu WSL2 with Docker
# Run this inside Ubuntu WSL2 after installation

echo "🚀 Setting up Docker in Ubuntu WSL2..."

# Update system
echo "📦 Updating packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt install -y docker.io docker-compose

# Add user to docker group
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# Start Docker service
echo "▶️ Starting Docker service..."
sudo service docker start

# Enable Docker on boot (if systemd available)
if systemctl is-system-running >/dev/null 2>&1; then
    echo "⚙️ Enabling Docker on boot..."
    sudo systemctl enable docker
fi

# Verify installation
echo "✅ Verifying Docker installation..."
docker --version
docker compose version

echo ""
echo "🎉 Docker setup complete!"
echo ""
echo "⚠️ IMPORTANT: You need to log out and log back into WSL2 for group changes to take effect."
echo "Or run: newgrp docker"
echo ""
echo "Then copy your project:"
echo "  cp -r /mnt/c/Users/Barchok/FluxAgent ~/FluxAgent"
echo "  cd ~/FluxAgent"
echo "  docker compose up --build -d"

