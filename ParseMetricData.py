import os
import datetime
import sys
    
timeCollection1 = {}
timeCollection2 = {}
timeCollection3 = {}
metricsRun1 = []
metricsRun2 = []
metricsRun3 = []

def getMetricNames(file,testRunDataNumber):
    #get metric name
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
    print folder
    if os.path.isdir(folder):
        ext = os.listdir(folder)
        for e in ext:
            if e.find("t01") >= 0:
                getMetricNames(os.path.join(folder,e),1)
            elif e.find("t02") >= 0:
                getMetricNames(os.path.join(folder,e),2)
            elif e.find("t03") >= 0:
                getMetricNames(os.path.join(folder,e),3)
            
            
def gatherMetricData(folder):
    print folder
    if os.path.isdir(folder):
        ext = os.listdir(folder)
        for e in ext:
            if e.find("t01") >= 0:
                addToTestSet(os.path.join(folder,e),1)
            elif e.find("t02") >= 0:
                addToTestSet(os.path.join(folder,e),2)
            elif e.find("t03") >= 0:
                addToTestSet(os.path.join(folder,e),3)
            
    return

def addToTestSet(file,testRunDataNumber):
    print file
    fileNoExt = os.path.splitext(file)[0]
    metricData = []
    #get metric name
    x = fileNoExt.find("t0" + str(testRunDataNumber))
    metricName = fileNoExt[(x+4):]
    print metricName
    #open file
    index = 0
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

    print "Gathering data..."
    
    files = os.listdir(sys.argv[1])
        
    #Loop through top level directories
    for file in files:
        gatherMetrics(os.path.join(sys.argv[1],file))
        
        #if os.path.isdir(file) and (os.path.split(file)[1].find("POWER-COOLING") >=0):
        #    ext = os.listdir(file)
        #    for e in ext:
        #        gatherMetrics(os.path.join(file,e))
    
    for file in files:
        gatherMetricData(os.path.join(sys.argv[1],file))
    
    
    #for file in files:
    #    if os.path.isdir(file) and (os.path.split(file)[1].find("POWER-COOLING") >=0):
    #        ext = os.listdir(file)
    #        for e in ext:
    #            gatherMetricData(os.path.join(file,e))
                
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
    
    
main()