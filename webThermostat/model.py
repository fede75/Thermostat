import web
import datetime
from datetime import date

db = web.database(dbn='sqlite', db='../backThermostat/thermostat.db')


# TABLE PROGRAM
def get_programs():
    return db.select('program', order='day,hour_ini ASC')


def get_program(id):
    try:
        return db.select('program', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def get_active_program():
    try:
        day=date.today().isoweekday()
        return db.query("SELECT * FROM PROGRAM WHERE day=$day AND hour_ini<=time('now','localtime') AND hour_end>time('now','localtime')",vars={'day':day})[0]
    except IndexError:
        return None


def new_program(day, hour_ini, hour_end, temp):
    db.insert('program', seqname=False, day=day, hour_ini=hour_ini, hour_end=hour_end, temp=temp)


def del_program(id):
    db.delete('program', 'id=$id', vars=locals())


def update_program(id, day,hour_ini,hour_end,temp):
    db.update('program', where="id=$id", vars=locals(),
              day=day, hour_ini=hour_ini, hour_end=hour_end, temp=temp)


# TABLE TEMP_HIST
def get_last_temp():
    return db.select('temp_hist', order='day DESC', limit=1)

def get_list_temp():
    return db.select('temp_hist', order='day DESC', limit=55)

# TABLE SETUP


# TABLE MANUAL
def get_manual_program():
    return db.select('manual_program')[0]

def update_manual_program(active,temp):
    db.update('manual_program',where="id=1",vars=locals(),active=active,temp=temp)

