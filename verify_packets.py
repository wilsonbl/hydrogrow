import sqlite3

num_packets = 20

conn = sqlite3.connect('backend/database/HydroDatabase.db')
curs = conn.cursor()

#Get packets from DB
curs.execute("SELECT time, base_water FROM BASE_WATER ORDER BY time DESC LIMIT " + str(num_packets))
DB_packets = (curs.fetchall())

#Get packets copied from web server
f = open("web_packets.txt", "r")
web_packets = f.readlines()
f.close()
web_packets.reverse() # Reverse so you are comparing the latest packets first

good_packets = 0
for i in range(num_packets):
    DB_time = DB_packets[i][0]
    DB_val = DB_packets[i][1]
    web_time = int(web_packets[i].split('time: ')[1].split(',')[0])
    web_val = int(web_packets[i].split('base_water: ')[1].split('}')[0])

    print("DB: " + str(DB_time) + ", " + str(DB_val) + ", Web: " + str(web_time) + ", " + str(web_val))
    if DB_time == web_time and DB_val == web_val:
        print("GOOD PACKET")
        good_packets += 1
    else:
        print("BAD PACKET")

print("PERCENTAGE OF ERROR_FREE PACKETS: " + str((good_packets/num_packets) * 100) + "%")