import sensor
import log
import cPickle as pickle
import time
import pygal

centralLog = 'House.bak'

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
    
if __name__ == "__main__":
    start=time.time()
    #print logPrint(centralLog)
    #print lineCount(centralLog)
    workingList = timePull(1449061019, 1449061169, centralLog)
    #print DictTimeValuePull(workingList, 'Value')
    #print listValuePull(workingList, 'Value')
    #print LogAttributePull(workingList, 'Temp1')
    data = listValuePull(LogAttributePull(workingList, 'Temp1'), 'Value')
    print data
    bar_chart = pygal.Bar()
    bar_chart.add('Temp1', data)
    bar_chart.render_to_png('bar_chart.png')
    end = time.time()
    print end-start
    
