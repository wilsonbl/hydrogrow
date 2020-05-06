import RPi.GPIO as GPIO
import time
import sqlite3
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import atexit
import multiprocessing
from ctypes import c_char
import smtplib
import ssl
from datetime import datetime, timezone
import pytz
import random
import subprocess
from UartComm import uart_init, uart_comm
from bitstring import BitArray



#-----------------------------------SETUP-------------------------------------
# Pin assignments
PIN_MAP = {
    3: 2,
    5: 3,
    7: 4,
    8: 14,
    10: 15,
    11: 17,
    12: 18,
    13: 27,
    15: 22,
    16: 23,
    18: 24,
    19: 10,
    21: 9,
    22: 25,
    23: 11,
    24: 8,
    26: 7,
    29: 5,
    31: 6,
    32: 12,
    33: 13,
    35: 19,
    36: 16,
    37: 26,
    38: 20,
    40: 21
}

# Pin numbers must be mapped to GPIO numbers due to GPIO.setmode(GPIO.BCM)
TRIG = PIN_MAP[19]
ECHO = PIN_MAP[21]
ULTRASONIC_SELECT_0 = PIN_MAP[11]
ULTRASONIC_SELECT_1 = PIN_MAP[13]
ULTRASONIC_SELECT_2 = PIN_MAP[15]
PUMP_SELECT_0 = PIN_MAP[36]
PUMP_SELECT_1 = PIN_MAP[38]
PUMP_SELECT_2 = PIN_MAP[40]
PUMP_CIRCULATION = PIN_MAP[32]
PUMP_SIGNAL = PIN_MAP[22]
FLOW_0 = PIN_MAP[33]
FLOW_1 = PIN_MAP[35]
UART_SELECT = PIN_MAP[7]
VALVE_1_HB1 = PIN_MAP[31]
VALVE_1_HB2 = PIN_MAP[29]
VALVE_2_HB1 = PIN_MAP[26]
VALVE_2_HB2 = PIN_MAP[24]
FLOW_0 = PIN_MAP[33]
FLOW_1 = PIN_MAP[35]
POWER_DOWN = PIN_MAP[23]

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ULTRASONIC_SELECT_0, GPIO.OUT)
GPIO.setup(ULTRASONIC_SELECT_1, GPIO.OUT)
GPIO.setup(ULTRASONIC_SELECT_2, GPIO.OUT)
GPIO.setup(PUMP_SELECT_0, GPIO.OUT)
GPIO.setup(PUMP_SELECT_1, GPIO.OUT)
GPIO.setup(PUMP_SELECT_2, GPIO.OUT)
GPIO.setup(PUMP_CIRCULATION, GPIO.OUT)
GPIO.setup(PUMP_SIGNAL, GPIO.OUT)
GPIO.setup(FLOW_0, GPIO.IN)
GPIO.setup(FLOW_1, GPIO.IN)
GPIO.setup(UART_SELECT, GPIO.OUT)
GPIO.setup(VALVE_1_HB1, GPIO.OUT)
GPIO.setup(VALVE_1_HB2, GPIO.OUT)
GPIO.setup(VALVE_2_HB1, GPIO.OUT)
GPIO.setup(VALVE_2_HB2, GPIO.OUT)
GPIO.setup(POWER_DOWN, GPIO.IN)

GPIO.output(ULTRASONIC_SELECT_0, GPIO.LOW)
GPIO.output(ULTRASONIC_SELECT_1, GPIO.LOW)
GPIO.output(ULTRASONIC_SELECT_2, GPIO.LOW)
GPIO.output(PUMP_SELECT_0, GPIO.HIGH)
GPIO.output(PUMP_SELECT_1, GPIO.HIGH)
GPIO.output(PUMP_SELECT_2, GPIO.HIGH)
GPIO.output(PUMP_SIGNAL, GPIO.HIGH)
GPIO.output(VALVE_2_HB1, GPIO.HIGH)
GPIO.output(VALVE_2_HB2, GPIO.LOW)

#UART initialization
ser = uart_init(UART_SELECT)

# Update intervals (seconds)
DB_UPDATE_INTERVAL = 10
DB_READ_INTERVAL = 10
BASE_WATER_UPDATE_INTERVAL = 10
FILL_TIME_LIMIT = 20

