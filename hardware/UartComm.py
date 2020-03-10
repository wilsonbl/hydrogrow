import RPi.GPIO as GPIO
import serial
import time, sys

UART_SEL = 7
ser = None

def uart_init():
	global ser
	#Using pin numbers rather than GPIO numbers
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(UART_SEL, GPIO.OUT)
	SERIAL_PORT = "/dev/ttyS0"
	ser = serial.Serial(SERIAL_PORT, baudrate = 9600)
	ser.timeout = 7 # Read timeout
	ser.write_timeout = 3 # Write timeout


def uart_comm(value, node_num):
	if node_num == 0:
		GPIO.output(UART_SEL, GPIO.HIGH)
	elif node_num == 1:
		GPIO.output(UART_SEL, GPIO.LOW)
	else:
		print("node_num for UART select must be 0 or 1")
		return None
	
	# Encode the message into binary before sending
	ser.write(value.encode())
	print("Sending" + str(value))

	#if value == 'o' or value == 'c':
	#	sleep(2)

	# Block until a value is read in
	read_value = ser.read()
	ser.reset_input_buffer()

	return read_value

	
