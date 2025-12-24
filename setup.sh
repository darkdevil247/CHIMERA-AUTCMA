#!/bin/bash
# setup.sh - Chimera-Automata Installation Script
# FOR AUTHORIZED SECURITY RESEARCH ONLY

echo "████████████████████████████████████████████████████"
echo "█           CHIMERA-AUTOMATA SETUP                █"
echo "█     FOR AUTHORIZED PENETRATION TESTING         █"
echo "████████████████████████████████████████████████████"
echo ""
echo "[!] WARNING: This tool is for legal security testing only!"
echo "[!] Using against unauthorized systems is ILLEGAL!"
echo ""
read -p "Do you agree to use this only for authorized testing? (yes/no): " agree
if [ "$agree" != "yes" ]; then
    echo "Exiting..."
    exit 1
fi

echo "[*] Starting installation..."
echo "[*] Updating system packages..."

# Update system
sudo apt update && sudo apt upgrade -y

echo "[*] Installing core dependencies..."

# Install system packages
sudo apt install -y \
    python3 python3-pip python3-venv \
    git curl wget \
    apache2 nginx \
    openjdk-17-jdk android-sdk-platform-tools \
    golang ruby-full \
    metasploit-framework \
    apktool dex2jar jd-gui \
    zipalign apksigner \
    qrencode libssl-dev \
    npm nodejs \
    wireshark tcpdump \
    sqlite3 \
    tmux screen \
    default-jre \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    sshpass \
    whois

echo "[*] Installing Python packages..."

# Install Python packages
pip3 install --upgrade pip
pip3 install flask flask-socketio flask-cors \
    requests pyngrok colorama \
    qrcode[pil] pillow cryptography \
    captcha watchdog python-dotenv \
    rich prompt_toolkit \
    paramiko scapy netifaces \
    psutil pyinstaller

echo "[*] Installing Node.js packages..."
npm install -g localtunnel ngrok

echo "[*] Setting up Metasploit database..."
sudo systemctl start postgresql
sudo msfdb init

echo "[*] Creating configuration files..."

# Create main configuration
cat > ~/chimera-automata/configs/main_config.json << EOF
{
    "project_name": "Chimera-Automata",
    "version": "1.0.0",
    "legal_warning": "FOR AUTHORIZED TESTING ONLY",
    "web_port": 8080,
    "c2_port": 8443,
    "default_lhost": "auto",
    "keystore_pass": "chimera_secure_123",
    "auto_start_servers": true,
    "log_level": "INFO"
}
EOF

# Create Android keystore
echo "[*] Creating Android signing keystore..."
keytool -genkey -v -keystore ~/chimera-automata/android_factory/chimera.keystore \
    -alias chimera -keyalg RSA -keysize 2048 \
    -validity 10000 -storepass chimera_secure_123 \
    -keypass chimera_secure_123 \
    -dname "CN=Android Security, OU=Research, O=Chimera Labs, C=US" <<< $'\n\n\n\n\n\n\n\n'

echo "[*] Setting file permissions..."
chmod +x ~/chimera-automata/scripts/*.sh 2>/dev/null || true

echo "[*] Creating startup script..."
cat > /usr/local/bin/chimera << 'EOF'
#!/bin/bash
cd ~/chimera-automata
source venv/bin/activate
python3 main.py "$@"
EOF

chmod +x /usr/local/bin/chimera

echo "████████████████████████████████████████████████████"
echo "█            SETUP COMPLETE!                       █"
echo "█                                                  █"
echo "█  To start: chimera                              █"
echo "█  Or: cd ~/chimera-automata && python3 main.py   █"
echo "█                                                  █"
echo "█  [!] REMEMBER: FOR AUTHORIZED TESTING ONLY!     █"
echo "████████████████████████████████████████████████████"
echo ""
echo "[+] Installation complete!"
echo "[+] Reboot or source ~/.bashrc to update PATH"
echo ""