# Share memory between processes
lock = multiprocessing.Lock()
state = multiprocessing.Value('i', 0)
base_water = multiprocessing.Value('d', 0.0)
ec = multiprocessing.Value('d', 0.0)
pH = multiprocessing.Value('d', 0.0)
nutrient_1 = multiprocessing.Value('d', 0.0)
nutrient_2 = multiprocessing.Value('d', 0.0)
nutrient_3 = multiprocessing.Value('d', 0.0)
nutrient_4 = multiprocessing.Value('d', 0.0)
nutrient_5 = multiprocessing.Value('d', 0.0)
node1_water_start = multiprocessing.Array(c_char, 40)
node1_water_hr = multiprocessing.Value('i', 0)
node1_water_min = multiprocessing.Value('i', 0)
node1_watering = multiprocessing.Value('i', 0)
node2_water_start = multiprocessing.Array(c_char, 40)
node2_water_hr = multiprocessing.Value('i', 0)
node2_water_min = multiprocessing.Value('i', 0)
node2_watering = multiprocessing.Value('i', 0)
node1_status = multiprocessing.Value('i', 0)
pump1_status = multiprocessing.Value('i', 0)
valve1_status = multiprocessing.Value('i', 0)
leak1_status = multiprocessing.Value('i', 0)
node2_status = multiprocessing.Value('i', 0)
pump2_status = multiprocessing.Value('i', 0)
valve2_status = multiprocessing.Value('i', 0)
leak2_status = multiprocessing.Value('i', 0)
pH_status = multiprocessing.Value('i', 0)
EC_status = multiprocessing.Value('i', 0)
node1_num_trays = multiprocessing.Value('i', 0)
node2_num_trays = multiprocessing.Value('i', 0)

#LCD initialization
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.create_char(0, [0,0,1,1,2,1,7,8])       # OK 1
lcd.create_char(1, [0,24,4,18,9,5,21,9])    # OK 2
lcd.create_char(2, [0,23,8,20,19,8,6,1])    # OK 3
lcd.create_char(3, [0,1,17,17,1,2,4,24])    # OK 4
lcd.create_char(4, [0,4,14,31,31,31,14,0])  # Water Drop
lcd.create_char(5, [0,0,27,14,4,14,27,0])   # X
lcd.create_char(6, [0,0,1,3,22,28,8,0])     # Check

# Email initialization
port = 465
smtp_server = "smtp.gmail.com"
sender_email = "hydrogrowalerts@gmail.com"
receiver_email = "1234blair@gmail.com"
password = "readytogrow"
context = ssl.create_default_context()

def send_email(error_message):
       with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            print("SENDING EMAIL")
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, error_message)
            except smtplib.SMTPException as error:
                print("ERROR:", error)



#--------------------------------LCD--------------------------------
def local_display(i2c, lcd, state):
    state.value = 0
    while True:
        if state.value == 0:
            lcd.message = "BW   EC   pH   {}\n{:0>2d}%  {:.1f}  {:.1f}  {}".format("\x04" if node1_watering.value else "\x05", int(base_water.value), float(ec.value), float(pH.value), "\x04" if node2_watering.value else "\x05")
        elif state.value == 1:
            lcd.message = "N1 N2 N3 N4 N5 {}\n{:0>2d} {:0>2d} {:0>2d} {:0>2d} {:0>2d} {}".format("\x04" if node1_watering.value else "\x05", int(nutrient_1.value), int(nutrient_2.value), int(nutrient_3.value), int(nutrient_4.value),  int(nutrient_5.value), "\x04" if node2_watering.value else "\x05")
        elif state.value == 2:
            lcd.message = "CPVL CPVL pE   {}\n{}{}{}{} {}{}{}{} {}{}   {}".format("\x04" if node1_watering.value else "\x05", "\x06" if node1_status.value else "\x05", "\x06" if pump1_status.value else "\x05", "\x06" if valve1_status.value else "\x05", "\x06" if leak1_status.value else "\x05", "\x06" if node2_status.value else "\x05", "\x06" if pump2_status.value else "\x05", "\x06" if valve2_status.value else "\x05", "\x06" if leak2_status.value else "\x05", "\x06" if pH_status.value else "\x05", "\x06" if EC_status.value else "\x05", "\x04" if node2_watering.value else "\x05")
        time.sleep(0.2)


