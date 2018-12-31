import boto3
import time
import datetime
from datetime import date
import sqlite3
import logging
import logging.handlers
from decimal import *


### SQLITE3 CONNECTION ###
conn = sqlite3.connect('/home/pi/Thermostat/backThermostat/thermostat.db')
# Para poder utilizar nombres de columnas
conn.row_factory = sqlite3.Row
c = conn.cursor()

### CONECT TO DYNAMODB IN AWS
client = boto3.resource('dynamodb')
table = client.Table("thermostat_alexa_order")
table.put_item(TableName='thermostat_alexa_order', Item={'id' : 1, 'desire_temp' : 20 , 'order_date' : str(datetime.datetime.now())})
