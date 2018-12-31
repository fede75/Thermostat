import boto3
import time
import datetime
from datetime import date
import sqlite3
import logging
import logging.handlers
from decimal import *

### LOGS CONFIGURATION ### 
LOG_FILENAME = '/home/pi/Thermostat/alexaThermostat/logs/alexaThermostat.out'
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=25000, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
my_logger.addHandler(handler)



### SQLITE3 CONNECTION ###
conn = sqlite3.connect('/home/pi/Thermostat/backThermostat/thermostat.db')
# Para poder utilizar nombres de columnas
conn.row_factory = sqlite3.Row
c = conn.cursor()


### CONECT TO DYNAMODB IN AWS
client = boto3.resource('dynamodb')
table_thermostat_status = client.Table("thermostat_status")
table_thermostat_alexa_order = client.Table("thermostat_alexa_order")


while 1:
	### READ DESIRE AND REAL TEMPERATURE
	c.execute("SELECT * FROM TEMP_HIST WHERE ID=(SELECT MAX(ID) FROM TEMP_HIST);")
	row=c.fetchone()
	my_logger.debug("Temp actual: " + str(row["temp"]) + " temp des: "+ str(row["tem_des"]) + " Estado Caldera: " + str(row["heating"]))
	read_date = row["day"]
	real_temp = row["temp"]
	desire_temp = row["tem_des"]
	heating_status = row["heating"]

	table_thermostat_status.put_item(TableName='thermostat_status', Item={'id' : 1, 'desire_temp' : Decimal(desire_temp) , 'real_temp' : Decimal(real_temp) , 'status' : heating_status , 'status_date':str(datetime.datetime.now())})
   
	### SEARCH FOR ANY ALEXA ORDER IN AWS DYNAMODB ###
	alexa_order = table_thermostat_alexa_order.get_item(TableName='thermostat_alexa_order' , Key={'id' : 1})

	if 'Item' in (alexa_order):
		my_logger.debug("Hay orden de Alexa con temperatura = " + str(alexa_order['Item']['desire_temp']))
		c.execute("UPDATE MANUAL_PROGRAM SET ACTIVE=1, TEMP="+str(alexa_order['Item']['desire_temp']))
		conn.commit()
		table_thermostat_alexa_order.delete_item(TableName='thermostat_alexa_order' , Key={'id' : 1})
		my_logger.debug("Orden alexa eliminada")
	else:
		my_logger.debug("No hay orden de Alexa")

    
	### DELAY 20 SEG
	time.sleep(5)
