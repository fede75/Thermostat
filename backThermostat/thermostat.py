import RPi.GPIO as GPIO
import time
import datetime
from datetime import date
import Adafruit_DHT
import sqlite3
import logging
import logging.handlers



#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='thermostat.log',level=logging.DEBUG)

LOG_FILENAME = '/home/pi/Thermostat/backThermostat/logs/thermostat.out'

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=25000, backupCount=10)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

my_logger.addHandler(handler)


#READ SETUP FROM DB
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)

#SETUP READ
conn = sqlite3.connect('/home/pi/Thermostat/backThermostat/thermostat.db')
c = conn.cursor()
c.execute("SELECT * FROM SETUP")
row=c.fetchone()
my_logger.debug(row)
min_bet_chages=row[1]
min_temp=row[2]
pinThermostat=row[3]
pinRelay=row[4]
delayReadings=row[5]

#HEATING START OFF
heating_status=0
GPIO.setup(pinRelay,GPIO.IN)


heating_status_change=0
#MANUAL MODE WILL EXECUTE ONLY DURING 2 HOURS MAX
num_exe_manual_mode=0
while 1:
    #CHECK IF MANUAL_PROGRAM IS ACTIVE
    c.execute("SELECT * FROM MANUAL_PROGRAM")
    row=c.fetchone()
    mode=row[1]
    manual_temp=row[2]
    #READ DESIRE TEMP FROM DB
    if mode==1: # MANUAL MODE
        desire_temp=manual_temp
        num_exe_manual_mode+=1
        my_logger.debug("NUM EXEC MANUAL MODE:"+str(num_exe_manual_mode))
        #DEACTIVATE MANUAL MODE AFTER 1:30H
        if num_exe_manual_mode==270:
            c.execute("UPDATE MANUAL_PROGRAM SET ACTIVE=0")
            my_logger.debug("MANUAL MODE DEACTIVATED")
            num_exe_manual_mode=0
    else:       # PROGRAM MODE
        t = (date.today().isoweekday(),)
        c.execute("SELECT * FROM PROGRAM WHERE Day=? AND hour_ini<=time('now','localtime') AND hour_end>time('now','localtime')", t)
        row=c.fetchone()
        #IF THERE IS NOT PROGRAM USE MANUAL TEMP
        if row is not None:
            desire_temp=row[4]
        else:
            my_logger.warning("ALARM: NOT PROGRAM DEFINED. USING MANUAL TEMP")
            desire_temp=manual_temp

    my_logger.debug("DESIRE TEMP"+str(desire_temp)+" MODE:"+str(mode)+" --> "+str(row))
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pinThermostat)

    if humidity is not None and temperature is not None:
        my_logger.debug('TEMPERATURA ACTUAL={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        my_logger.error('Failed to get reading. Try again!')


    # WAIT 3 CICLES BEFORE SWITCHING ON/OFF HEATING
    if temperature<desire_temp and heating_status==0:
        if heating_status_change==3:
            GPIO.setup(pinRelay,GPIO.OUT)  #NO CUADRA HACERLO CON SETUP!!!!
            heating_status=1
            my_logger.info( "Enciende Caldera")
            heating_status_change=0
        else:
            heating_status_change+=1
            my_logger.debug( "Preparando encendido:"+str(heating_status_change))
    elif temperature>=desire_temp and heating_status==1:
        if heating_status_change==3:
            GPIO.setup(pinRelay,GPIO.IN)
            heating_status=0
            my_logger.info("Apaga Caldera!")
        else:
            heating_status_change+=1
            my_logger.debug( "Preparando apagado:"+str(heating_status_change))
    else:
        heating_status_change=0
    p=(temperature, humidity,desire_temp,heating_status)
    c.execute("INSERT INTO TEMP_HIST(DAY,TEMP,HUMIDITY,TEM_DES,HEATING) VALUES(datetime('now','localtime'), ?,?,?,?)",p)
    conn.commit()
    time.sleep(delayReadings)

GPIO.cleanup()
