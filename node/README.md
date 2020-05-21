# Node

## Firmware running on the ATmega328p on the nodes.

Contains run_node.c, which uses UART (uart_functions) to read in a command from the base station PCB.

If asked, it polls water level sensors and sends back the water level values.

If asked, it opens and closes the node's valve.

Compiles and uploads without a bootloader using the Makefile provided.

Requires avr-dude and avr-gcc to be installed. 
