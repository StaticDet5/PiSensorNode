import time
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_ADXL345 as ADXL345
import os
import glob
import RPi.GPIO as io
import log


validSensors = ['BMP180', 'OLED', 'L3G4200D', 'ADXL345', 'HMC5883L', 'None']

BMP180= BMP085.BMP085()

def BMP180c():
    temperature = BMP180.read_temperature()
    return temperature
def BMP180f():
    t = BMP180.read_temperature()
    temperature = ((t*1.8)+32)
    return temperature
def BMP180p():
    pressure = BMP180.read_pressure()
    return pressure
def BMP180sl():
    pressure = BMP180.read_sealevel_pressure()
    return pressure
def BMP180a():
    alt = BMP180.read_altitude()
    return alt
def BMP180allDict():
    cTemp = BMP180.read_temperature()
    t = BMP180.read_temperature()
    fTemp = ((t*1.8)+32)
    press = BMP180.read_pressure()
    slPress = BMP180.read_sealevel_pressure()
    alt = BMP180.read_altitude()
    dict = {'tempf' : fTemp, 'tempc' : cTemp, 'Pressure' : press, 'SLPress' : slPress, 'Alt' : alt}
    return dict

ADXL345 = ADXL345.Adafruit_ADXL345()

def ADXL345read():   #list
    triple = ADXL345.read()
    return triple

def ADXL345X():
    triple = ADXL345.read()
    return triple[0]

def ADXL345Y():
    triple = ADXL345.read()
    return triple[1]

def ADXL345Z():
    triple = ADXL345.read()
    return triple[2]

def ADXL345dict():
    triple = {'x' : ADXL345X(), 'y' : ADXL345Y(), 'z' : ADXL345Z()}
    return triple


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

def main():
    print BMP180allDict()
    print ADXL345read()


if __name__ == "__main__":
    print time.asctime()
    main()
    
