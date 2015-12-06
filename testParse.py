import cPickle as pickle
import time

def timePull(pulltime1, pulltime2, centralLog):
    if pulltime2 > pulltime1:
        placeholder = pulltime1
        pulltime1 = pulltime2
        pulltime2 = placeholder
    logFile = open(centralLog, 'r')
    workingLog = []
    try:
        while True:
            readFile = pickle.load(logFile)
            print readFile
            if pulltime1 <= float(readFile('Time')) <= pulltime2:
                workingLog.append(readFile)
                print readFile
    except:
            return workingLog
        
    logFile.close()


if __name__ == "__main__":
    start=time.time()
    centralLog = 'House.bak'
    pulltime1 = 1449061079
    pulltime2 = 1449061169
    print timePull(pulltime1, pulltime2, centralLog)
    #print lineCount(centralLog)
    end = time.time()
    print end-start

