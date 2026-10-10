#!/bin/bash
# After copying a new skysquad.pck and VERSION into this folder, run:  bash update.sh
set -e
cd "$(dirname "$0")"
VER="$(cat VERSION)"
sudo sed -i "s/--version [0-9.]*/--version $VER/" /etc/systemd/system/skysquad.service
sudo systemctl daemon-reload
sudo systemctl restart skysquad
echo "Sky Squad server now runs version $VER"
