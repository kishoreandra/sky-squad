#!/bin/bash
# Sky Squad server: one-time setup on an Ubuntu cloud machine (Oracle Cloud Always Free works).
# Run:  bash setup.sh
set -e
cd "$(dirname "$0")"
DIR="$(pwd)"
echo "== Sky Squad server setup in $DIR"

# 1. Godot (the game engine) without a screen
if [ ! -x "$DIR/godot" ]; then
  sudo apt-get update -y
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y unzip curl python3 iptables-persistent
  if [ "$(uname -m)" = "aarch64" ]; then GZ=Godot_v4.3-stable_linux.arm64; else GZ=Godot_v4.3-stable_linux.x86_64; fi
  curl -L -o godot.zip "https://github.com/godotengine/godot-builds/releases/download/4.3-stable/$GZ.zip"
  unzip -o godot.zip && mv "$GZ" godot && chmod +x godot && rm godot.zip
fi

# 2. open the game ports on this machine (Oracle's Ubuntu blocks them by default)
sudo iptables -C INPUT -p udp --dport 24870 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT -p udp --dport 24870 -j ACCEPT
sudo iptables -C INPUT -p udp --dport 25001:25012 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT -p udp --dport 25001:25012 -j ACCEPT
sudo netfilter-persistent save

# 3. start the room finder now and after every restart
VER="$(cat VERSION)"
sudo tee /etc/systemd/system/skysquad.service > /dev/null <<EOT
[Unit]
Description=Sky Squad room server
After=network-online.target
[Service]
User=$USER
WorkingDirectory=$DIR
ExecStart=/usr/bin/python3 $DIR/roomd.py --godot $DIR/godot --pack $DIR/skysquad.pck --version $VER
Restart=always
[Install]
WantedBy=multi-user.target
EOT
sudo systemctl daemon-reload
sudo systemctl enable skysquad
sudo systemctl restart skysquad
sleep 2
sudo systemctl --no-pager status skysquad | head -5
echo
echo "== Done. Your server address (type this in the game under ONLINE ROOMS > SERVER):"
curl -s https://ifconfig.me || echo "(see your machine's Public IP in the Oracle console)"
echo
