# Garagectl

**Garagectl** is a simple, DIY smart garage door opener running on a Raspberry Pi Zero 2 W. It provides a web dashboard to monitor and control your garage door from anywhere on your local network - pair with tailscale for remote access.

##[Garagectl Dashboard]

### Features
-   **Web Interface**: Clean, responsive dashboard to view status and toggle the door.
-   **Multi-Sensor Tracking**: Supports up to 4 sensors to track exact door position (Closed, Ajar, Partially Open, Open).
-   **Enhanced Logging**: Visual log of events with icons, daily archiving, and a built-in archive viewer.
-   **Theming**: Light/Dark mode with monochromatic styling.
-   **Real-Time Monitoring**: Uses magnetic reed switches to detect door state.
-   **Secure**: Runs locally on your network; no cloud subscription required.
-   **Mock Mode**: Development mode to test the UI on a regular PC without GPIO pins.

---

## 🛒 Hardware Shopping List

You will need the following components. To build this for under $100, buy "Starter Kits" where possible.

### Core Computer
| Component | Recommendation | Logic | Est. Price |
| :--- | :--- | :--- | :--- |
| **SBC** | **Raspberry Pi Zero 2 W** | Powerful & cheap. Try "Starter Kits" if sold out solo. | $15 (Board) / $45 (Kit) |
| **Micro SD Card** | **32GB Class 10** | Required for OS. Use reliable brands (SanDisk/Samsung). | $10 |
| **Power Supply** | **5V 2.5A Micro USB PSU** | Official Pi PSU or generic UL-listed 5V 2.5A+. | $12 |

### Interface Hardware
| Component | Recommendation | Why? | Est. Price |
| :--- | :--- | :--- | :--- |
| **Relay Module** | **5V 1-Channel Relay** | Simulates the button press. Look for "Active Low". | $6 (often 2-pack) |
| **Door Sensors** | **4x Magnetic Reed Switches** | For granular position tracking (Closed -> Open). | $12 - $15 |
| **Wires** | **Dupont Jumper Wires** | Female-to-Female & Male-to-Female for GPIO. | $6 (Kit) |
| **Bell Wire** | **2-Core Bell Wire** | To run long distance from opener to sensor. | $10 - $15 |

### Mounting & Misc
| Component | Recommendation |
| :--- | :--- |
| **Case** | **Raspberry Pi Zero Case** (Essential for protection) |
| **Mounting Tape** | **3M Command Strips** (No screws needed) |
| **SD Card Reader** | **USB SD Card Reader** (**Required** to flash OS on PC) |

### 🛠️ Tools Required
| Tool | Why? | Alternatives |
| :--- | :--- | :--- |
| **Small Screwdriver** | For Relay terminals. | Eyeglass kit. |
| **Wire Strippers** | To strip bell wire. | Scissors (carefully). |
| **Step Ladder** | To reach opener. | Sturdy chair. |
| **Cable Clips** | To hide wires. | Duct tape. |

---

## 📖 Complete Build Guide

### Part 1: Hardware Setup

#### 1. Wiring Diagram
**WARNING**: Ensure your Raspberry Pi is unpowered while wiring.

| Component | Pin Name | Connects To | Raspberry Pi Pin (BCM) |
| :--- | :--- | :--- | :--- |
| **Relay** | VCC | 5V Power | Pin 2 or 4 (5V) |
| **Relay** | GND | Ground | Pin 6 (GND) |
| **Relay** | IN (Signal) | GPIO 17 | Pin 11 (GPIO 17) |
| **Sensor 1 (Bottom)** | Wire 1 / 2 | GND / GPIO 27 | Pin 13 (AGND / GPIO 27) |
| **Sensor 2** | Wire 1 / 2 | GND / GPIO 22 | Pin 15 (GPIO 22) |
| **Sensor 3** | Wire 1 / 2 | GND / GPIO 23 | Pin 16 (GPIO 23) |
| **Sensor 4 (Top)** | Wire 1 / 2 | GND / GPIO 24 | Pin 18 (GPIO 24) |


> **Note**: The Reed Switch has no polarity. It doesn't matter which wire goes to where.

#### 2. Physical Installation
1.  **Reed Switch**: Mount the magnet on the door and the wired sensor on the frame (<1 inch gap when closed).
2.  **Relay**: Connect relay "NO" and "COM" terminals to your garage door opener motor (same terminals as the wall button).

### Part 2: Raspberry Pi Setup (OS)
1.  Download **Raspberry Pi Imager**.
2.  Choose OS: **Raspberry Pi OS Lite (64-bit)**.
3.  **Edit Settings** regarding Hostname (`garagepi`), User (`pi`), WiFi, and SSH enabled.
4.  Write to SD card, insert into Pi, and boot.

### Part 3: Software Installation
SSH into your Pi (`ssh pi@garagepi.local`) and run:

```bash
# 1. Update System
sudo apt update && sudo apt upgrade -y

# 2. Get Code
sudo apt install git -y
git clone https://github.com/SonOfMithras/Garagectl.git
cd Garagectl

# 3. Run Installer
chmod +x install.sh
./install.sh

# 4. Test It
./.venv/bin/python app.py
```

Visit `http://localhost:5000` (if running locally) or `http://<your-pi-ip>:5000` to see it working.
> **Note:** If you configured the hostname as `garagepi`, you may be able to access it at `http://garagepi.local:5000` depending on your network.

### Part 4: Auto-Start
To run on boot, create a systemd service:

1.  Create file: `sudo nano /etc/systemd/system/garage.service`
2.  Paste content:
    ```ini
    [Unit]
    Description=Garage Door Automation
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/Garagectl
    Environment="PATH=/home/pi/Garagectl/.venv/bin"
    ExecStart=/home/pi/Garagectl/.venv/bin/python app.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
3.  Enable: `sudo systemctl enable --now garage.service`

## License
MIT License
