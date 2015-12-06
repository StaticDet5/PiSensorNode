#!/usr/bin/python

##  This snippet takes an input (to be determined what form), and appends it
##  to a logfile passed to it in the input.
##  Log format should be "Time, Node-Sensor, value, units"
import logging
import time
import socket
import sys
import pygal

try:
    import cPickle as pickle
except:
    import pickle
loggerIP = '192.168.1.50'
nodeName = 'Office'
centralLog = 'House.log'
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

def log2net(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = pickle.dumps(message, pickleProtocol)
    try:
        
        server_address = (loggerIP, 10000)
        print >>sys.stderr, 'connecting to "%s" port "%s"' % server_address
        sock.connect(server_address)
        print >>sys.stderr, 'sending "%s"' % data
        sock.sendall(data)
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()

def netLogger():
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (loggerIP, 10000)
    sock.bind(server_address)
    sock.listen(1)
    while True:
        print >>sys.stderr, 'waiting for connection'
        connection, client_address = sock.accept()
        try:
            print >>sys.stderr, 'connection from ', client_address
            client_IP, client_Port = client_address
            client_IP = str(client_IP)
            client_Port = str(client_Port)
            strTime = str(time.time())
            netLog = open(centralLog, 'a')
            while True:
                data = connection.recv(1000)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    #data = str(data)
                    message = {'RecTime' : time.time(), 'ClientIP' : client_IP, 'ClientPort' : client_Port}
                    print type(data)
                    data= pickle.loads(data)
                    message.update(data)
                    print message
                    message = pickle.dumps(message, pickleProtocol)
                    netLog.write(message)
                    #print data
                    #netLog.write(data)
                    netLog.close()
                else:
                    print >>sys.stderr, 'no more data from ', client_address
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

    





if __name__ == "__main__":
    main()
    

 
