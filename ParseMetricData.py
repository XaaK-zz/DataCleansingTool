###########################################################
# ParseMetricData.py
# Copyright © Zach Greenvoss 
# Licensed under the MIT license - http://www.opensource.org/licenses/mit-license.php
###########################################################
import os
import datetime
import sys
    
timeCollection1 = {}
timeCollection2 = {}
timeCollection3 = {}
metricsRun1 = []
metricsRun2 = []
metricsRun3 = []
normalizedTimeCollection1 = {}
normalizedTimeCollection2 = {}
normalizedTimeCollection3 = {}

def getMetricNames(file,testRunDataNumber):
    #get metric name
    #print "GetMetricNames - " + str(file)
    fileNoExt = os.path.splitext(file)[0]
    x = fileNoExt.find("t0" + str(testRunDataNumber))
    if x < 0:
        return
    
    metricName = fileNoExt[(x+4):]
    try:
        if testRunDataNumber == 1:
            x = metricsRun1.index(metricName)
        elif testRunDataNumber == 2:
            x = metricsRun2.index(metricName)
        elif testRunDataNumber == 3:
            x = metricsRun3.index(metricName)
    except:
        if testRunDataNumber == 1:
            x = metricsRun1.append(metricName)
        elif testRunDataNumber == 2:
            x = metricsRun2.append(metricName)
        elif testRunDataNumber == 3:
            x = metricsRun3.append(metricName)
        pass

    return

def gatherMetrics(folder):
    #print "Gather Metrics - " + folder
    if os.path.isdir(folder):
        ext = os.listdir(folder)
        for e in ext:
            if e.find("t01") >= 0:
                getMetricNames(os.path.join(folder,e),1)
            elif e.find("t02") >= 0:
                getMetricNames(os.path.join(folder,e),2)
            elif e.find("t03") >= 0:
                getMetricNames(os.path.join(folder,e),3)
            else:
                print "Invalid file - " + e
            



def updateTimeSlices(timeCollection,destTimeCollection,timeDelta,metricData):
    currentBottomTime = datetime.datetime.strptime(sorted(timeCollection.iterkeys())[0],"%Y-%m-%d %H:%M:%S.%f") - datetime.timedelta(0,0,0,timeDelta)
    currentTopTime = currentBottomTime + datetime.timedelta(0,0,0,timeDelta)
        
    while True:
        tempCollection = ["" for x in range(len(metricData))]
        count = 0
        #print "Bottom: " + str(currentBottomTime)
        #print "Top: " + str(currentTopTime)
        for key in sorted(timeCollection.iterkeys()):
            currentTime = datetime.datetime.strptime(str(key),"%Y-%m-%d %H:%M:%S.%f")
            if currentTime > currentBottomTime and currentTime <= currentTopTime:
                #metric row within time slice
                #print "Valid Metric Found. CurrentTime: " + str(currentTime)
                #print "     Bottom: " + str(currentBottomTime)
                #print "     Top: " + str(currentTopTime)
                #print "     " + str(timeCollection1[key])
                
                count += 1
                for x in range(0,len(timeCollection[key])):
                    if len(tempCollection) <= x:
                        print "Error - size issue. x: " + str(x) + "len(tempCollection): " + str(len(tempCollection))
                        print "len(metricsRun1): " + str(len(metricsRun1))
                        print "len(metricsRun2): " + str(len(metricsRun2))
                        print "len(metricsRun3): " + str(len(metricsRun3))
                    #print x    
                    if tempCollection[x] == "":
                        if timeCollection[key][x] == "":
                            currentVal = 0.0
                        else:
                            currentVal = float(timeCollection[key][x])
                    else:
                        currentVal = float(tempCollection[x])
                        
                    if timeCollection[key][x] == "":
                        newVal = 0.0
                    else:
                        newVal = float(timeCollection[key][x])
                    #if x == 0:
                    #    print "currentVal: " + str(currentVal) + " newVal: " + str(newVal)
                    #calculate running average...
                    if float(newVal) != 0.0:
                        tempCollection[x] = (((count - 1) * currentVal) + newVal)/float(count)
                    #print "currentVal: " + str(currentVal) + " newVal: " + str(newVal) + " - " + str(tempCollection[x])
            elif currentTime > currentBottomTime and currentTime > currentTopTime:
                    #outside time slice
                    break     
        
        #print "Done with time slice - adding " + str(len(tempCollection)) + " metric into slice. count: " + str(count)
        destTimeCollection[currentBottomTime] = tempCollection
        
        #advance time window
        currentBottomTime = currentTopTime + datetime.timedelta(0,0,0,1)
        currentTopTime = currentTopTime + datetime.timedelta(0,0,0,timeDelta)
    
        #check for exit
        if datetime.datetime.strptime(sorted(timeCollection.iterkeys())[-1],"%Y-%m-%d %H:%M:%S.%f") < currentBottomTime:
            break;
    return

