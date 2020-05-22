# Node

## Firmware running on the ATmega328p on the nodes.

Contains run_node.c, which uses UART (uart_functions) to read in a command from the base station PCB.

If asked, it polls water level sensors and sends back the water level values.

If asked, it opens and closes the node's valve.

Compiles and uploads without a bootloader using the Makefile provided.

Requires avr-dude and avr-gcc to be installed. 

## Uploading code to microcontroller

Use a usb-asp programmer and connect its 5V and ground to the 5V and ground on the node PCB.  Connect the reset, MOSI, MISO, and clock ports on the programmer to the corresponding ports on J13 on the node PCB.

Type "make program" into the command line

The firmware should be uploaded to your microcontroller and should begin running when the PCB is connected to 5V and ground.
