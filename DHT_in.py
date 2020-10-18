import Adafruit_DHT
import time
import datetime
import mariadb
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
dht =  Adafruit_DHT.DHT22
pin =  17

db = mariadb.connect(host = "localhost", user = "root", passwd = "root", db = "iotaquaponic")
cur = db.cursor()

while True:
    humidity, temperature = Adafruit_DHT.read(dht, pin)
    recTime = datetime.datetime.now()
    
    i = recTime.strftime("%Y-%m-%d %H:%M:%S")
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        print("Current Time =", i)
        try:
            cur.execute("""INSERT INTO iotaquaponic.dht_logs(dateCreate, temperature, humidity) VALUES(%s,%s,%s)""",(i, temperature, humidity))
            db.commit()
        except:
            db.rollback()
    else:
        print('Failed to get reading. Try again!')
    time.sleep(600)
