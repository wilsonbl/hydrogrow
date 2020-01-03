import RPi.GPIO as GPIO
import time
import sqlite3
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import atexit
import multiprocessing

#-----------------------------------SETUP-------------------------------------
# Pin assignments
TRIG = 4
ECHO = 17

# Update intervals (seconds)
DB_UPDATE_INTERVAL = 10
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

# Pin initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

#LCD initialization
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)


#--------------------------------LCD--------------------------------
def local_display(i2c, lcd, state):
    state.value = 0
    while True:
        if state.value == 0:
            lcd.message = "BW EC pH       {}\n{:0>2d} {:0>2d} {:0>2d}".format(str(state.value), int(base_water.value), int(ec.value), int(pH.value))
        elif state.value == 1:
            lcd.message = "N1 N2 N3 N4    {}\n{:0>2d} {:0>2d} {:0>2d} {:0>2d}".format(str(state.value), int(nutrient_1.value), int(nutrient_2.value), int(nutrient_3.value), int(nutrient_4.value))
        
        time.sleep(0.2)


def local_buttons(i2c, lcd, state):
    state.value = 0
    while True:
        if lcd.up_button:
            if state.value == 3:
                with lock:
                    state.value = 0
            else:
                with lock:
                    state.value += 1
        elif lcd.down_button:
            if state.value == 0:
                with lock:
                    state.value = 3
            else:
                with lock:
                    state.value -= 1

        time.sleep(0.2)


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

        if distance > 20 and distance < 400:            #Is distance within range
            print ("Distance:",distance - 0.5,"cm")     #Distance with calibration
            with lock:
                base_water.value = distance
        else:
            print ("Out Of Range")                      #display out of range
            with lock:
                base_water.value = 0

        time.sleep(BASE_WATER_UPDATE_INTERVAL)


#-----------------------------------DATABASE----------------------------------
def update_database():
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    while True:
        t = time.strftime("%H:%M:%S", time.localtime())
        print("INSERTING INTO DB: ", t, base_water.value - 0.5)
        curs.execute("INSERT INTO timed(time, base_water) VALUES(?, ?)", (t, base_water.value-0.5))

        conn.commit()
        time.sleep(DB_UPDATE_INTERVAL)


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
        display_process = multiprocessing.Process(target=local_display, args=(i2c, lcd, state))
        button_process = multiprocessing.Process(target=local_buttons, args=(i2c, lcd, state))
        base_water_process = multiprocessing.Process(target=read_base_water)
        database_process = multiprocessing.Process(target=update_database)

        button_process.start()
        display_process.start()
        base_water_process.start()
        database_process.start()

    except:
        print("Unable to start threads")

main()
