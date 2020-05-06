import RPi.GPIO as GPIO
import serial
import time, sys

# Initializing the UART port for the Raspberry Pi
def uart_init(pin):
    SERIAL_PORT = "/dev/ttyS0"
    ser = serial.Serial(SERIAL_PORT, baudrate = 9600)
    ser.timeout = 7 # Read timeout
    ser.write_timeout = 3 # Write timeout
    return ser

# Send a value through UART and receive a value through UART from the node
def uart_send_rec(value, ser):
    # Encode the message into binary before sending
    ser.write(value.encode())
    print("Sending " + value)

    if value == 'o' or value == 'c':
            time.sleep(2)

    # Block until a value is read in
    read_value = ser.read()
    ser.reset_input_buffer()

    return read_value

# Begin communication with the node microcontroller via UART
def uart_comm(value, node_num, ser, UART_SEL):
    # Select with node you want to communicate with using the UART select
    if node_num == 0:
        GPIO.output(UART_SEL, GPIO.HIGH)
    elif node_num == 1:
        GPIO.output(UART_SEL, GPIO.LOW)
    else:
        print("node_num for UART select must be 0 or 1")
        return None

    # Try communicating with the node a few times to make sure that there wasn't
    # a misreading (this UART doesn't do parity checking)
    returned_values = []
    for _ in range(2):
        returned_values.append(uart_send_rec(value, ser))

        # Make sure all returned values are equal
        if returned_values[1:] == returned_values[:-1]:
            return returned_values[0]
        else:
            return 'f'