def local_buttons(i2c, lcd, state):
    state.value = 0
    while True:
        if lcd.up_button:
            if state.value == 2:
                with lock:
                    state.value = 0
            else:
                with lock:
                    state.value += 1
        elif lcd.down_button:
            if state.value == 0:
                with lock:
                    state.value = 2
            else:
                with lock:
                    state.value -= 1
        elif lcd.right_button:
            power_down()

        time.sleep(0.2)



#-----------------------------------SENSORS-----------------------------------

# Read the ultrasonic sensor for determining the water left in the reservoir
def read_base_water():
    pulseStart = 0

    while True:
        # Pulse the trigger signal to begin reading
        GPIO.output(TRIG, GPIO.LOW)                     #Set TRIG as LOW
        GPIO.output(TRIG, GPIO.HIGH)                    #Set TRIG as HIGH
        time.sleep(0.000001)                            #Delay of 0.00001 seconds
        GPIO.output(TRIG, GPIO.LOW)                     #Set TRIG as LOW

        # Waiting for the echo response so we can time it
        while GPIO.input(ECHO)==0:                      #Check if Echo is LOW
            pulseStart = time.time()                    #Time of the last  LOW pulse

        while GPIO.input(ECHO)==1:                      #Check whether Echo is HIGH
            pulseEnd = time.time()                      #Time of the last HIGH pulse

        pulseDuration = pulseEnd - pulseStart           #pulse duration to a variable
        distance = pulseDuration * 17150                #Calculate distance
        distance = round(distance, 2)                   #Round to two decimal points

        #if distance > 20 and distance < 400:            #Is distance within range
        if distance < 400:
            #print ("Distance:",distance - 0.5,"cm")     #Distance with calibration
            with lock:
                base_water.value = int((((30 - distance) / 30) * 100) - 0.5)
                #print("BASE WATER:", base_water.value)
        else:
            #print ("Out Of Range")                      #display out of range
            with lock:
                base_water.value = 0

        time.sleep(BASE_WATER_UPDATE_INTERVAL)

# Read the pH of the reservoir using the ADC
def read_pH():
    # Not complete - output dummy values
    ph_values = [6, 6.5, 6.5, 6.5, 6.4, 6.2, 6.3, 6.2, 6.2, 6.3, 6.3, 6.2, 6.4, 6.4]
    while True:
        for x in ph_values:
            pH.value = x
            time.sleep(10)


# Read the electrical conductivity of the reservoir using the ADC
def read_EC():
    # Not complete - output dummy values
    ec_values = [2, 2.2, 2.2, 2.1, 2.3, 2.3, 2.2, 2.1, 1.9, 2.1, 2.1]
    while True:
        for x in ec_values:
            ec.value = x
            time.sleep(10)

# Read the flow sensor to determine whether water is flowing through the tubes
def read_flow():
    state = 0
    timer = 0

    while timer < 5:
        # If water is flowing, input FLOW_0 should toggle multiple times
        # Using a state machine to determine if it is toggling
        flow_input = GPIO.input(FLOW_0)
        if state % 2 == 0 and flow_input == 0:
            state += 1
        elif state % 2 == 1 and flow_input == 1:
            state += 1

        if state == 4:
            print("WATER FLOWING")
            return True

        time.sleep(0.01)
        timer += 0.01

    print("WATER NOT FLOWING")
    return False


# Determines if the trays are done filling up with water (at least one tray in the
# node has reached the top/bottom  water level sensor)
def trays_filled(node, read_value, level):
    # Reverse read_value (indexing starts on opposite end)
    read_value = read_value[::-1]

    # Use the value from the web interface to see how many trays the user has
    # connected to the node
    if node == 0:
        num_trays = node1_num_trays.value
    elif node == 1:
        num_trays = node2_num_trays.value

    # All of the top water level sensors have an odd index
    # All of the bottom water level sensors have an even index
    if level == 'top':
        start = 1
        end = num_trays * 2
    elif level == 'bottom':
        start = 0
        end = (num_trays * 2) - 1

    print("Start:", start)
    print("End:", end)
    print(read_value)

    # If any of the trays are filled, say the entire node is done filling
    for i in range(start, end, 2):
        if int(read_value[i]) == 1:
            print("NODE " + str(node) + " TRAY FILLED")
            return True

    print("NODE " + str(node) + " TRAY NOT FILLED")
    return False



