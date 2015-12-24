#!/usr/bin/python
import time
import sensor2 as sensor
import log
import math
import os
import socket
import threading
try:
    import cPickle as pickle
except:
    import pickle
pickleProtocol = 2

validSensors = ['BMP180', 'OLED', 'L3G4200D', 'ADXL345', 'HMC5883L', 'None']
defaultConfig = {'Node' : 'Default', 'CentralLogIP' : '192.168.1.50', 'I2CBus1' : 'None'}
logIP = defaultConfig['CentralLogIP']

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name


class Node:
    'Every Pi within the sensor network is a Node'
    nodeCount = 0
    
    def __init__(self, name, logIP = logIP):
        print logIP
        configFileBase = 'NodeConfig.cfg'
        configFile = name + configFileBase
        self.name = name
        self.logIP = logIP
        print configFile
        try:
            configuration = open(configFile, 'r')
            config = pickle.load(configuration)
            logIP = config['CentralLogIP']
            print config
            configuration.close()
            self.sendMessage(data ={'Node' : config['Node'], 'Value' : 'NodeInitStart', 'Level' : 'Config'})
            #data = pickle.dumps(message, pickleProtocol)
            #log.log2net(message, logIP)
        except:
            print "Configuration file not found, starting first time configuration"
            try:
                self.sendMessage(data={'Node' : 'NewNode', 'Value' : 'NodeFirstConfig', 'Level' : 'Config'})
            except:
                print"Default IP does not work: ", self.logIP
            logIP = raw_input("IP of central logger (four numbers, 0-255, separated by periods (.))>>> ")
            self.logIP = logIP
            self.sendMessage(data ={'Node' : self.name, 'Value' : 'NodeName', 'Level' : 'Config'})
            config = {'Node' : self.name, 'CentralLogIP' : self.logIP}
            configFile = self.name + configFileBase
            configuration = open(configFile, 'w')
            data = pickle.dumps(config, pickleProtocol)
            configuration.write(data)
            configuration.close()
            self.sendMessage(data={'Value' : 'NodeConfigured', 'Level' : 'Config'})

        print "Completed initial config"    
        configuration = open(configFile, 'r')
        config = pickle.load(configuration)
        configuration.close()

        #######  Check for I2C sensors on bus 1

        i2cOneFile = os.popen('i2cdetect -y 1')
        i2cOne = i2cOneFile.read()
        i2cOneFile.close()
        linecount = i2cOne.count('\n')
        i2cOneList = i2cOne.splitlines(linecount)
        activeI2C = []
        del i2cOneList[0]
        #i2cOneList.append('80: -- 81 -- 83 -- -- 86 -- -- -- 8a -- \n')  ##debug lines to test multiple addresses
        #print i2cOneList
        for item in i2cOneList:
            cutIndex = item.find(':')
            newItem = item[cutIndex+1:]
            newItem = newItem.replace('--', '')
            
            while newItem.isspace() == False:
                newItem = newItem.lstrip()
                validAddr = newItem[0:2]
                activeI2C.append(validAddr)
                newItem = newItem[3:]
                #print newItem

        
        if config.has_key('I2CBus1') == False:
            I2CBus1 = {}
            for item in activeI2C:
                tempDict = {item : 'Unknown'}
                I2CBus1.update(tempDict)
            I2CDict = {'I2CBus1' : I2CBus1}
            config.update(I2CDict)


            
        configI2C = config['I2CBus1']   ## compares the checked I2C addresses versus the remembered addresses
        if cmp(configI2C.keys(), activeI2C) == False:
            self.sendMessage(data={'Sensor' : 'I2CBus1', 'Value' : 'Sensor Change', 'Level' : 'Config'})
            previous = 'Was ' + str(configI2C.keys())
            self.sendMessage(data={'Sensor' : 'I2CBus1', 'Value' : previous, 'Level' : 'Config'})

        print type(activeI2C)
        self.sendMessage(data={'Sensor' : 'I2CBus1', 'Value' : activeI2C, 'Level' : 'Config'})

        for item in configI2C:   #Attempts to lean what sensors are at various I2C addresses, then logs it
            if configI2C[item] == 'Unknown':
                query = 'Please tell me what kind of sensor is at I2C address '+ item + '. >>>'
                sensorName = raw_input(query)
                while sensorName not in validSensors:
                    print 'Currently Supported Sensors:'
                    print validSensors
                    sensorName = raw_input(query)
                tempdict = {item : sensorName}
                
                configI2C.update(tempdict)
            config.update(configI2C)
            configuration = open(configFile, 'w')
            data = pickle.dumps(config, pickleProtocol)
            configuration.write(data)
            configuration.close()
        self.sensorList = []
        for item in configI2C:  #Logs the I2C sensor to the central log, currently only BMP180, ADXL345 supported
            if configI2C[item] != 'None':
                self.sendMessage(data = {'Sensor' : 'I2CBus1', 'I2CAddr' : item, 'Type' : configI2C[item], 'Level' : 'Config'})
                print "First Config Sent"
                if  configI2C[item] == 'BMP180':
                    self.BMP180 = True
                    #BMP180f = Sensor(self, 'BMP180f', 'Thermal', 'BMP180', 'Degreesf', minValue = 32, maxValue = 138)
                    BMP180f = Sensor(self, 'BMP180f', 'Thermal', 'BMP180', 'Degreesf')
                    self.sendMessage(data = {'Sensor' : 'BMP180f', 'Value' :BMP180f.getValue()})
                    self.BMP180t = True
                    self.sensorList.append(BMP180f)
                    BMP180p = Sensor(self, 'BMP180p', 'Pressure', 'BMP180', 'Pascals')
                    self.sendMessage(data = {'Sensor' : 'BMP180p', 'Value' :BMP180p.getValue()})
                    self.BMP180p = True
                    self.sensorList.append(BMP180p)
                if configI2C[item] == 'ADXL345':
                    self.ADXL345 = True
                    ADXL345x = Sensor(self, 'ADXL345x', 'Accelx', 'ADXL345', 'M/s')
                    self.sendMessage(data = {'Sensor' : 'ADXL345x', 'Value' :ADXL345x.getValue()})
                    self.ADXL345x = True
                    self.sensorList.append(ADXL345x)
                    ADXL345y = Sensor(self, 'ADXL345y', 'Accely', 'ADXL345', 'M/s')
                    self.sendMessage(data = {'Sensor' : 'ADXL345y', 'Value' :ADXL345y.getValue()})
                    self.ADXL345y = True
                    self.sensorList.append(ADXL345y)
                    ADXL345z = Sensor(self, 'ADXL345z', 'Accelz', 'ADXL345', 'M/s')
                    self.sendMessage(data = {'Sensor' : 'ADXL345z', 'Value' :ADXL345z.getValue()})
                    self.ADXL345z = True
                    self.sensorList.append(ADXL345z)
                    print self.sensorList
                    
                    
        print self.sensorList
        self.go()
                    


    def go(self):     #######################WIP
        print "Go Initialized!!!!!!!!!!!!!!!!!!!!!"
        run = True
        x=0
        for item in self.sensorList:
            item.threadedMonitor()
            print item, " Started!"
        print "All threads started!"            

    def pickleMessage(self, data, level = 'Info'): #take a message dict, add the baseMessage, pickle, return
        baseMessage = {'Time' : time.time(), 'Node': self.name, 'Level' : level}
        logLine = baseMessage.update(data)
        package = pickle.dumps(logLine, pickleProtocol)
        return package
    
    def sendMessage(self, data, level = 'Info', logIP = None): #take a message dict, add the baseMessage, pickle, log it
        if logIP ==None:
            logIP = self.logIP
        baseMessage = {'Time' : time.time(),'Level' : level}
        baseMessage.update(data)
        if baseMessage.has_key('Node') == False:
            dataUpdate = {'Node' : self.name}
            baseMessage.update(dataUpdate)
        package = pickle.dumps(baseMessage, pickleProtocol)
        log.log2net(package, logIP)
        
    def message(self, data, level = 'Info'):  #basic log formatter
        baseMessage = {'Time' : time.time(), 'Node': self.name, 'Level' : level}
        baseMessage.update(data)
        return baseMessage

    def packageMessage(self, data):
        package = pickle.dumps(data, pickleProtocol)
        return package

    def sendLog(self, package, logIP = None):
        if logIP ==None:
            logIP = self.logIP
        log.log2net(package, logIP)

        
