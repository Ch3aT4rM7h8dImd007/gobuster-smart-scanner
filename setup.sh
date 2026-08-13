#!/usr/bin/env bash
# Setup script for Gobuster Smart Scanner

set -e

echo -e "\n[+] Gobuster Smart Scanner Setup\n"

# Update package lists
echo "[+] Updating package lists..."
sudo apt update -qq

# Install system dependencies
echo "[+] Installing system dependencies (gobuster, proxychains, curl)..."
sudo apt install -y gobuster proxychains4 curl git

# Check if Python3 and pip3 are installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Installing..."
    sudo apt install -y python3 python3-pip
fi

# Install Python dependencies
echo "[+] Installing Python dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "[!] requirements.txt not found. Installing requests only..."
    pip3 install requests
fi

# Make the main script executable
if [ -f "gobuster_scanner.py" ]; then
    chmod +x gobuster_scanner.py
    echo "[+] Made gobuster_scanner.py executable"
else
    echo "[!] gobuster_scanner.py not found in current directory."
    echo "    Please rename your script to gobuster_scanner.py or adjust the shebang."
fi

# Optional: download SecLists if not present
if [ ! -d "/usr/share/seclists" ]; then
    echo "[+] Downloading SecLists wordlists (this may take a moment)..."
    sudo git clone --depth 1 https://github.com/danielmiessler/SecLists.git /usr/share/seclists
else
    echo "[+] SecLists already present."
fi

echo -e "\n[+] Setup complete! You can now run the scanner:\n"
echo "    python3 gobuster_scanner.py <target-domain>"
echo "    or"
echo "    ./gobuster_scanner.py <target-domain>"
echo
