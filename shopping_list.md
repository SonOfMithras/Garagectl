# Hardware Shopping List

To build the Garage Door Automation project, you will need the following components. I have assumed you have "nothing other than a screwdriver and this PC", so I have included essentials like the computer board and wires.

## Core Computer
| Component | Recommendation | Logic | Est. Price |
| :--- | :--- | :--- | :--- |
| **Single Board Computer (SBC)** | [**Raspberry Pi Zero 2 W**](https://www.amazon.com/s?k=raspberry+pi+zero+2+w) | Powerful & cheap. **Note**: Hard to find solo; try "Starter Kits" or Adafruit. | $15 (Board) / $45 (Kit) |
| **Micro SD Card** | [**32GB Class 10** (SanDisk Ultra)](https://www.amazon.com/s?k=sandisk+ultra+32gb+micro+sd) | Required for OS. Use reliable brands (SanDisk/Samsung). | $10 |
| **Power Supply** | [**5V 2.5A Micro USB PSU**](https://www.amazon.com/s?k=5v+2.5a+micro+usb+power+supply) | Official Pi PSU or generic UL-listed 5V 2.5A+ MicroUSB. | $12 |

## Interface Hardware
| Component | Recommendation | Logic | Est. Price |
| :--- | :--- | :--- | :--- |
| **Relay Module** | [**5V 1-Channel Relay**](https://www.amazon.com/s?k=5v+1+channel+relay+module+raspberry+pi) | Simulates the button press. Look for "Active Low" or standard Arduino/Pi relays. | $6 (often 2-pack) |
| **Door Sensor** | [**Magnetic Reed Switch (Wired)**](https://www.amazon.com/s?k=magnetic+reed+switch+wired+garage+door) | Security alarm style. "Overhead Door" floor-mount types are durable for garages. | $12 - $15 |
| **Connecting Wires** | [**Dupont Jumper Wires**](https://www.amazon.com/s?k=dupont+jumper+wires+kit) | Female-to-Female & Male-to-Female for GPIO connections. | $6 (Kit) |
| **Wire for Run** | [**2-Core Bell/Thermostat Wire**](https://www.amazon.com/s?k=2+core+bell+wire) | To run the long distance from the opener to the door sensor. | $10 - $15 |

## Mounting & Misc
| Component | Recommendation | Logic | Est. Price |
| :--- | :--- | :--- | :--- |
| **Case** | [**Raspberry Pi Zero Case**](https://www.amazon.com/s?k=raspberry+pi+zero+case) | Essential for protection. included in most Starter Kits. | $8 |
| **Mounting Tape** | [**3M Command Strips**](https://www.amazon.com/s?k=3m+command+strips) | For sticking sensors/relay to the opener/door without screws. | $5 |
| **USB OTG Adapter** | [**Micro-USB to USB-A**](https://www.amazon.com/s?k=micro+usb+to+usb+adapter) | For connecting a keyboard setup. Included in most kits. | $5 |
| **SD Card Reader** | [**USB SD Card Reader**](https://www.amazon.com/s?k=usb+sd+card+reader) | **REQUIRED** if your PC doesn't have a slot. Used to flash the OS. | $6 - $10 |

## "Nice to Have" Extras
-   **DHT22 Sensor**: If you want to log the temperature/humidity in the garage.
-   **Breadboard**: For prototyping on your desk before installing.

## Tools Required
| Tool | Why? | Alternatives |
| :--- | :--- | :--- |
| **Small Screwdriver Set** | For the Relay terminals and Pi case screws. | Eyeglass kit or a small knife (carefully). |
| **Wire Strippers / Cutters** | To strip the plastic off the ends of the wires. | Scissors (be careful not to cut the copper). |
| **Step Ladder** | To reach your garage door opener. | A sturdy chair. |
| **Electrical Tape** | To secure connections and prevent shorts. | Masking tape (temporary). |
| **Cable Clips / Staples** | To maximize WAF (Wife Acceptance Factor) by hiding wires. | Duct tape (ugly but works). |

> [!NOTE]
> **No Soldering Required**: This project uses screw terminals (on the relay) and "Dupont" header wires (for the Pi), so no soldering is needed if you buy the recommended headers/wires.

> [!TIP]
> **Starter Kits**: You can often find "Raspberry Pi Zero W Starter Kits" that include the Pi, Case, PSU, SD Card, and headers. You would then just need to add the Relay and Reed Switch to your cart.
