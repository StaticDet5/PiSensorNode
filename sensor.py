import time
import Adafruit_BMP.BMP085 as BMP085
import os
import glob
import RPi.GPIO as io


sensor = BMP085.BMP085()
##  This code is designed to take the feed from a variety of sensor feeds
##  it does so by take a given feed, normalize it, and assign it a time.
##  A separate function will then log it.
def main():

    test = sensor.read_temperature()
    temp = sensor.read_temperature()
    
    print 'Tempf {0:0.2f}'.format((temp*1.8)+32)
    print 'Tempc {0:0.2f}'.format(sensor.read_temperature())
    
    print 'Pressure {0:0.2f}'.format(sensor.read_pressure())
    print 'Pressure@SL {0:0.2f}'.format(sensor.read_sealevel_pressure())
    print 'AltitudeM {0:0.2f}'.format(sensor.read_altitude())
    DS18B20init()
    DS18B20thermometers = DS18B20discover()
    print DS18B20thermometers
    print DS18B20read_temp_c(DS18B20thermometers[0])
    

def tempc():
    temperature = sensor.read_temperature()
    return temperature
def tempf():
    t = sensor.read_temperature()
    temperature = ((t*1.8)+32)
    return temperature
def rawPress():
    pressure = sensor.read_pressure()
    return pressure
def SLpressure():
    pressure = sensor.read_sealevel_pressure()
    return pressure
def altitude():
    alt = sensor.read_altitude()
    return alt
def allDict():
    cTemp = sensor.read_temperature()
    t = sensor.read_temperature()
    fTemp = ((t*1.8)+32)
    press = sensor.read_pressure()
    slPress = sensor.read_sealevel_pressure()
    alt = sensor.read_altitude()
    dict = {'tempf' : fTemp, 'tempc' : cTemp, 'Pressure' : press, 'SLPress' : slPress, 'Alt' : alt}
    return dict

####### the following is for the DS18B20 thermometers

def DS18B20init():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

def DS18B20discover():
    base_dir = '/sys/bus/w1/devices/'
    thermometers = (glob.glob(base_dir + '28*'))
    return thermometers

def DS18B20read_temp_raw(thermometer):
    thermometer = thermometer + '/w1_slave'
    f=open(thermometer, 'r')
    time.sleep(0.2)
    line1 = f.readline()
    line2 = f.readline()
    f.close()
    return line2

def DS18B20read_temp_c(thermometer):
    lise = str(DS18B20read_temp_raw(thermometer))
    temp_pos = lines.find('t=')
    temp_string = lines[temp_pos+2:]
    temp_float = (float(temp_string)) / 1000.0
    return temp_float

if __name__ == "__main__":
    print time.asctime()
    main()
    
