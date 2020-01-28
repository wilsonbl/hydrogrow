import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import threading
import aiosqlite
import asyncio

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2
 
# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
 
# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# Display startup message
lcd.color = [100, 0, 0]
lcd.create_char(0, [0,0,1,1,2,1,7,8])
lcd.create_char(1, [0,24,4,18,9,5,21,9])
lcd.create_char(2, [0,23,8,20,19,8,6,1])
lcd.create_char(3, [0,1,17,17,1,2,4,24])
lcd.message = '\x00\x01  READY TO  \x00\x01\n\x02\x03    GROW    \x02\x03'
lcd.clear()

async def get_data():
    db = await aiosqlite.connect('../backend/database/HydroDatabase.db')

    cursor = await db.execute('SELECT base_water FROM timed ORDER BY time DESC LIMIT')
    base_water = await cursor.fetchone()

    return base_water

async def main():
    message = "Starting message"

    while True:
        if lcd.up_button:
            if state == 3:
                state = 0
            else:
                state += 1
        elif lcd.down_button:
            if state == 0:
                state = 3
            else:
                state -= 1
        
        message = await get_data()

        lcd.message = message
        #if state == 0:
        #   lcd.message = "BW\n" + state
        time.sleep(0.1)

asyncio.run(main())

'''def getSensorData():
    # Create connection to sqlite database
    conn = sqlite3.connect('../backend/database/HydroDatabase.db')
    curs = conn.cursor()

    global base_water

    while(1):
        curs.execute("SELECT time, base_water FROM timed ORDER BY time DESC LIMIT 1")
        rows = curs.fetchall()
        base_water = rows[0][1]
        time.sleep(5)
        print(base_water)


def main():
    state = 0
    global base_water

    while(1):
        if lcd.up_button:
            if state == 3:
                state = 0
            else:
                state += 1
        elif lcd.down_button:
            if state == 0:
                state = 3
            else:
                state -= 1

        if state == 0:
            lcd.message = "BW\n" + str(int(base_water))
        time.sleep(0.1)


base_water = 0
sensorThread = threading.Thread(target=getSensorData)
mainThread = threading.Thread(target=main)
sensorThread.start()
mainThread.start()'''