class Sensor:
    count = 0
    sensorList = []
    def __init__(self, nodeName, SensorName, valueType, sensorType, units, interval = 60, minInterval = 5, minValue = None, maxValue = None, report = 'normal', logIP = '192.168.1.50'):
        self.name = SensorName
        self.nodeName = nodeName
        self.valueType = valueType
        while sensorType not in validSensors:
            print "Invalid sensor type, ", sensorType
            print "Supported sensors: ", validSensors
            message = {'Time' : time.time(), 'Level' : 'Error', 'Node' : self.name, 'InvalidSensor' : sensorType}
            log.log2net(message, logIP)
            sensorType = raw_input("Please specify sensor type")
        self.sensorType = sensorType
        self.units = units
        self.interval = interval
        self.minInterval = minInterval
        self.minValue = minValue
        self.maxValue = maxValue
        self.report = report

        ######  Begin setting up sensors  ########


        
        self.logIP = logIP   ###Write a check here
        #self.baseMessage = {'Sensor' : self.name, 'Type' : self.valueType, 'Units' : self.units}
        Sensor.count += 1
    def baseMessage(self):
        self.base = {'Sensor' : self.name, 'Type' : self.valueType, 'Units' : self.units}
        return self.base
      
    def getValue(self):    ## returns a dictionary, used for reporting outside of the sensor, typically to the Node and beyond
        if self.name == 'BMP180f':
            self.value = sensor.BMP180f()
        elif self.name == 'BMP180p':
            self.value = sensor.BMP180p()
        elif self.name == 'ADXL345x':
            self.value = sensor.ADXL345X()
        elif self.name == 'ADXL345y':
            self.value = sensor.ADXL345Y()
        elif self.name == 'ADXL345z':
            self.value = sensor.ADXL345Z()
        if self.minValue != None:
            if self.value < self.minValue:
                self.data={'Level' : 'Critical', 'Value' : self.value}
                self.data.update(self.baseMessage())
                self.nodeName.sendMessage(self.data)
        if self.maxValue != None:
            if self.value > self.maxValue:
                self.data={'Level' : 'Critical', 'Value' : self.value}
                self.data.update(self.baseMessage())
                self.nodeName.sendMessage(self.data)
        
        self.data = self.baseMessage()
        self.data['Value'] = self.value
        return self.data

    def discreteValue(self):   ## returns only a value
        if self.name == 'BMP180f':
            self.value = sensor.BMP180f()
        elif self.name == 'BMP180p':
            self.value = sensor.BMP180p()
        elif self.name == 'ADXL345x':
            self.value = sensor.ADXL345X()
        elif self.name == 'ADXL345y':
            self.value = sensor.ADXL345Y()
        elif self.name == 'ADXL345z':
            self.value = sensor.ADXL345Z()
        if self.minValue != None:
            if self.value < self.minValue:
                self.data={'Level' : 'Critical', 'Value' : self.value}
                self.data.update(self.baseMessage())
                self.nodeName.sendMessage(self.data)
        if self.maxValue != None:
            if self.value > self.maxValue:
                self.data={'Level' : 'Critical', 'Value' : self.value}
                self.data.update(self.baseMessage())
                self.nodeName.sendMessage(self.data)
        return self.value
        
    def monitor(self, run=True, memorySize = 60000):
        self.sensorMemory = []
        self.reportTime = time.time()
        self.nextReport = self.reportTime + self.interval
        self.singleValue = self.discreteValue()
        self.memorySize = memorySize
        self.runningTotal = 0
        x=0
        while run==True:
            self.intervalTime = time.time()
            x=x+1
            self.runningTotal = self.runningTotal + self.singleValue
            if len(self.sensorMemory) > self.memorySize:
                self.runningTotal = self.runningTotal - self.sensorMemory[0]
                del self.sensorMemory[0]
            self.singleValue = self.discreteValue()
            self.sensorMemory.append(self.singleValue)
            if self.intervalTime > self.reportTime:
                self.reportTime = (time.time() + self.interval)
                self.dataMin = min(self.sensorMemory)
                self.dataMax = max(self.sensorMemory)
                self.dataAvg = (sum(self.runningTotal[-x:] / x)

                self.data={'Value': self.singleValue, 'Min': self.dataMin, 'Max' : self.dataMax, 'Avg' : self.dataAvg}
                self.data.update(self.baseMessage())
                self.nodeName.sendMessage(self.data)
                x=0
                               
            
    def threadedMonitor(self, run=True, memorySize = 60000):
        self.t = threading.Thread(target=self.monitor)
        self.t.start()
        
        
        
        

if __name__ == "__main__":
    start=time.time()
    OfficeNode = Node("Office")
    end = time.time()
    print end-start
