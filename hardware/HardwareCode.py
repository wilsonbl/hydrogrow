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
from datetime import datetime, timezone, timedelta
import pytz
import random
import math
import subprocess


#-----------------------------------SETUP-------------------------------------
# Pin assignments
TRIG = 4
ECHO = 17

# Update intervals (seconds)
DB_UPDATE_INTERVAL = 10
DB_READ_INTERVAL = 10
BASE_WATER_UPDATE_INTERVAL = 10

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
node1_water_start = multiprocessing.Array(c_char, 40)
node1_water_hr = multiprocessing.Value('i', 0)
node1_water_min = multiprocessing.Value('i', 0)
node1_watering = multiprocessing.Value('i', 0)
node2_water_start = multiprocessing.Array(c_char, 40)
node2_water_hr = multiprocessing.Value('i', 0)
node2_water_min = multiprocessing.Value('i', 0)
node2_watering = multiprocessing.Value('i', 0)
node1_status = multiprocessing.Value('i', 0)
node2_status = multiprocessing.Value('i', 0)
pump1_status = multiprocessing.Value('i', 0)
pump2_status = multiprocessing.Value('i', 0)
fill_time_limit = multiprocessing.Value('i', 10)

# Pin initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# LCD initialization
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.create_char(0, [0,0,1,1,2,1,7,8])
lcd.create_char(1, [0,24,4,18,9,5,21,9])
lcd.create_char(2, [0,23,8,20,19,8,6,1])
lcd.create_char(3, [0,1,17,17,1,2,4,24])
lcd.create_char(4, [0,4,14,31,31,31,14,0])
lcd.create_char(5, [0,0,27,14,4,14,27,0])
lcd.create_char(6, [0,31,31,31,31,31,31,31])

# Email initialization
port = 465
smtp_server = "smtp.gmail.com"
sender_email = "myhydrogrow@gmail.com" 
receiver_email = "1234blair@gmail.com"
password = "readytogrow"
context = ssl.create_default_context()


#--------------------------------LCD--------------------------------
def local_display(i2c, lcd, state):
    state.value = 0
    while True:
        if state.value == 0:
            #lcd.message = ""
            #lcd.message = "\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\n\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06"
            lcd.message = "BW EC pH       {}\n{:0>2d} {:0>2d} {:0>2d}       {}".format("\x04" if node1_watering.value else "\x05", int(base_water.value), int(ec.value), int(pH.value), "\x04" if node2_watering.value else "\x05")
        elif state.value == 1:
            lcd.message = "N1 N2 N3 N4    {}\n{:0>2d} {:0>2d} {:0>2d} {:0>2d}    {}".format("\x04" if node1_watering.value else "\x05", int(nutrient_1.value), int(nutrient_2.value), int(nutrient_3.value), int(nutrient_4.value), "\x04" if node2_watering.value else "\x05")
        elif state.value == 2:
            lcd.message = "N1 N2 P1 P2    {}\n{:0>2d} {:0>2d} {:0>2d} {:0>2d}    {}".format("\x04" if node1_watering.value else "\x05", int(node1_status.value), int(node2_status.value), int(pump1_status.value), int(pump2_status.value), "\x04" if node2_watering.value else "\x05")
        
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
        elif lcd.left_button:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                print("SENDING EMAIL")
                try:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, "TEST MESSAGE")
                except:
                    print("ERROR")

        time.sleep(0.2)


#-----------------------------------SENSORS-----------------------------------
def read_base_water():
    while True:
        base_water.value = random.randint(0, 99)
        time.sleep(1)
    '''pulseStart = 0

    while True:
        GPIO.output(TRIG, GPIO.LOW)                     #Set TRIG as LOW
        GPIO.output(TRIG, GPIO.HIGH)                    #Set TRIG as HIGH
        time.sleep(0.000001)                            #Delay of 0.00001 seconds
        GPIO.output(TRIG, GPIO.LOW)                     #Set TRIG as LOW

        while GPIO.input(ECHO)==0:               	    #Check if Echo is LOW
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
                base_water.value = distance
        else:
            #print ("Out Of Range")                      #display out of range
            with lock:
                base_water.value = 0

        time.sleep(BASE_WATER_UPDATE_INTERVAL)'''


def read_pH():
    while True:
        pH.value = random.randint(0, 14)
        time.sleep(1)


def read_EC():
    while True:
        ec.value = random.randint(0, 10)
        time.sleep(1)
    

#-----------------------------------WATERING----------------------------------
def fill_tray():
    start_time = time.time()
    while(time.time() - start_time < fill_time_limit.value): #OR UPPER SENSOR TRIGGERED
        print("FILLING TRAY")
        time.sleep(1)

