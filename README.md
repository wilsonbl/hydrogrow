# Hydrogrow

Hydrogrow is an automated hydroponics system created for ECE Senior Design 2019-20 at Oregon State University

## Frontend

Web interface for the hydroponic system written in react.

Displays system information in real time including water, pH, electrical conductivity (EC), and nutrient levels. Also displays any system faults that the system has encountered.

Allows users to input custom watering cycles and the desired pH/EC levels for the system.

Each React component created for the frontend can be found in hydrogrow/frontend/src.

## Backend

Backend for the web interface created using Express.

Contains an SQLite database that stores system data and user settings. Communicates with both the frontend and the hardware code.

## Hardware

Multi-threaded system control software written in Python. Designed to run on the system's Raspberry Pi.

Walks the user through a WiFi connection setup process.

Periodically reads the backend database to obtain customized user settings for watering cycles and pH/EC levels.

Sends and receives data with base station PCB over UART.

Controls pumps and valves to execute custom watering cycles.

Updates the local display and backend database with sensor, watering, and fault information.

The main hardware code can be found at hydrogrow/hardware/HardwareCode.py
