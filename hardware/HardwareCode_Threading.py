import RPi.GPIO as GPIO
import time
import sqlite3
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import atexit
from threading import Thread, Lock, Event
import smtplib
import ssl
from datetime import datetime


#-----------------------------------SETUP-------------------------------------
# Pin assignments
TRIG = 4
ECHO = 17

# Update intervals (seconds)
DB_UPDATE_INTERVAL = 10
DB_READ_INTERVAL = 10
BASE_WATER_UPDATE_INTERVAL = 10
'''
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
node1_water_start = multiprocessing.sharedctypes.Array(ctypes.c_wchar, 40)
'''
lock = Lock()
state = 0
base_water = 0
ec = 0
pH = 0
nutrient_1 = 0
nutrient_2 = 0
nutrient_3 = 0
nutrient_4 = 0



# Pin initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# LCD initialization
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# Email initialization
port = 465
smtp_server = "smtp.gmail.com"
sender_email = "myhydrogrow@gmail.com" 
receiver_email = "1234blair@gmail.com"
password = "readytogrow"
context = ssl.create_default_context()


#--------------------------------LCD--------------------------------
def local_display(i2c, lcd):
    global state
    global base_water
    global ec
    global pH
    global nutrient_1
    global nutrient_2
    global nutrient_3
    global nutrient_4

    while True:
        if state == 0:
            lcd.message = "BW EC pH       {}\n{:0>2d} {:0>2d} {:0>2d}".format(str(state), int(base_water), int(ec), int(pH))
        elif state == 1:
            lcd.message = "N1 N2 N3 N4    {}\n{:0>2d} {:0>2d} {:0>2d} {:0>2d}".format(str(state), int(nutrient_1), int(nutrient_2), int(nutrient_3), int(nutrient_4))
        
        time.sleep(0.1)


def local_buttons(i2c, lcd):
    global state
    #while True:
    if lcd.up_button:
        if state == 3:
            #lock.acquire()
            state = 0
            #lock.release()
        else:
            #lock.acquire()
            state += 1
            #lock.release()
    elif lcd.down_button:
        if state == 0:
            #lock.acquire()
            state = 3
            #lock.release()
        else:
            #lock.acquire()
            state -= 1
            #lock.release()

    #time.sleep(0.2)


#-----------------------------------SENSORS-----------------------------------
def read_base_water():
    pulseStart = 0

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
            print ("Distance:",distance - 0.5,"cm")     #Distance with calibration
            with lock:
                base_water.value = distance
        else:
            print ("Out Of Range")                      #display out of range
            with lock:
                base_water.value = 0

        time.sleep(BASE_WATER_UPDATE_INTERVAL)


#-----------------------------------WATERING----------------------------------
def node1_water_cycle():
    while True:
        try:
            print("START TIME:", node1_water_start.value)
        except:
            print("EXCEPTION OCCURRED")
        time.sleep(20)




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
        print("READING WATER TIME")
        curs.execute("SELECT hr FROM NODE1_WATER_FREQ")
        print(curs.fetchall()[0][0])
        curs.execute("SELECT min FROM NODE1_WATER_FREQ")
        print(curs.fetchall()[0][0])
        curs.execute("SELECT start FROM NODE1_WATER_FREQ")
        with lock:
            node1_water_start.value = curs.fetchall()[0][0].encode()
        print("TEST", node1_water_start.value)

        #print("OG datetime:", dt)
        #print("Current datetime:", datetime.now().isoformat())
        
        time.sleep(DB_READ_INTERVAL)

#-----------------------------------CLEANUP-----------------------------------
#@atexit.register
def cleanup():
    lcd.clear()
    #conn.close()
    #GPIO.cleanup()
    print("See ya later! :D")


#-------------------------------------MAIN-------------------------------------
def main():
    try:
        '''display_process = multiprocessing.Process(target=local_display, args=(i2c, lcd, state))
        button_process = multiprocessing.Process(target=local_buttons, args=(i2c, lcd, state))
        base_water_process = multiprocessing.Process(target=read_base_water)
        update_database_process = multiprocessing.Process(target=update_database)
        read_database_process = multiprocessing.Process(target=read_database)
        node1_water_cycle_process = multiprocessing.Process(target=node1_water_cycle)

        button_process.start()
        display_process.start()
        base_water_process.start()
        update_database_process.start()
        read_database_process.start()
        node1_water_cycle_process.start()'''

        display_thread = Thread(target=local_display, args=(i2c, lcd,))
        button_thread = Thread(target=local_buttons, args=(i2c, lcd,))

        display_thread.start()
        button_thread.start()
    except:
        print("Unable to start threads")

main()