#-----------------------------------WATERING----------------------------------

# Turn on and off all the pumps connected to the mux (water and nutrient pumps)
def toggle_pump(pump, enable):
    if pump == 0:
        print("TOGGLING RES_TO_TRAY PUMP: " + str(enable))
        #Res to tray
        GPIO.output(PUMP_SELECT_0, GPIO.LOW)
        GPIO.output(PUMP_SELECT_1, GPIO.LOW)
        GPIO.output(PUMP_SELECT_2, GPIO.LOW)
    elif pump == 1:
        print("TOGGLING TRAY_TO_RES PUMP: " + str(enable))
        #Tray to res
        GPIO.output(PUMP_SELECT_0, GPIO.HIGH)
        GPIO.output(PUMP_SELECT_1, GPIO.LOW)
        GPIO.output(PUMP_SELECT_2, GPIO.LOW)
    elif pump == 2:
        print("TOGGLING NUTRIENT 0 PUMP: " + str(enable))
        #Nutrient 0
        GPIO.output(PUMP_SELECT_0, GPIO.LOW)
        GPIO.output(PUMP_SELECT_1, GPIO.HIGH)
        GPIO.output(PUMP_SELECT_2, GPIO.LOW)
    elif pump == 3:
        print("TOGGLING NUTRIENT 1 PUMP: " + str(enable))
        #Nutrient 1
        GPIO.output(PUMP_SELECT_0, GPIO.HIGH)
        GPIO.output(PUMP_SELECT_1, GPIO.HIGH)
        GPIO.output(PUMP_SELECT_2, GPIO.LOW)
    elif pump == 4:
        print("TOGGLING NUTRIENT 2 PUMP: " + str(enable))
        #Nutrient 2
        GPIO.output(PUMP_SELECT_0, GPIO.LOW)
        GPIO.output(PUMP_SELECT_1, GPIO.LOW)
        GPIO.output(PUMP_SELECT_2, GPIO.HIGH)
    elif pump == 5:
        print("TOGGLING NUTRIENT 3 PUMP: " + str(enable))
        #Nutrient 3
        GPIO.output(PUMP_SELECT_0, GPIO.HIGH)
        GPIO.output(PUMP_SELECT_1, GPIO.LOW)
        GPIO.output(PUMP_SELECT_2, GPIO.HIGH)
    elif pump == 6:
        print("TOGGLING NUTRIENT 4 PUMP: " + str(enable))
        #Nutrient 4
        GPIO.output(PUMP_SELECT_0, GPIO.LOW)
        GPIO.output(PUMP_SELECT_1, GPIO.HIGH)
        GPIO.output(PUMP_SELECT_2, GPIO.HIGH)

    if enable:
        GPIO.output(PUMP_SIGNAL, GPIO.HIGH)
    else:
        GPIO.output(PUMP_SIGNAL, GPIO.LOW)

# Turn on and off the pump that circulates the reservoir water
def toggle_circulation_pump(enable):
    print("TOGGLING CIRCULATION PUMP: " + enable)
    if enable:
        GPIO.output(PUMP_CIRCULATION, GPIO.HIGH)
    else:
        GPIO.output(PUMP_CIRCULATION, GPIO.LOW)


# Open/close/brake the valves connected to the base station
def toggle_valve(associated_pump, direction):
    print("TOGGLING " + associated_pump + " VALVE: " + direction)

    if associated_pump == 'res_to_tray':
        valve_hb1 = VALVE_1_HB1
        valve_hb2 = VALVE_1_HB2
    elif associated_pump == 'tray_to_res':
        valve_hb1 = VALVE_2_HB1
        valve_hb2 = VALVE_2_HB2

    if direction == 'open':
        GPIO.output(valve_hb1, GPIO.LOW)
        GPIO.output(valve_hb2, GPIO.HIGH)
    elif direction == 'close':
        GPIO.output(valve_hb1, GPIO.HIGH)
        GPIO.output(valve_hb2, GPIO.LOW)
    elif direction == 'brake':
        GPIO.output(valve_hb1, GPIO.LOW)
        GPIO.output(valve_hb2, GPIO.LOW)