def node1_water_cycle():
    while True:
        if node1_water_start.value.decode("utf-8") != '':
            #Read water cycle datetime and convert to UTC
            node1_datetime = datetime.strptime(node1_water_start.value.decode("utf-8"), '%Y-%m-%dT%H:%M:%S.%fZ')
            node1_datetime = node1_datetime.replace(tzinfo=pytz.UTC, second=0)

            #Calculate the diff between the current datetime and the cycle start datetime in mins
            datetime_diff = datetime.now(timezone.utc) - node1_datetime
            diff_min = datetime_diff.total_seconds()//60
            node1_cycle_min = node1_water_hr.value*60 + node1_water_min.value

            print("NODE 1", diff_min, node1_cycle_min)
            #Start watering if current datetime is a) greater than start datetime and b) a multiple of the cycle time
            if diff_min >= 0 and diff_min % node1_cycle_min == 0:
                print("START NODE 1 WATER CYCLE")
                node1_watering.value = 1
            else:
                print("DON'T START NODE 1 WATER CYCLE")
                node1_watering.value = 0
        time.sleep(1)


def node2_water_cycle():
    while True:
        if node2_water_start.value.decode("utf-8") != '':
            #Read water cycle datetime and convert to UTC
            node2_datetime = datetime.strptime(node2_water_start.value.decode("utf-8"), '%Y-%m-%dT%H:%M:%S.%fZ')
            node2_datetime = node2_datetime.replace(tzinfo=pytz.UTC, second=0)

            #Calculate the diff between the current datetime and the cycle start datetime in mins
            datetime_diff = datetime.now(timezone.utc) - node2_datetime
            diff_min = datetime_diff.total_seconds()//60
            node2_cycle_min = node2_water_hr.value*60 + node2_water_min.value

            print("NODE 2", diff_min, node2_cycle_min)
            #Start watering if current datetime is a) greater than start datetime and b) a multiple of the cycle time
            if diff_min >= 0 and diff_min % node2_cycle_min == 0:
                print("START NODE 2 WATER CYCLE")
                node2_watering.value = 1
            else:
                print("DON'T START NODE 2 WATER CYCLE")
                node2_watering.value = 0
        time.sleep(1)


#-----------------------------------DATABASE----------------------------------
def update_database():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    while True:
        t = int(round(time.time() * 1000))
        print("INSERTING INTO DB: ", t, base_water.value - 0.5)
        curs.execute("INSERT INTO BASE_WATER(time, base_water) VALUES(?, ?)", (t, base_water.value - 0.5))

        conn.commit()
        time.sleep(DB_UPDATE_INTERVAL)


def read_database():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    while True:
        curs.execute("SELECT hr FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_hr.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT min FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_min.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT start FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_start.value = curs.fetchall()[0][0].encode()

        curs.execute("SELECT hr FROM NODE2_WATER_FREQ")
        with lock:
            node2_water_hr.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT min FROM NODE2_WATER_FREQ")
        with lock:
            node2_water_min.value = int(curs.fetchall()[0][0])
        curs.execute("SELECT start FROM NODE2_WATER_FREQ")
        with lock:
            node2_water_start.value = curs.fetchall()[0][0].encode()

        curs.execute("SELECT * FROM SUBSYSTEM_STATUS")
        subsystem_status = curs.fetchall()[0]
        with lock:
            node1_status.value = subsystem_status[0]
            node2_status.value = subsystem_status[1]
            pump1_status.value = subsystem_status[2]
            pump2_status.value = subsystem_status[3]
        
        time.sleep(DB_READ_INTERVAL)

def read_config():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    curs.execute("SELECT fill_time_limit FROM CONFIG")
    fill_time_limit.value = int(curs.fetchall()[0][0])

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


def test_nodes():
    #Send x messages. If no response throw node error
    print("TESTING NODES")
    time.sleep(5)
    return False

def test_valves():
    #Send x valve open commands. If error, throw node valve fail error
    print("TESTING VALVES")
    time.sleep(5)
    return False

def test_pumps():
    #Turn main pump on and check output flow sensor. If flowrate = 0, throw pump error. If flowrate <= 0.5*(avg_flowrate), throw clog/leak error
    print("TESTING PUMPS")
    time.sleep(5)
    return False

def test_trays():
    #Meant to be run after test_pumps (or whenever you're expecting water to be in a node).
    #Check node tray bottom sensors. If any == 0, throw clog/leak error
    print("TESTING TRAYS")
    time.sleep(5)
    return False

def test_pH():
    #Send x messages requesting pH info. If error, throw pH error
    print("TESTING pH")
    time.sleep(5)
    return False

def test_EC():
    #Send x messages requesting EC info. If error, throw EC error.
    print("TESTING EC")
    time.sleep(5)
    return False

def startup_diagnostics():
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
        test_nodes()
        test_valves()
        print("MAIN PUMP VALVE OPEN")
        print("NODE VALVE OPEN")
        print("MAIN PUMP ON")
        print("FILLING TRAYS")
        time.sleep(15)
        test_trays()
        fill_tray()
        print("MAIN PUMP VALVE CLOSE")
        print("MAIN PUMP OFF")


#-----------------------------------CLEANUP-----------------------------------
#@atexit.register
def cleanup():
    lcd.clear()
    #conn.close()
    #GPIO.cleanup()
    print("See ya later! :D")


#-------------------------------------MAIN-------------------------------------
def main():
    setup_wifi()
    startup_diagnostics()

    # Display startup message
    lcd.message = '\x00\x01  READY TO  \x00\x01\n\x02\x03    GROW    \x02\x03'
    time.sleep(2)
    lcd.clear()
    
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
