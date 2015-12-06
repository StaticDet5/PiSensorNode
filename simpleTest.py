#!/usr/bin/python
import Adafruit_BMP.BMP085 as BMP085
import time
def main():
    
    sensor = BMP085.BMP085()
    temp = sensor.read_temperature()
    
    print 'Tempf {0:0.2f}'.format((temp*1.8)+32)
    print 'Tempc {0:0.2f}'.format(sensor.read_temperature())
    
    print 'Pressure {0:0.2f}'.format(sensor.read_pressure())
    print 'Pressure@SL {0:0.2f}'.format(sensor.read_sealevel_pressure())
    print 'AltitudeM {0:0.2f}'.format(sensor.read_altitude())

def tempf():
    temperature = sensor.read_temperature()
    return temperature
def tempc():
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
    
if __name__ == "__main__":
    print time.asctime()
    main()
    
