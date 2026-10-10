SKY SQUAD SERVER (version in VERSION)

Files
  roomd.py      the room finder (phones ask it where a room is)
  skysquad.pck  the game itself; each room runs its own copy with no screen
  setup.sh      one-time setup: bash setup.sh
  update.sh     after replacing skysquad.pck + VERSION: bash update.sh

Ports to open in the cloud firewall (Oracle: Security List, "Ingress Rules"):
  UDP 24870          room finder
  UDP 25001-25012    rooms (one port per room, up to 12 rooms at once)

Each room uses about 190 MB of memory and very little CPU.
Rooms close by themselves 90 seconds after everyone leaves.

See what is happening:  journalctl -u skysquad -f
Room logs:              room-<CODE>.log in this folder
