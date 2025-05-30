# USB Device Tracker

A simple Python GUI application that monitors USB device connections and disconnections in real-time.

## Features
- Tracks all USB storage devices
- Shows connection/disconnection history
- Displays device details (name, mount point, size)
- Exports history to text files
- Works on Windows, Linux and macOS

## Requirements
- Python 3.7+ (for source version)
- psutil library (`pip install psutil`)

## How to Use

### From Source:
1. Install requirements: `pip install psutil`
2. Run: `usbtracker.py`

### Using Pre-built Executable:
1. Download the latest release from [Releases page](https://github.com/spark1ch/kernel-console/releases/tag/1.0)
2. Run the executable file (no installation needed)

Files are automatically saved in `/reports` folder with timestamps (e.g. `usb_history_20231215_1423.txt`)

## File Structure
/reports - Auto-created folder for history exports
main.py - Main application file

> Note: On Linux/macOS, run with `sudo` for complete device information.
