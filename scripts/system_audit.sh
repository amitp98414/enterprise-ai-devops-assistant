#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo " DEVOPS SYSTEM AUDIT"
echo "========================================"

echo
echo "=== BASIC SYSTEM INFORMATION ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Uptime: $(uptime -p)"

echo
echo "=== CPU INFORMATION ==="
echo "CPU cores: $(nproc)"
lscpu | grep -E "Model name|CPU\(s\)" | head -n 2 || true

echo
echo "=== MEMORY INFORMATION ==="
free -h

echo
echo "=== DISK INFORMATION ==="
df -h /

echo
echo "=== NETWORK INTERFACES ==="
ip -brief address

echo
echo "=== LISTENING PORTS ==="
ss -tulpn || true

echo
echo "=== DEVOPS TOOLS ==="

if command -v git >/dev/null 2>&1; then
    git --version
else
    echo "Git: NOT INSTALLED"
fi

if command -v docker >/dev/null 2>&1; then
    if docker --version >/dev/null 2>&1; then
        docker --version
    else
        echo "Docker CLI: FOUND BUT NOT WORKING"
    fi
else
    echo "Docker: NOT INSTALLED"
fi

if docker compose version >/dev/null 2>&1; then
    docker compose version
else
    echo "Docker Compose: NOT INSTALLED"
fi

if command -v aws >/dev/null 2>&1; then
    aws --version
else
    echo "AWS CLI: NOT INSTALLED"
fi

if command -v terraform >/dev/null 2>&1; then
    terraform version | head -n 1
else
    echo "Terraform: NOT INSTALLED"
fi

if command -v kubectl >/dev/null 2>&1; then
    kubectl version --client
else
    echo "Kubectl: NOT INSTALLED"
fi

echo
echo "=== RUNNING DOCKER CONTAINERS ==="

if command -v docker >/dev/null 2>&1; then
    if docker info >/dev/null 2>&1; then
        docker ps
    else
        echo "Docker daemon: NOT AVAILABLE"
    fi
else
    echo "Docker: NOT INSTALLED"
fi

echo
echo "========================================"
echo " AUDIT COMPLETED"
echo "========================================"\