#datetime.datetime.strptime(splitData[1][1:] + " " + splitData[2][:-1],"%Y-%m-%d %H:%M:%S.%f")])

def addToTimeSlice(file,testRunDataNumber,timeDelta):
    #print file
    timeData = []
    currentBottomTime = datetime.datetime(1900,1,1)
    
    #open file
    index = 0
    fileData = open(file,"r")
    while fileData:
        line = fileData.readline()
        if len(line) == 0:
            break;
        #time data
        lineData = line.split(",")
        dateField = lineData[0]
        valueField = lineData[1].strip()
        if testRunDataNumber == 1:
            if timeCollection1.has_key(dateField):
                tempCollection = timeCollection1.get(dateField)
            else:
                tempCollection = ["" for x in range(len(metricsRun1))]
            
            index = metricsRun1.index(metricName)
            tempCollection[index] = valueField
            timeCollection1[dateField] = tempCollection
        elif testRunDataNumber == 2:
            if timeCollection2.has_key(dateField):
                tempCollection = timeCollection2.get(dateField)
            else:
                tempCollection = ["" for x in range(len(metricsRun2))]
            
            index = metricsRun2.index(metricName)
            tempCollection[index] = valueField
            timeCollection2[dateField] = tempCollection
        elif testRunDataNumber == 3:
            if timeCollection3.has_key(dateField):
                tempCollection = timeCollection3.get(dateField)
            else:
                tempCollection = ["" for x in range(len(metricsRun3))]
            
            index = metricsRun3.index(metricName)
            tempCollection[index] = valueField
            timeCollection3[dateField] = tempCollection
         
        index += 1
    fileData.close()
    

def gatherMetricData(folder,timeDelta):
    #print folder
    if os.path.isdir(folder):
        ext = os.listdir(folder)
        for e in ext:
            if e.find("t01") >= 0:
                addToTestSet(os.path.join(folder,e),1,timeDelta)
            elif e.find("t02") >= 0:
                addToTestSet(os.path.join(folder,e),2,timeDelta)
            elif e.find("t03") >= 0:
                addToTestSet(os.path.join(folder,e),3,timeDelta)
            
    return

def addToTestSet(file,testRunDataNumber,timeDelta):
    #print file
    fileNoExt = os.path.splitext(file)[0]
    metricData = []
    #get metric name
    x = fileNoExt.find("t0" + str(testRunDataNumber))
    metricName = fileNoExt[(x+4):]
    #print metricName
    #open file
    index = 0
    #print "Opening " + str(file)
    fileData = open(file,"r")
    while fileData:
        
        line = fileData.readline()
        if len(line) == 0:
            break;
        metricData.append(metricName + "," + line)
        #time data
        lineData = line.split(",")
        dateField = lineData[0]
        valueField = lineData[1].strip()
        #print dateField
        #print valueField
        if testRunDataNumber == 1:
            if timeCollection1.has_key(dateField):
                tempCollection = timeCollection1.get(dateField)
            else:
                tempCollection = ["" for x in range(len(metricsRun1))]
            
            index = metricsRun1.index(metricName)
            tempCollection[index] = valueField
            timeCollection1[dateField] = tempCollection
        elif testRunDataNumber == 2:
            if timeCollection2.has_key(dateField):
                tempCollection = timeCollection2.get(dateField)
            else:
                tempCollection = ["" for x in range(len(metricsRun2))]
            
            index = metricsRun2.index(metricName)
            tempCollection[index] = valueField
            timeCollection2[dateField] = tempCollection
        elif testRunDataNumber == 3:
            if timeCollection3.has_key(dateField):
                tempCollection = timeCollection3.get(dateField)
            else:
                tempCollection = ["" for x in range(len(metricsRun3))]
            
            index = metricsRun3.index(metricName)
            tempCollection[index] = valueField
            timeCollection3[dateField] = tempCollection
         
        index += 1
    fileData.close()
    
