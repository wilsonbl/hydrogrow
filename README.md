# Hydrogrow

Hydrogrow is an automated hydroponics system created for ECE Senior Design 2019-20 at Oregon State University

## Frontend

**Web interface for the hydroponic system written in react.**

Displays system information in real time including water, pH, electrical conductivity (EC), and nutrient levels. Also displays any system faults that the system has encountered.

Allows users to input custom watering cycles and the desired pH/EC levels for the system.

Each React component created for the frontend can be found in hydrogrow/frontend/src.

## Backend

**Backend for the web interface created using Express.**

Contains an SQLite database that stores system data and user settings. Communicates with both the frontend and the hardware code.

## Hardware

**Multi-threaded system control software written in Python. Designed to run on the system's Raspberry Pi.**

Walks the user through a WiFi connection setup process.

Periodically reads the backend database to obtain customized user settings for watering cycles and pH/EC levels.

Sends and receives data with base station PCB over UART.

Controls pumps and valves to execute custom watering cycles.

Updates the local display and backend database with sensor, watering, and fault information.

The main hardware code can be found at hydrogrow/hardware/HardwareCode.py

## Node

**Firmware running on the ATmega328p microcontrollers on the nodes.**

Contains run_node.c, which uses UART (uart_functions) to read in a command from the base station PCB.

If asked, it polls water level sensors and sends back the water level values.

If asked, it opens and closes the node's valve.

Compiles and uploads without a bootloader using the Makefile provided.

Requires avrdude and avr-gcc to be installed. 


## Running the code
By default, the Raspberry Pi on the system runs the frontend, backend, and hardware code automatically on boot. Any of these three pieces of software can also be run manually.

To run the frontend or backend code, [node.js](https://nodejs.org/) must be installed.

To run the hardware code, [python3](https://www.python.org/downloads/) must be installed.

### Frontend
1. From the frontend directory, execute ```npm install``` to install all required dependencies.
2. Use ```npm start``` to run the web interface frontend. To view the interface, navigate a web browser to [localhost:3000](localhost:3000) (this webpage should open automatically when you run the command).

### Backend
1. From the backend directory, execute ```npm install``` to install all require dependencies.
2. If you are on Windows, use ```SET PORT=3001 && npm start``` to run the web interface backend. If you are using Linux, this command can be shortened to ```PORT=3001 npm start```. The port is set to 3001 so it doesn't conflict with the frontend code which is running on port 3000.

### Hardware
1. From the hardware directory, execute ```python3 HardwareCode.py```. If any dependencies are not present, please install them with pip and try again.