# Open/close/brake the valves connected to the nodes
def toggle_node_valve(direction, node):
    print("TOGGLING NODE " + str(node) + " VALVE: " + str(direction))

    # Send a request to the node microcontroller to toggle the valve
    valve_success = str(uart_comm(direction, node, ser, UART_SELECT).decode())
    print(valve_success)

    # If it failed to open/close, alert the user
    if valve_success == 'f':
        if node == 0:
            valve1_status.value = 0
        elif node == 1:
            valve2_status.value = 0

        send_email("Subject: Hydrogrow Valve Error\n\nAn issue occurred with the valve on node " + str(node) + " at " + str(datetime.now().strftime('%H:%M') + " on " + str(datetime.now().strftime("%m/%d/%Y") + ".\n\nPlease examine the Hydrogrow system.")))
    return valve_success

# Drain all the trays for the given node
def drain_tray(node):
    print("STARTING NODE " + str(node) + " DRAIN")
    toggle_pump(0, False)

    toggle_valve('res_to_tray', 'close')
    time.sleep(5)
    toggle_valve('res_to_tray', 'brake')

    toggle_node_valve('c', node)

    time.sleep(5) #ADJUST ME WHEN SYSTEM IS BUILT

    # Turn on drain pump and open drain valves until bottom level sensors aren't triggered.
    toggle_valve('tray_to_res', 'open')
    time.sleep(5)
    toggle_valve('tray_to_res', 'brake')

    toggle_node_valve('o', node)

    toggle_pump(1, True)

    # Read the trays' water level sensors
    # Stop pumping once none of the bottom water level sensors are submerged
    read_value = BitArray(uart_comm('w', node, ser, UART_SELECT)).bin
    while trays_filled(node, read_value, 'bottom'):
        read_value = BitArray(uart_comm('w', node, ser, UART_SELECT)).bin
        time.sleep(0.1) #ADJUST ME WHEN SYSTEM IS BUILT

    # Turn off drain pump, close drain valves, and return
    toggle_pump(1, False)

    toggle_valve('tray_to_res', 'close')
    time.sleep(5)
    toggle_valve('tray_to_res', 'brake')

    toggle_node_valve('c', node)

    return

# Pump water to the trays associated with the given node
def fill_tray(node):
    print("STARTING NODE " + str(node) + " FILL")

    # If trays are already full, don't fill them more, so return
    read_value = BitArray(uart_comm('w', node, ser, UART_SELECT)).bin
    print("Top:", read_value)
    if trays_filled(node, read_value, 'top'):
        print("TRAY FULL. STOPPING FILL.")
        drain_tray(node)
        return

    toggle_valve('res_to_tray', 'open')
    time.sleep(5)
    toggle_valve('res_to_tray', 'brake')

    toggle_node_valve('o', node)

    toggle_pump(0, True)
    time.sleep(20) #ADJUST ME WHEN SYSTEM IS BUILT

    # If no water is flowing, throw pump error and return
    if not read_flow():
        if node == 0:
            pump1_status.value = 0
        elif node == 1:
            pump2_status.value = 0
        toggle_pump(0, False)

        send_email("Subject: Hydrogrow Pump Error\n\nAn issue occurred with the pump on node " + str(node) + " at " + str(datetime.now().strftime('%H:%M') + " on " + str(datetime.now().strftime("%m/%d/%Y") + ".\n\nPlease examine the Hydrogrow system.")))
        print("NO WATER FLOWING. PUMP ERROR.")
        return

    # Return if time limit reached
    start_time = time.time()
    while(time.time() - start_time < FILL_TIME_LIMIT):
        # If bottom level sensors aren't triggered, throw leak error, turn off pump, and return
        read_value = BitArray(uart_comm('w', node, ser, UART_SELECT)).bin
        print("Bottom:", read_value)
        if not trays_filled(node, read_value, 'bottom'):
            if node == 0:
                leak1_status.value = 0
            elif node == 1:
                leak2_status.value = 0

            send_email("Subject: Hydrogrow Leak Issue\n\nA leak issue occurred on node " + str(node) + " at " + str(datetime.now().strftime('%H:%M') + " on " + str(datetime.now().strftime("%m/%d/%Y") + ".\n\nPlease examine the Hydrogrow system.")))
            print("BOTTOM LEVEL SENSORS NOT TRIGGERED WHEN WATER SHOULD BE FLOWING. LEAK ERROR.")

            toggle_pump(0, False)
            return

        # If top level sensors are triggered, turn off fill pump and close fill valves.
        read_value = BitArray(uart_comm('w', node, ser, UART_SELECT)).bin
        print("Top:", read_value)
        if trays_filled(node, read_value, 'top'):
            drain_tray(node)
            return

    print("FILL TIMEOUT REACHED.")
    drain_tray(node)
    return


