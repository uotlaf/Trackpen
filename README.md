# Trackpen
## Emulate a stylus with a touchpad

Trackpen is a program that allows you to use the touchpad as a stylus, even if the touchpad does not support absolute mode 

**Note** Trackpen is currently a CLI application, without any graphical interface. 

**Planeed** 
- Mouse emulation mode
- Argument Parsing

## Requirements
- Linux
- A touchpad
- Python 3
- python-evdev 

## How to install
### Debian/Ubuntu
````bash
sudo apt install python-evdev
git clone https://github.com/uotlaf/Trackpen.git
cd Trackpen
./Trackpen.py or python3 Trackpen.py
````
### Arch Linux
````bash
sudo pacman -S python-evdev
git clone https://github.com/uotlaf/Trackpen.git
cd Trackpen
./Trackpen.py or python3 Trackpen.py
````
