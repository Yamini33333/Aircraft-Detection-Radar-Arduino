# Aircraft Detection & Radar System using Arduino

## Overview

An Arduino-based radar system developed for aircraft and obstacle detection using two ultrasonic sensors. The sensor data is transmitted to a computer through serial communication and visualized using a Python Tkinter GUI.

## Features

- Two ultrasonic sensors for distance measurement
- Real-time aircraft and obstacle detection
- Arduino-based sensor data acquisition
- Serial communication between Arduino and computer
- Python Tkinter-based radar visualization
- Real-time display of Sensor 1 and Sensor 2 distances

## Working

1. Two ultrasonic sensors measure the distance of objects.
2. Arduino processes the sensor readings.
3. Distance values are transmitted to the computer through serial communication.
4. Python receives the sensor data.
5. The Tkinter GUI displays the sensor readings in real time.
6. The system indicates object detection based on the sensor readings.

## Technologies Used

- Arduino Uno
- Ultrasonic Sensors
- C/C++ (Arduino)
- Python
- Tkinter
- Serial Communication

## Project Structure

```text
Aircraft-Detection-Radar-Arduino
├── arduino
│   └── radar_system.ino
├── python
│   └── radar_gui.py
├── README.md
└── LICENSE