# If it is time to water, display that node 1 is in the middle of a watering cycle on web interface
# Also begin filling the trays
def node1_water_cycle():
    while True:
        if node1_water_start.value.decode("utf-8") != '':
            # Read water cycle datetime and convert to UTC
            node1_datetime = datetime.strptime(node1_water_start.value.decode("utf-8"), '%Y-%m-%dT%H:%M:%S.%fZ')
            node1_datetime = node1_datetime.replace(tzinfo=pytz.UTC, second=0)

            # Calculate the diff between the current datetime and the cycle start datetime in mins
            datetime_diff = datetime.now(timezone.utc) - node1_datetime
            diff_min = datetime_diff.total_seconds()//60
            node1_cycle_min = node1_water_hr.value*60 + node1_water_min.value

            # Start watering if current datetime is a) greater than start datetime and b) a multiple of the cycle time
            if diff_min >= 0 and diff_min % node1_cycle_min == 0:
                if node1_watering.value == 0:
                    print("NODE 1 WATER CYCLE STARTING")
                    node1_watering.value = 1
                    fill_tray(0)
                    node1_watering.value = 0

            else:
                #print("DON'T START NODE 1 WATER CYCLE")
                node1_watering.value = 0
        time.sleep(1)


# Display that node 2 is in the middle of a watering cycle on web interface
def node2_water_cycle():
    while True:
        if node2_water_start.value.decode("utf-8") != '':
            # Read water cycle datetime and convert to UTC
            node2_datetime = datetime.strptime(node2_water_start.value.decode("utf-8"), '%Y-%m-%dT%H:%M:%S.%fZ')
            node2_datetime = node2_datetime.replace(tzinfo=pytz.UTC, second=0)

            # Calculate the diff between the current datetime and the cycle start datetime in mins
            datetime_diff = datetime.now(timezone.utc) - node2_datetime
            diff_min = datetime_diff.total_seconds()//60
            node2_cycle_min = node2_water_hr.value*60 + node2_water_min.value

            # Start watering if current datetime is a) greater than start datetime and b) a multiple of the cycle time
            if diff_min >= 0 and diff_min % node2_cycle_min == 0:
                if node2_watering.value == 0:
                    print("NODE 2 WATER CYCLE STARTING")
                    node2_watering.value = 1
            else:
                #print("DON'T START NODE 2 WATER CYCLE")
                node2_watering.value = 0
        time.sleep(1)



#-----------------------------------DATABASE----------------------------------
def update_database():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    while True:
        t = int(round(time.time() * 1000))
        print("INSERTING INTO DB: ", t, base_water.value)
        curs.execute("INSERT INTO BASE_WATER(time, base_water) VALUES(?, ?)", (t, base_water.value))

        conn.commit()
        time.sleep(DB_UPDATE_INTERVAL)

