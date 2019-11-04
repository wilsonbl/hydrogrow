import RPi.GPIO as GPIO
import time
import sqlite3

conn = sqlite3.connect('sensorDatabase.db')
curs = conn.cursor()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def add_reading():
    reading = GPIO.input(7)
    print(reading)
    curs.execute("INSERT INTO readings values(?)", (reading,))
    conn.commit
    time.sleep(0.2)

for _ in range(20):
    add_reading()

print("CURRENT STATE")
for row in curs.execute("SELECT * FROM readings"):
    print(row)

conn.close()