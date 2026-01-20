# Garage Door Automation - Complete Build Guide

This guide will walk you through building your own smart garage door opener from scratch. It is designed for beginners.

---

## Part 1: Hardware Setup

### 1. Gather Components
Refer to the [Shopping List](shopping_list.md) for parts. You need:
*   Raspberry Pi Zero 2 W (or any Pi 3/4)
*   Relay Module (5V)
*   Magnetic Reed Switch (Wired)
*   Jumper Wires & Wiring
*   **SD Card Reader** (for your PC to write the OS)

### 2. Wiring Diagram
**WARNING**: Ensure your Raspberry Pi is unpowered while wiring.

| Component | Pin Name | Connects To | Raspberry Pi Pin (BCM) |
| :--- | :--- | :--- | :--- |
| **Relay** | VCC | 5V Power | Pin 2 or 4 (5V) |
| **Relay** | GND | Ground | Pin 6 (GND) |
| **Relay** | IN (Signal) | GPIO 17 | Pin 11 (GPIO 17) |
| **Reed Switch** | Wire 1 | Ground | Pin 9 (GND) |
| **Reed Switch** | Wire 2 | GPIO 27 | Pin 13 (GPIO 27) |

> **Note**: The Reed Switch has no polarity. It doesn't matter which wire goes to Ground vs GPIO 27.

### 3. Physical Installation
1.  **Reed Switch**: Mount the magnet on the door and the wired sensor on the frame. They should be <1 inch apart when the door is closed.
2.  **Relay**: Connect the relay's "Normally Open" (NO) and "Common" (COM) screw terminals to the two terminals on your garage door opener motor (where the wall button wires connect).

---

## Part 2: Raspberry Pi Setup (OS)

### 1. Flash the OS
1.  Download **Raspberry Pi Imager** on your PC.
2.  Insert your MicroSD card.
3.  **Choose OS**: Select "Raspberry Pi OS Lite (64-bit)" (No Desktop needed).
4.  **Choose Storage**: Select your SD Card.
5.  **Click Next**, then **Edit Settings** (The Gear Icon):
    *   [x] Set Hostname: `garagepi`
    *   [x] Set Username and Password (e.g., `pi` / `raspberry`)
    *   [x] Configure Wireless LAN: Enter your WiFi Name & Password.
    *   [x] Enable SSH: Use password authentication.
6.  **Write** the OS.

### 2. First Boot
1.  Insert SD card into Pi and power it up.
2.  Wait 2-3 minutes for first boot.
3.  Open a terminal (Command Prompt/PowerShell) on your PC and run:
    ```bash
    ssh pi@garagepi.local
    ```
    (Enter the password you created e.g., `raspberry`)

---

## Part 3: Software Installation

Once logged into your Pi via SSH:

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Get the Code
You can copy this project to your Pi. If you have git installed:
```bash
sudo apt install git -y
git clone https://github.com/SonOfMithras/Garage-Project.git
cd Garage-Project
```

### 3. Install Dependencies
Set up a virtual environment so we don't mess up system packages:
```bash
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
*(If `requirements.txt` is missing, run: `pip install flask RPi.GPIO`)*

### 4. Test It
Run the app manually to check:
```bash
python app.py
```
Go to `http://garagepi.local:5000` in your web browser. You should see the dashboard!

---

## Part 4: Auto-Start (Production)

To make the app run automatically when the Pi turns on, create a Systemd service.

1.  **Create Service File**:
    ```bash
    sudo nano /etc/systemd/system/garage.service
    ```

2.  **Paste Configuration**:
    (Adjust paths if your username is not `pi`)
    ```ini
    [Unit]
    Description=Garage Door Automation
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/Garage-Project
    Environment="PATH=/home/pi/Garage-Project/venv/bin"
    ExecStart=/home/pi/Garage-Project/venv/bin/python app.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Enable & Start**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable garage.service
    sudo systemctl start garage.service
    ```

4.  **Check Status**:
    ```bash
    sudo systemctl status garage.service
    ```

---

## Troubleshooting

*   **Door Toggles but Animation doesn't move**: Check your sensor wiring. Is the magnet close enough?
*   **"Mock GPIO" Logs**: If you see this in logs, `RPi.GPIO` failed to load. Make sure you are running on a real Pi.
