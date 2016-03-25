#!/usr/bin/python

##  This snippet takes an input (to be determined what form), and appends it
##  to a logfile passed to it in the input.
##  Log format should be "Time, Node-Sensor, value, units"
import logging
import time
import socket
import sys
#import pygal

try:
    import cPickle as pickle
except:
    import pickle
loggerIP = '192.168.1.50'
nodeName = 'Office'
centralLog = 'House.log'
localLog = 'Sensor.log'
pickleProtocol = 2

def log2file(logName, sensor, level, value, sensorType, units):
    
    filename = logName
    logtime = time.time()
    logtime = str(logtime)
    message = level,sensor,value,sensorType,units
    logging.basicConfig(level=logging.DEBUG,
                    format='%s : %s' % (logtime, message), 
                    filename=logName,
                    filemode='a')
    
    logging.info(message)
    print"Logged", message

def log2net(message, loggerIP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #data = pickle.dumps(message, pickleProtocol)
    data = message
    try:
        
        server_address = (loggerIP, 10000)
        print >>sys.stderr, 'connecting to "%s" port "%s"' % server_address
        sock.connect(server_address)
        print >>sys.stderr, 'sending "%s"' % data
        sock.sendall(data)
    finally:
        #print >>sys.stderr, 'closing socket'
        sock.close()

def netLogger():
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (loggerIP, 10000)
    sock.bind(server_address)
    sock.listen(1)
    print "Started!", time.time()
    while True:
        #print >>sys.stderr, 'waiting for connection'
        connection, client_address = sock.accept()
        try:
            print >>sys.stderr, 'connection from ', client_address,
            client_IP, client_Port = client_address
            client_IP = str(client_IP)
            client_Port = str(client_Port)
            strTime = str(time.time())
            netLog = open(centralLog, 'a')
            while True:
                data = connection.recv(2000)
                #translated = pickle.loads(data)
                #print >>sys.stderr, 'received "%s"' % translated
                #print 'Received ,', data
                if data:
                    #data = str(data)
                    translated = pickle.loads(data)
                    message = {'RecTime' : time.time(), 'ClientIP' : client_IP, 'ClientPort' : client_Port}
                    message.update(translated)
                    print message
                    message = pickle.dumps(message, pickleProtocol)
                    netLog.write(message)
                    #print data
                    #netLog.write(data)
                    netLog.close()
                else:
                    #print >>sys.stderr, 'no more data from ', client_address
                    break
        finally:
            connection.close
            
    
def directLog(logName, message):
    filename = open(logName, 'a')
    logtime = time.time()
    filename.write(message)
    filename.close()
    
def sensorLog(logName, message):
    filename = open(logName, 'a')
    logtime = time.time()
    #message = "%s | Level : %s | Sensor : %s | Value : %s | Type : %s | Units : %s \n" % (logtime, level, sensor, value, sensorType, units)
    if type(message) == 'dict':
        timeDict = {'Time' : logtime}
        message.update(timeDict)
    elif type(message) == 'string':
        message = (str(logtime)) + " " + message 
        
    data = pickle.dumps(message, pickleProtocol)
    filename.write(data)
    filename.close()

def logPrint(logName):
    tempFile = open(logName, 'r')
    logFile = pickle.load(tempFile)
    print logFile
    while True:
        logFile = pickle.load(tempFile)
        print logFile

def lineCount(logName):
    count = 0
    logFile = open(centralLog, 'r')
    try:
        while True:
            readFile = pickle.load(logFile)
            count = count + 1
    except:
        return count    
    logFile.close()

def logPrint(logName):
    count = lineCount(logName)
    print "This can take a minute or so per MB of log."
    print "Parsing " + str(lineCount()) + " lines of log."
    logFile = open(centralLog, 'r')
    log = ""
    try:
        while True:
            readFile = pickle.load(logFile)
            #print readFile
            log = log + str(readFile) + "\n"
    except:
            return log
    logFile.close()

def timePull(pulltime1, pulltime2, centralLog):  #returns a list of loglines (which are dictionaries)
    if pulltime2 < pulltime1:
        placeholder = pulltime1
        pulltime1 = pulltime2
        pulltime2 = placeholder
    count = lineCount(centralLog)
    logFile = open(centralLog, 'r')
    
    workingLog = []

    for i in range(count):
        logLine = pickle.load(logFile)
        #print str(pulltime1) + " " + str(logLine['Time']) + " " + str(pulltime2) 
        if float(pulltime1) <= logLine['Time']:
            
            if float(pulltime2) >= logLine['Time']:
                workingLog.append(logLine)
                
    logFile.close()
    return workingLog

def scaledTimePull(pulltime1, pulltime2, centralLog, scale):  #returns a scaled list of loglines (which are dictionaries), needs a rewrite
    if pulltime2 < pulltime1:
        placeholder = pulltime1
        pulltime1 = pulltime2
        pulltime2 = placeholder
    #count = lineCount(centralLog)
    logFile = open(centralLog, 'r')
    
    workingLog = []
   # print int(pulltime1), int(pulltime2), scale, count
    for i in range(int(pulltime1), int(pulltime2), scale):
        #print i, int(pulltime1), int(pulltime2), scale, count
        if i < int(pulltime2):
            #print i, int(pulltime2)
            try:
                logLine = pickle.load(logFile)
            except:
                #print "Skipped at", int(i)
                pass
            #print logLine
            #print str(pulltime1) + " " + str(logLine['Time']) + " " + str(pulltime2) 
            if float(pulltime1) <= logLine['Time']:
            
                if float(pulltime2) >= logLine['Time']:
                    workingLog.append(logLine)
        else:
            break
                
    logFile.close()
    return workingLog

def listValuePull(listName, attribute):  #returns a list of attribute values
    pulledList = []
    if type(listName) != type(pulledList):
        print 'Invalid list'
    for item in listName:
        if item.has_key(attribute):
            pulledList.append(item[attribute])
    return pulledList

def DictTimeValuePull(listName, attribute):  #returns a dictionary of attribute values with key of time from a list of log dictionaries
    pulledList = []
    newDict = {}
    if type(listName) != type(pulledList):
        print 'Invalid list'
    for item in listName:
        if item.has_key(attribute):
            tempDict = {item['Time'] : item[attribute]}
            newDict.update(tempDict)
    return newDict

def LogAttributePull(listName, attribute): #returns a list of dictionaries that all contain a given key (example, all dicts that have 'temp1')
    pulledList = []
    if type(listName) != type(pulledList):
        print 'Invalid list'
    for item in listName:
        if attribute in str(item):
            pulledList.append(item)

    return pulledList

def TwoKeyPull(listName, key1, key2):  # returns a list from dictionaries (log lines) that have match two keys.  IE:  Pull "Temperature" from "Office" lines from log dictionary
    pulledList = []
    if type(listName) != type(pulledList):
        print 'Invalid list'
    data = listValuePull(LogAttributePull(LogAttributePull(workingList, key1),key2), 'Value')
    return data
    
if __name__ == "__main__":
    start=time.time()
    #print logPrint(centralLog)
    #print lineCount(centralLog)
    currentTime = time.time()
    workingList = scaledTimePull(1449061019, (currentTime-10) , 'House.bak', 30)
    #print DictTimeValuePull(workingList, 'Value')
    #print listValuePull(workingList, 'Value')
    #print LogAttributePull(workingList, 'Temp1')
    data1 = listValuePull(LogAttributePull(LogAttributePull(workingList, '192.168.1.50'),'BMP180f'), 'Avg')
    #data2 = TwoKeyPull(workingList, '192.168.1.50','Temp1')
    #print data
    line_chart = pygal.Line()
    line_chart.title = 'Household Temperatures'
    line_chart.add('Office', data1)
    #line_chart.add('LivingRoom', data2)
    line_chart.render_to_png('tempOffice_chart3.png')
    end = time.time()
    print end-start
    
