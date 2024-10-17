# MagiQuestHomeAutomation



# OLD

MagiQuest IR Signal Decoder

This project decodes MagiQuest wand signals using an IR receiver connected to a Raspberry Pi. The code is written in Python, and it utilizes the pigpio library for precise timing and signal processing.

Table of Contents

Prerequisites
Hardware Setup
Software Setup
Running the Decoder
Adjusting Parameters
Troubleshooting
License
Prerequisites

A Raspberry Pi with GPIO pins.
An IR receiver module (e.g., TSOP38238, TSOP4838, or any 38 kHz IR receiver).
Python 3.7 or higher.
pigpio library for Raspberry Pi.
Hardware Setup

Connect the IR Receiver to the Raspberry Pi:
VCC (pin 1) of the IR receiver goes to 5V on the Raspberry Pi.
GND (pin 3) of the IR receiver goes to GND on the Raspberry Pi.
OUT (pin 2) of the IR receiver goes to GPIO 14 (pin 8) on the Raspberry Pi.
Ensure proper wiring as the pins may vary depending on your specific IR receiver module.

(Replace with a wiring diagram image)
Software Setup

Install pigpio:
The pigpio library is used to read the IR pulses from the GPIO pin.

First, install pigpio:

bash
Copy code
sudo apt update
sudo apt install pigpio python3-pigpio
Enable pigpio daemon:
The pigpio daemon (pigpiod) must be running for the code to work. Start the daemon with the following command:

bash
Copy code
sudo pigpiod
You can also enable it to start automatically at boot:

bash
Copy code
sudo systemctl enable pigpiod
Clone or Download the Project:
bash
Copy code
git clone https://github.com/yourusername/magiquest-ir-decoder.git
cd magiquest-ir-decoder
Install Python Dependencies:
The script doesn’t have any external Python dependencies beyond the pigpio library. Ensure you have the following installed:

bash
Copy code
sudo apt install python3-pigpio
If you are using a virtual environment, activate it and install pigpio:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
pip install pigpio
Running the Decoder

To run the MagiQuest IR signal decoder:

Ensure the pigpio daemon is running:
bash
Copy code
sudo pigpiod
Run the magiquest_decoder.py script:
bash
Copy code
python3 magiquest_decoder.py
The script will listen for signals from the MagiQuest wand, decode them, and print both the raw magnitude value and a human-readable magnitude to the console.

Example output:

yaml
Copy code
Signal ended. Decoding pulses.
Raw magnitude: 0x00c8 (200)
Human-readable magnitude: 3
Decoded wand_id: 0x12345678, magnitude: 0x00c8 (human-readable: 3)
Adjusting Parameters

The script is tuned for the MagiQuest IR protocol. If you find that the script is not detecting signals correctly, you can adjust the following parameters in the code:

TOLERANCE: This is set to ±150 microseconds. If signals are slightly off, you can increase this value for more leniency in pulse timing.
PULSE_THRESHOLD: This is set to 100000 microseconds (100 ms) to filter out very large pulses (noise). You can adjust this based on your signal environment.
IR_PIN: This is set to GPIO 14 (pin 8 on the Pi). If you are using a different GPIO pin, update this variable in the script.
Troubleshooting

pigpio not running: Ensure that the pigpiod daemon is running by executing sudo pigpiod. You can check if it’s running with the command sudo systemctl status pigpiod.
Signal not being detected: Ensure your IR receiver is properly connected and that the correct GPIO pin is specified in the code (IR_PIN). Additionally, try increasing the TOLERANCE value if the timing is slightly off.
Permission errors: You might need to run the script with sudo if you encounter permission errors when accessing the GPIO.