def main():

    if (len(sys.argv) < 2):
        print("Please provide the location of the POWER-COOLING directory.")
        quit()
    
    if (len(sys.argv) < 3):
        print("No output directory specified - defauling to current directory.")
        outputDir = os.getcwd()
    else:
        print("Output directory set to: " + sys.argv[2])
        outputDir = sys.argv[2]
        
    if (len(sys.argv) < 4):
        print("No time argument specified - use time values as default.")
        timeDelta = -1
    else:
        print("Time argument specified - using time slices of " + sys.argv[3] + " milliseconds.")
        timeDelta = int(sys.argv[3])

    print "Gathering data..."
    
    files = os.listdir(sys.argv[1])
        
    #Loop through directories - first getting metric names
    #   then getting metric data
    for file in files:
        gatherMetrics(os.path.join(sys.argv[1],file))
    
    for file in files:
        gatherMetricData(os.path.join(sys.argv[1],file),timeDelta)
    
    if timeDelta != -1:
        updateTimeSlices(timeCollection1,normalizedTimeCollection1,timeDelta,metricsRun1)
        updateTimeSlices(timeCollection2,normalizedTimeCollection2,timeDelta,metricsRun2)
        updateTimeSlices(timeCollection3,normalizedTimeCollection3,timeDelta,metricsRun3)
    
    print "done generating collections..."
    print "writing test data..."
    
    fileData = open(os.path.join(outputDir,"TimeData1.csv"),"w")
    fileData.write("Time,")
    for metric in metricsRun1:
        fileData.write(metric + ", ")
    fileData.write("\n")
    
    for key in sorted(timeCollection1.iterkeys()):
        fileData.write(str(key) + ", ")
        for metricData in timeCollection1[key]:
            fileData.write(str(metricData) + ", ")
        fileData.write("\n")
    fileData.close()
    
    fileData = open(os.path.join(outputDir,"NormalizedTimeData1.csv"),"w")
    fileData.write("Time,")
    for metric in metricsRun1:
        fileData.write(metric + ", ")
    fileData.write("\n")
    
    for key in sorted(normalizedTimeCollection1.iterkeys()):
        fileData.write(str(key) + ", ")
        for metricData in normalizedTimeCollection1[key]:
            fileData.write(str(metricData) + ", ")
        fileData.write("\n")
    fileData.close()
    
    fileData = open(os.path.join(outputDir,"TimeData2.csv"),"w")
    fileData.write("Time,")
    for metric in metricsRun2:
        fileData.write(metric + ", ")
    fileData.write("\n")
    
    for key in sorted(timeCollection2.iterkeys()):
        fileData.write(str(key) + ", ")
        for metricData in timeCollection2[key]:
            fileData.write(str(metricData) + ", ")
        fileData.write("\n")
    fileData.close()
    
    
    fileData = open(os.path.join(outputDir,"NormalizedTimeData2.csv"),"w")
    fileData.write("Time,")
    for metric in metricsRun2:
        fileData.write(metric + ", ")
    fileData.write("\n")
    
    for key in sorted(normalizedTimeCollection2.iterkeys()):
        fileData.write(str(key) + ", ")
        for metricData in normalizedTimeCollection2[key]:
            fileData.write(str(metricData) + ", ")
        fileData.write("\n")
    fileData.close()
    
    fileData = open(os.path.join(outputDir,"TimeData3.csv"),"w")
    fileData.write("Time,")
    for metric in metricsRun3:
        fileData.write(metric + ", ")
    fileData.write("\n")
    
    for key in sorted(timeCollection3.iterkeys()):
        fileData.write(str(key) + ", ")
        for metricData in timeCollection3[key]:
            fileData.write(str(metricData) + ", ")
        fileData.write("\n")
    fileData.close()
    
    fileData = open(os.path.join(outputDir,"NormalizedTimeData3.csv"),"w")
    fileData.write("Time,")
    for metric in metricsRun3:
        fileData.write(metric + ", ")
    fileData.write("\n")
    
    for key in sorted(normalizedTimeCollection3.iterkeys()):
        fileData.write(str(key) + ", ")
        for metricData in normalizedTimeCollection3[key]:
            fileData.write(str(metricData) + ", ")
        fileData.write("\n")
    fileData.close()
    
main()