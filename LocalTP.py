#!/usr/bin/python
import time
import sensor
import log

logFile = 'sensor.log'
interval = 60
logLevel = 'Info'
sensor1 = 'Temp1'
sensor1Type = 'Thermal'
sensor1Units = 'DegreeF'
sensor2 = 'Press1'
sensor2Type = 'Pressure'
sensor2Units = 'Pascals'

def main():
    x = 1
    while x == 1:
        currentTime = time.time()
        currentTime = round(currentTime)
        if currentTime % interval == 0:
            currentTemp = round(sensor.tempf(), 2)
            currentRawPress = sensor.rawPress()
            message = {'Time' : time.time(), 'Level' : logLevel, 'Sensor' : sensor1, 'Value' : currentTemp, 'Type' : sensor1Type, 'Units' : sensor1Units}
            log.sensorLog(logFile, message)
            log.log2net(message)
            message2 = {'Time' : time.time(), 'Level' : logLevel, 'Sensor' : sensor2, 'Value' : currentRawPress, 'Type' : sensor2Type, 'Units' : sensor2Units}
            log.sensorLog(logFile, message2)
            log.log2net(message2)
            print time.time(), time.asctime(), "    ", currentTemp, "   ", currentRawPress

        time.sleep(1)          

main()
