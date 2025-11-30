#!/usr/bin/env bash
set -e  # Exit on error

echo "=== Raspberry Pi Project Setup ==="

#-------------------------------
# 1. Load apt packages file
#-------------------------------
APT_FILE="apt-packages.txt"

if [[ ! -f "$APT_FILE" ]]; then
    echo "ERROR: $APT_FILE not found!"
    exit 1
fi

echo "Installing APT packages from $APT_FILE..."
sudo apt update
sudo xargs -a "$APT_FILE" apt install -y

echo "APT packages installed."

#-------------------------------
# 2. Create the virtual environment
#-------------------------------
if [[ ! -d ".venv" ]]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists — skipping creation."
fi

echo "Activating virtual environment..."
source .venv/bin/activate

#-------------------------------
# 3. Install Python requirements
#-------------------------------
REQ_FILE="requirements.txt"

if [[ -f "$REQ_FILE" ]]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r "$REQ_FILE"
else
    echo "WARNING: requirements.txt not found — skipping pip install."
fi

#-------------------------------
# 4. Install and check pigpiod
#-------------------------------
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
sudo tee /etc/systemd/system/pigpiod.service > dev.null <<EOF
[Unit]
Description=Daemon required to control GPIO pins via pigpio
After=network.target

[Service]
ExecStart=/usr/local/bin/pigpiod
Type=forking

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
echo "Enabling pigpiod..."
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo "Checking pigpiod status..."
if pgrep pigpiod >/dev/null; then
    echo "pigpiod is running."
else
    echo "ERROR: pigpiod failed to start!"
    exit 1
fi

#-------------------------------
# 5. Test Picamera2 import
#-------------------------------
source .venv/bin/activate
echo "Testing Picamera2..."
python3 - << 'EOF'
try:
    from picamera2 import Picamera2
    print("Picamera2 import successful.")
except Exception as e:
    print("Picamera2 import FAILED:")
    print(e)
    exit(1)
EOF

#-------------------------------
# 6. Test pigpio import
#-------------------------------
source .venv/bin/activate
echo "Testing pigpio..."
python3 - << 'EOF'
try:
    import pigpio
    print("pigpio import successful.")
except Exception as e:
    print("pigpio import FAILED:")
    print(e)
    exit(1)
EOF
# --- 7. Setup systemd service for Flask ---
sudo tee /etc/systemd/system/flaskapp.service > /dev/null <<EOF
[Unit]
Description=Flask Facial Tracker Server
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=/home/$(whoami)/camera-tripod
ExecStart=/home/$(whoami)/camera-tripod/.venv/bin/python server.py
Restart=always
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp

# --- 8. Setup Openbox autostart for kiosk mode ---
mkdir -p ~/.config/openbox
tee ~/.config/openbox/autostart > /dev/null <<'EOF'
# Hide mouse after 0 seconds (always visible)
# To hide mouse automatically, change -idle value
unclutter -idle 1 &

# Disable screen blanking
xset -dpms
xset s off
xset s noblank

# Wait for Flask server to start
sleep 5

# Launch Chromium in kiosk mode with cursor visible
chromium \
    --noerrdialogs \
    --disable-infobars \
    --kiosk http://localhost:5000 \
    --incognito \
    --disable-gpu \
    --disable-software-rasterizer \
    --overscroll-history-navigation=0 &
EOF

# --- 9. Auto-start X on login ---
# Add to ~/.bash_profile if not already present
grep -qxF 'if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then startx -- -nocursor; fi' ~/.bash_profile || \
echo 'if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then startx -- -nocursor; fi' >> ~/.bash_profile

echo ""
echo "=== Setup Complete! ==="
echo "To start working, activate your venv with:"
echo "source .venv/bin/activate"
