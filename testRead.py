import time
import datetime
import mariadb
import RPi.GPIO as GPIO

db = mariadb.connect(host = "localhost", user = "root", passwd = "root", db = "iotaquaponic")
cur = db.cursor()
somename = "pinout"
relay1 = 23
relay2 = 24

while True: 
    cur.execute("SELECT settingsName, settingsValue FROM settings WHERE settingsName=?", (somename,))
    record = cur.fetchone()
 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(relay1, GPIO.OUT)
    GPIO.setup(relay2, GPIO.OUT)
    #channel_is_on = GPIO.input(relay2)
  
    if record[0] == somename and record[1] is "0":
        GPIO.output(relay1, 1)
        GPIO.output(relay2, 1)
        GPIO.input(relay1)
        GPIO.input(relay2)
        print("mati")
    elif record[0] == somename and record[1] is "1":
        GPIO.output(relay1, 0)
        GPIO.output(relay2, 0)
        #GPIO.cleanup()
        print("nyala")
  
    time.sleep(2)