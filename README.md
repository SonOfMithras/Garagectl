# Garagectl

**Garagectl** is a simple, DIY smart garage door opener running on a Raspberry Pi Zero 2 W. It provides a web dashboard to monitor and control your garage door from anywhere on your local network.

![Garagectl Dashboard](https://via.placeholder.com/800x400?text=Garagectl+Dashboard+Preview)

## Features
-   **Web Interface**: Clean, responsive dashboard to view status and toggle the door.
-   **Real-Time Monitoring**: Uses a magnetic reed switch to detect if the door is open or closed.
-   **Secure**: Runs locally on your network; no cloud subscription required.
-   **Mock Mode**: Development mode to test the UI on a regular PC without GPIO pins.

---

## 🛒 Hardware Shopping List

You will need the following components. To build this for under $30, buy "Starter Kits" where possible.

### Core Computer
| Component | Recommendation | Logic | Est. Price |
| :--- | :--- | :--- | :--- |
| **SBC** | [**Raspberry Pi Zero 2 W**](https://www.amazon.com/s?k=raspberry+pi+zero+2+w) | Powerful & cheap. Try "Starter Kits" if sold out solo. | $15 (Board) / $45 (Kit) |
| **Micro SD Card** | [**32GB Class 10**](https://www.amazon.com/s?k=sandisk+ultra+32gb+micro+sd) | Required for OS. Use reliable brands (SanDisk/Samsung). | $10 |
| **Power Supply** | [**5V 2.5A Micro USB PSU**](https://www.amazon.com/s?k=5v+2.5a+micro+usb+power+supply) | Official Pi PSU or generic UL-listed 5V 2.5A+. | $12 |

### Interface Hardware
| Component | Recommendation | Why? | Est. Price |
| :--- | :--- | :--- | :--- |
| **Relay Module** | [**5V 1-Channel Relay**](https://www.amazon.com/s?k=5v+1+channel+relay+module+raspberry+pi) | Simulates the button press. Look for "Active Low". | $6 (often 2-pack) |
| **Door Sensor** | [**Magnetic Reed Switch**](https://www.amazon.com/s?k=magnetic+reed+switch+wired+garage+door) | Security alarm style (Wired). Floor-mount types are durable. | $12 - $15 |
| **Wires** | [**Dupont Jumper Wires**](https://www.amazon.com/s?k=dupont+jumper+wires+kit) | Female-to-Female & Male-to-Female for GPIO. | $6 (Kit) |
| **Bell Wire** | [**2-Core Bell Wire**](https://www.amazon.com/s?k=2+core+bell+wire) | To run long distance from opener to sensor. | $10 - $15 |

### Mounting & Misc
| Component | Recommendation |
| :--- | :--- |
| **Case** | [**Raspberry Pi Zero Case**](https://www.amazon.com/s?k=raspberry+pi+zero+case) (Essential for protection) |
| **Mounting Tape** | [**3M Command Strips**](https://www.amazon.com/s?k=3m+command+strips) (No screws needed) |
| **SD Card Reader** | [**USB SD Card Reader**](https://www.amazon.com/s?k=usb+sd+card+reader) (**Required** to flash OS on PC) |

### 🛠️ Tools Required
| Tool | Why? | Alternatives |
| :--- | :--- | :--- |
| **Small Screwdriver** | For Relay terminals. | Eyeglass kit. |
| **Wire Strippers** | To strip bell wire. | Scissors (carefully). |
| **Step Ladder** | To reach opener. | Sturdy chair. |
| **Cable Clips** | To hide wires. | Duct tape. |

> **No Soldering Required**: This project uses screw terminals and plug-in headers.

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
| **Reed Switch** | Wire 1 | Ground | Pin 9 (GND) |
| **Reed Switch** | Wire 2 | GPIO 27 | Pin 13 (GPIO 27) |

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

# 3. Install Dependencies
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Test It
python app.py
```
Visit `http://garagepi.local:5000` to see it working.

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
    Environment="PATH=/home/pi/Garagectl/venv/bin"
    ExecStart=/home/pi/Garagectl/venv/bin/python app.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
3.  Enable: `sudo systemctl enable --now garage.service`

## License
MIT License
