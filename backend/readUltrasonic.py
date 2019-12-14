import RPi.GPIO as GPIO
import time
import sqlite3

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
TRIG = 7
GPIO.setup(11, GPIO.IN)
ECHO = 11
pulseStart = 0
pulseEnd = 0

conn = sqlite3.connect('./database/HydroDatabase.db')
curs = conn.cursor()

while(1):
    GPIO.output(TRIG, GPIO.LOW)                 #Set TRIG as LOW

    GPIO.output(TRIG, GPIO.HIGH)                  #Set TRIG as HIGH
    time.sleep(0.000001)                          #Delay of 0.00001 seconds
    GPIO.output(TRIG, GPIO.LOW)                   #Set TRIG as LOW

    while GPIO.input(ECHO)==0:               	  #Check if Echo is LOW
        pulseStart = time.time()                   #Time of the last  LOW pulse

    while GPIO.input(ECHO)==1:                    #Check whether Echo is HIGH
        pulseEnd = time.time()                     #Time of the last HIGH pulse 

    pulseDuration = pulseEnd - pulseStart      #pulse duration to a variable

    distance = pulseDuration * 17150             #Calculate distance
    distance = round(distance, 2)                 #Round to two decimal points

    if distance > 20 and distance < 400:          #Is distance within range
        print ("Distance:",distance - 0.5,"cm")     #Distance with calibration
        t = time.strftime("%H:%M:%S", time.localtime())
        curs.execute("INSERT INTO timed(time, base_water) VALUES(?, ?)", (t, distance-0.5))
        #curs.execute("UPDATE timed SET base_water = ?", (distance - 0.5,))
    else:
        print ("Out Of Range")                      #display out of range
        curs.execute("INSERT INTO timed(time, base_water) VALUES(?, ?)", (t, 0))
        #curs.execute("UPDATE timed SET base_water = ?", (0,))

    conn.commit()

    time.sleep(1) 

conn.close()
GPIO.cleanup()