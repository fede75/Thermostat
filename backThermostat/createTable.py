import sqlite3
conn = sqlite3.connect('thermostat.db')

c = conn.cursor()

# Drop table si ya existe
c.execute("DROP TABLE PROGRAM")
#c.execute("DROP TABLE MANUAL_PROGRAM")
#c.execute("DROP TABLE TEMP_HIST")
#c.execute("DROP TABLE SETUP")

# Create table SETUP
# MIN_BET_CHANGES --> Delay in minutes between heating status changes
# MIN_TEMP --> Min temperature to avoid tubes freezing
# DELAY_TEMP_READS --> Delay between temp reads in seconds
#c.execute("CREATE TABLE SETUP(ID integer primary key,MIN_BET_CHANGES int, MIN_TEMP integer,TEMP_SENSOR_PIN integer, RELAY_SENSOR_PIN integer, DELAY_TEMP_READS integer)")

# Create table PROGRAM
c.execute("CREATE TABLE PROGRAM(id integer primary key, day integer, hour_ini text, hour_end text, temp real)")
# active --> 0 False 1 True
# Create table MANUAL_PROGRAM
#c.execute("CREATE TABLE MANUAL_PROGRAM(id integer primary key,active integer, temp real)")

# Create table TEMP_HIST
#c.execute("CREATE TABLE TEMP_HIST(id integer primary key,day text, temp real, humidity real,tem_des real, heating integer)")


# Insert SETUP data
#c.execute("INSERT INTO SETUP(MIN_BET_CHANGES, MIN_TEMP,TEMP_SENSOR_PIN, RELAY_SENSOR_PIN, DELAY_TEMP_READS) VALUES(3,5,4,18,20)")

# Insert MANUAL_PROGRAM data
#c.execute("INSERT INTO MANUAL_PROGRAM(ACTIVE,TEMP) VALUES (0,24)")

# Insert PROGRAM data
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (1,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (1,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (1,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (1,'21:30','23:59:59',20)")

c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (2,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (2,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (2,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (2,'21:30','23:59:59',20)")

c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (3,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (3,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (3,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (3,'21:30','23:59:59',20)")

c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (4,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (4,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (4,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (4,'21:30','23:59:59',20)")

c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (5,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (5,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (5,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (5,'21:30','23:59:59',20)")

c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (6,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (6,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (6,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (6,'21:30','23:59:59',20)")

c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (7,'00:00','07:45',18)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (7,'07:45','11:45',20)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (7,'11:45','21:30',23)")
c.execute("INSERT INTO program(DAY,HOUR_INI,HOUR_END,TEMP) VALUES (7,'21:30','23:59:59',20)")






# Save (commit) the changes
conn.commit()
