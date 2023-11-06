# IoT Temperature and Color Control System

This GitHub repository contains Python scripts for an IoT temperature control system with a servo motor and a color detection system using a camera. The project involves controlling a servo motor based on temperature readings and detecting colors using computer vision techniques. Both systems integrate with Adafruit IO and Airtable for remote monitoring and control.

## Temperature Control System

### Description

The temperature control system monitors temperature using a thermistor and controls a servo motor based on the temperature. The system communicates the temperature and servo status to Adafruit IO for remote monitoring.

### Requirements

Before running the temperature control system, ensure the following requirements are met:

- Python 3.x
- MicroPython firmware for your target board
- Required MicroPython libraries
- Hardware setup for the servo motor and thermistor
- `mysecrets.py` file with `adafruitKey` and `buttoncode` variables
- `airtablesecrets.py` file with `BASE_ID`, `API_KEY`, `TABLE_ID`, and `RECORD_ID` variables

### Installation and Setup

1. Install the MicroPython firmware on your target board.
2. Copy the Python script for the temperature control system to your board.
3. Ensure that the required libraries and secrets files are correctly set up.
4. Connect the hardware components as specified in your script.

### Usage

1. Run the Python script for the temperature control system on your MicroPython device.
2. The script will initialize the servo motor, read temperature from the thermistor, and set the servo's position accordingly.
3. Temperature and servo status will be published to Adafruit IO.
4. If a gamepad is connected, you can use it to control the servo position manually.

## Color Detection System

### Description

The color detection system uses a camera to detect colors (green and red) in the captured frames. It can differentiate between green and red colors and communicates the detected color to Airtable.

### Requirements

For the color detection system, you need the following:

- Python 3.x
- OpenCV (cv2)
- NumPy
- `airtablesecrets.py` file with `BASE_ID`, `API_KEY`, `TABLE_ID`, and `RECORD_ID` variables
- A camera (usually integrated with your computer)

### Installation and Setup

1. Install Python and the required libraries (OpenCV, NumPy).
2. Copy the Python script for the color detection system to your computer.
3. Ensure that the `airtablesecrets.py` file is correctly populated with your Airtable secrets.
4. Make sure your computer's camera is working.

### Usage

1. Run the Python script for the color detection system on your computer.
2. The script will capture frames from your camera and detect colors (green and red) in the frames.
3. Detected colors will be communicated to Airtable for remote monitoring and control.
4. The color detection process runs continuously as long as the script is running.

## Features

- Real-time temperature monitoring and control with a servo motor.
- Integration with Adafruit IO for remote temperature monitoring and control.
- Manual control of the servo position using a gamepad.
- Continuous color detection and differentiation between green and red colors.
- Communication of detected colors to Airtable for remote monitoring.

Generated using ChatGPT