# Read the watering frequency and nutrient levels provided by the user from the web interface
def read_database():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    while True:
        # Node 1 watering frequency
        curs.execute("SELECT hr FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_hr.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT min FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_min.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT start FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_start.value = curs.fetchall()[0][0].encode()

        # Node 2 watering frequency
        curs.execute("SELECT hr FROM NODE2_WATER_FREQ")
        with lock:
            node2_water_hr.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT min FROM NODE2_WATER_FREQ")
        with lock:
            node2_water_min.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT start FROM NODE2_WATER_FREQ")
        with lock:
            node2_water_start.value = curs.fetchall()[0][0].encode()

        # Nutrient levels
        curs.execute("SELECT N1, N2, N3, N4, N5 FROM NUTRIENTS")
        nutrients = list(curs.fetchall()[0])
        # If nutrient levels == 100, they screw up the formatting on the local display. Round down to 99.
        for i in range(len(nutrients)):
            if nutrients[i] == 100:
                nutrients[i] = 99
        with lock:
            nutrient_1.value = nutrients[0]
            nutrient_2.value = nutrients[1]
            nutrient_3.value = nutrients[2]
            nutrient_4.value = nutrients[3]
            nutrient_5.value = nutrients[4]

        # Subsystem status
        curs.execute("SELECT node1, node2, pump1, pump2, node1Leak, node2Leak, valve1, valve2, pH, EC FROM SUBSYSTEM_STATUS")
        subsystem_status = curs.fetchall()[0]
        with lock:
            node1_status.value = subsystem_status[0]
            node2_status.value = subsystem_status[1]
            pump1_status.value = subsystem_status[2]
            pump2_status.value = subsystem_status[3]
            leak1_status.value = subsystem_status[4]
            leak2_status.value = subsystem_status[5]
            valve1_status.value = subsystem_status[6]
            valve2_status.value = subsystem_status[7]
            pH_status.value = subsystem_status[8]
            EC_status.value = subsystem_status[9]

        time.sleep(DB_READ_INTERVAL)

# Read the system configuration values from the web interface
def read_config():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    curs.execute("SELECT node1_num_trays from CONFIG")
    node1_num_trays.value = int(curs.fetchall()[0][0])

    curs.execute("SELECT node2_num_trays from CONFIG")
    node2_num_trays.value = int(curs.fetchall()[0][0])

    conn.close()



#---------------------------------CALIBRATION---------------------------------
def setup_wifi():
    lcd.message = "SELECT > WiFi\nOTHER > Continue"
    selection = 0
    while selection == 0:
        if lcd.up_button or lcd.down_button or lcd.left_button or lcd.right_button:
            selection = 1
        elif lcd.select_button:
            selection = 2
        time.sleep(0.2)

    if selection == 2:
        lcd.clear()
        lcd.message = "Router WPS > Con\nSELECT > Cancel"
        subprocess.Popen(["wpa_cli", "-i", "wlan0", "wps_pbc"])
        time.sleep(5)

        while True:
            try:
                ps = subprocess.run(['iwgetid', '-r'], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                network = str(ps.stdout)
                if network != "\\n" and network != "":
                    lcd.clear()
                    lcd.message = "Connected to \n" + network
                    time.sleep(2)
                    break
            except subprocess.CalledProcessError:
                print("WPS connection error")

            if lcd.select_button:
                subprocess.Popen(["wpa_cli", "-i", "wlan0", "wps_cancel"])
                break

            time.sleep(0.2)

# Testing if the base station can communicate with the node microcontroller
def test_node(node):
    # Send x messages. If no response throw node error
    print("TESTING NODE", node)
    node_hs = str(uart_comm('h', node, ser, UART_SELECT).decode())
    print(node_hs)

    if node_hs != 'h':
        if node == 0:
            node1_status.value = 0
        elif node == 1:
            node2_status.value = 0

        send_email("Subject: Hydrogrow Node Communication Issue\n\nAn issue occurred when attempting to communicate with node " + str(node) + " at " + str(datetime.now().strftime('%H:%M') + " on " + str(datetime.now().strftime("%m/%d/%Y") + ".\n\nPlease examine the Hydrogrow system.")))


# Startup test of the node and base station valves during the system diagnostics
def test_valve(node):
    # Not done implementing
    # Send x valve close commands. If error, throw node valve fail error
    print("TESTING VALVE", node)
    toggle_node_valve('c', node)


# Startup test of the reservoir to tray and tray to reservoir pumps  during the system diagnostics
def test_pumps():
    # Not done implementing
    # Turn main pump on and check output flow sensor. If flowrate = 0, throw pump error.p If flowrate <= 0.5*(avg_flowrate), throw clog/leak error
    print("TESTING PUMPS")
    toggle_pump(0, True)
    time.sleep(5) #ADJUST WHEN SYSTEM IS BUILT

    return False


# Startup test of the tray water levels during the system diagnostics
def test_trays():
    # Not done implementing
    # Meant to be run after test_pumps (or whenever you're expecting water to be in a node).
    # Check node tray bottom sensors. If any == 0, throw clog/leak error
    print("TESTING TRAYS")
    time.sleep(5)
    return False


# Startup test of the pH sensor during the system diagnostics
def test_pH():
    # Not done implementing
    # Send x messages requesting pH info. If error, throw pH error
    print("TESTING pH")
    time.sleep(5)
    return False


# Startup test of the electrical conductivity sensor during the system diagnostics
def test_EC():
    # Not done implementing
    # Send x messages requesting EC info. If error, throw EC error.
    print("TESTING EC")
    time.sleep(5)
    return False

# Running the diagnostics test to ensure the system is hooked up and working properly
def startup_diagnostics():
    # Not done implementing
    lcd.clear()
    lcd.message = "SELECT > Diags\nOTHER > Continue"
    selection = 0
    while selection == 0:
        if lcd.up_button or lcd.down_button or lcd.left_button or lcd.right_button:
            selection = 1
        elif lcd.select_button:
            selection = 2
        time.sleep(0.2)

    if selection == 2:
        read_config()
        test_node(0)
        test_node(1)
        test_valve(0)
        test_valve(1)
        print("MAIN PUMP VALVE OPEN")
        print("NODE VALVE OPEN")
        print("MAIN PUMP ON")
        print("FILLING TRAYS")
        time.sleep(15)
        test_trays()
        fill_tray()
        print("MAIN PUMP VALVE CLOSE")
        print("MAIN PUMP OFF")

# Configuring the pumps to off and the valves to close
def startup_config():
    toggle_pump(0, False)
    toggle_pump(1, False)
    toggle_node_valve('c', 0)
    toggle_valve('res_to_tray', 'close')
    time.sleep(5)
    toggle_valve('res_to_tray', 'brake')
    toggle_valve('tray_to_res', 'close')
    time.sleep(5)
    toggle_valve('tray_to_res', 'brake')



#-------------------------------------MAIN-------------------------------------
# Safely shut down the Raspberry Pi while in headless mode
def power_down():
    # Not done: implementing power down with a button press
    #while True:
        #if GPIO.input(POWER_DOWN):
    print("STOPPING PROGRAM")
    lcd.clear()
    GPIO.cleanup()
    subprocess.run(['shutdown', '0'], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exit()

    time.sleep(0.1)


def main():
    read_config()
    #fill_tray(0)
    #startup_config()

    #setup_wifi()
    #startup_diagnostics()


    # Display startup message
    lcd.message = '\x00\x01  READY TO  \x00\x01\n\x02\x03    GROW    \x02\x03'
    time.sleep(2)
    lcd.clear()

    #test_node(0)



    '''
    toggle_valve('res_to_tray', 'close')
    time.sleep(5)
    toggle_valve('res_to_tray', 'brake')

    toggle_node_valve('c', 0, ser)
    fill_tray(0)
    print(BitArray(uart_comm('w', 0, ser, UART_SELECT)).bin)
    '''


    try:
        display_process = multiprocessing.Process(target=local_display, args=(i2c, lcd, state))
        button_process = multiprocessing.Process(target=local_buttons, args=(i2c, lcd, state))
        base_water_process = multiprocessing.Process(target=read_base_water)
        pH_process = multiprocessing.Process(target=read_pH)
        EC_process = multiprocessing.Process(target=read_EC)
        update_database_process = multiprocessing.Process(target=update_database)
        read_database_process = multiprocessing.Process(target=read_database)
        node1_water_cycle_process = multiprocessing.Process(target=node1_water_cycle)
        node2_water_cycle_process = multiprocessing.Process(target=node2_water_cycle)

        button_process.start()
        display_process.start()
        base_water_process.start()
        pH_process.start()
        EC_process.start()
        update_database_process.start()
        read_database_process.start()
        node1_water_cycle_process.start()
        node2_water_cycle_process.start()

    except:
        print("Unable to start processes")




main()
