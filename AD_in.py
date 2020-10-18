import smbus
import time
import datetime
import mariadb

address =  0x48
bus = smbus.SMBus(1)
cmd =  0x40
db = mariadb.connect(host = "localhost", user = "root", passwd = "root", db = "iotaquaponic")
cur = db.cursor()

def analogRead(chn):
    value =  bus.read_byte_data(address, cmd+chn)
    return value

def analogWrite(value):
    bus.write_byte_data(address,cmd,value)
    
def loop():
    while True:
        recTime = datetime.datetime.now()    
        i = recTime.strftime("%Y-%m-%d %H:%M:%S")
        
        #val1 = analogRead(0)
        val2 = analogRead(1)
        val3 = analogRead(2)
        #val4 = analogRead(3)

        #analogWrite(val1)
        analogWrite(val2)
        analogWrite(val3)
        #analogWrite(val4)
        
        convertph = (0.048225806 * val2) + 2.852580645
        convertsoil = (-0.980392157 * val3) + 156.8627451
        
        print ('ADC Value Ph: %d, Convert : %d'%(val2,convertph))
        print ('ADC Value Soil: %d, Convert : %d'%(val3,convertsoil))
        try:
            cur.execute("""INSERT INTO iotaquaponic.ph_logs(dateCreate, ph) VALUES(%s,%s)""",(i, convertph))
            db.commit()
            cur.execute("""INSERT INTO iotaquaponic.soil_logs(dateCreate, soilMoisture) VALUES(%s,%s)""",(i, convertsoil))
            db.commit()
        except:
            db.rollback()
        time.sleep(600)
        
def destroy():
    print('problem with Analog to Digital Converter, restarting')
    time.sleep(2)

if __name__ == '__main__':
    print('program is starting')
    while True:
        try:
            loop()
        except:
            destroy()