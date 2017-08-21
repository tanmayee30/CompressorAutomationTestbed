#!/usr/bin/env python
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import sys
import os

#from datetime import datetime
import datetime
import glob
import MySQLdb
from time import strftime

import time                             # time used for delays
import httplib, urllib                  # http and url libs used for HTTP $
import socket
import json
import ctypes
import RPi.GPIO as gpio
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(36,gpio.OUT)
gpio.output(36,0)

#############################################################################################

server = "data.sparkfun.com"        					# base URL of your feed
publicKey = "9b1g78xoMjs8787z3OwZ" 					#"GEGLXdO3dnHDKar5x2xW"
privateKey = "xv9R17XkDntnYnYr259q" 					#"Nnlxo7DK7Vij456RVJVD"
fields = ["aux_temp","bat_temp","comp_curr","hp","lp","milk_temp"]    	# Your feed's data fields


# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
client=ModbusClient(method='rtu',port='/dev/ttyUSB0',baudrate=9600,timeout=1,parity='N')
client.connect()

db = MySQLdb.connect(host="localhost", user="root",passwd="root", db="temp_database")
cur = db.cursor()

response=client.read_holding_registers(0004,6,unit=1) #(starting addr, no of registers to be read, slave addr)
responseFault=client.read_holding_registers(0022,14,unit=1)

with open('/var/www/html/AutomationProject/file2.json')as f:
    data = json.loads(f.read())

print data['serial']
serialNum = data['serial']

######################### Read MOD-BUS registers ############################
bat_x = response.registers[0]
bat_temp = (ctypes.c_int16(bat_x).value)/10.0
print bat_temp

milk_y = response.registers[1]
milk_temp = (ctypes.c_int16(milk_y).value)/10.0
print milk_temp

aux_temp = response.registers[2]/10.0
comp_curr = response.registers[5]/10.0

HP=0
LP=0
fault = responseFault.registers[12]
print "Fault register reading: ",fault
if fault == 4:
    HP = 1
elif fault == 5:
    LP = 1
else:
    HP = 0
    LP = 0
#############################################################################

client.close()

while True:
    Milk = milk_temp;
    Ambient = aux_temp;
    Battery = bat_temp;
    Comp = comp_curr;
    
    print "Milk Temp: ",Milk
    print "Aux Temp: ",Ambient
    print "Battery Temp: ",Battery
    print "Comp curr: ",Comp
    print "HP in while : ",HP
    print "LP in while : ",LP
    datetimeWrite = (time.strftime("%Y-%m-%d "))
    time_ = (time.strftime("%H:%M:%S"))
    #time_ =  "%s-%s-%s" % (datetime.now().hour,datetime.now().minute, datetime.now().second)  
    #datestamp =  "%s-%s-%s" % (datetime.now().year,datetime.now().month, datetime.now().day)


    if 24.8 <= Milk <=25.2:
        print "In milk"
        gpio.output(36,1)
        time.sleep(3)
        gpio.output(36,0)
    elif Battery == -10.0:
        print "In battery"
        gpio.output(36,1)
        time.sleep(6)
        gpio.output(36,0)
    else:
        print "Out of buzzer condition"
    print datetimeWrite
    print time_
    if Milk<=29.0 or Battery==-10.0:
        sql = ("""INSERT INTO compData(date,time,SerialNo, Bat_temp, Milk_temp, Aux_temp, Comp_curr,HP,LP) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(datetimeWrite,time_,serialNum,Battery,Milk,Ambient,Comp,HP,LP))  
    try:
        print "Writing to database..."
        # Execute the SQL command
        cur.execute(*sql)
        # Commit your changes in the database
        db.commit()
        print "Write Complete"
	data = {} # Create empty set, then fill in with our three fields:
                # Field 0, light, gets the local time:
	data[fields[0]] = aux_temp
                # Field 1, switch, gets the switch status:
	data[fields[1]] = bat_temp
	data[fields[2]] = comp_curr
	data[fields[3]] ="0"# hp
	data[fields[4]] ="0"# lp
	data[fields[5]] = milk_temp
	params = urllib.urlencode(data)

	headers = {} # start with an empty set
                # These are static, should be there every time:
	headers["Content-Type"] = "application/x-www-form-urlencoded"
	headers["Connection"] = "close"
	headers["Content-Length"] = len(params) # length of data
	headers["Phant-Private-Key"] = privateKey # private key he

	#c = httplib.HTTPConnection(server)

	#c.request("POST", "/input/" + publicKey + ".txt", params, headers)
	#r = c.getresponse() # Get the server's response and print it
	#print r.status, r.reason

################################# Condition check for Buzzer ######################
	if 24.8 <= Milk <=25.2:
                print "In milk"
                gpio.output(36,1)
                time.sleep(3)
                gpio.output(36,0)
        elif -9.8 <= Battery <= -10.0:
                print "In battery"
                gpio.output(36,1)
                time.sleep(6)
                gpio.output(36,0)
####################################################################################

    except:
        # Rollback in case there is any error
        db.rollback()
        print "Failed writing to database"

    cur.close()
    db.close()
    break


#print response.registers[0:]
#print "Battery Temp:",bat_temp
#print "Milk_temp:",milk_temp
#print "Aux. Temp:",aux_temp
#print "Comp curr:",comp_curr
