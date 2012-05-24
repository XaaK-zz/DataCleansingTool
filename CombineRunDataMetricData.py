import os
import sys
import datetime

timeDataCollection = []
mpiResults = []

def main():
    
    if (len(sys.argv) < 2):
        print("Usage: python CombineRunDataMetricData.py <TimeData.csv> <MPIResults.csv> <OutputFile.csv>")
        quit()
    else:
        timeDataFile = sys.argv[1]
    
    if (len(sys.argv) < 3):
        print("Usage: python CombineRunDataMetricData.py <TimeData.csv> <MPIResults.csv> <OutputFile.csv>")
        quit()
    else:
        mpiResultsFile = sys.argv[2]
    
    if (len(sys.argv) < 4):
        print("Usage: python CombineRunDataMetricData.py <TimeData.csv> <MPIResults.csv> <OutputFile.csv>")
        quit()
    else:
        outputFile = sys.argv[3]
        
    print "Opening TimeData file: " + timeDataFile
    
    fileData = open(timeDataFile,"r")
    while fileData:
            line = fileData.readline()
            if line == "":
                break;
            lineData = line.split(",")
            timeDataCollection.append(lineData)
    
    print "Opening MPI Results file: " + mpiResultsFile
    
    fileData = open(mpiResultsFile,"r")
    while fileData:
            line = fileData.readline()
            if line == "":
                break;
            lineData = line.split(",")
            mpiResults.append(lineData)
    
    newCollection = []
    
    print "Adding MPI data into time data..."
    index = 0
    for timeDataRow in timeDataCollection:
        mpiData = mpiResults[index]
        try:
            if index > 0 and datetime.datetime.strptime(mpiData[0],"%Y-%m-%d %H:%M:%S.%f") != datetime.datetime.strptime( timeDataRow[0],"%Y-%m-%d %H:%M:%S.%f"):
                print "timestamps not equal..." + str(mpiData[0]) + " - " + str(timeDataRow[0])
                quit()
        except ValueError:
            #when the MPI results are written out the datetime formatting will drop the milliseconds if they equal 000
            #   This catch will re-compare with the date format only down to seconds
            if index > 0 and datetime.datetime.strptime(mpiData[0],"%Y-%m-%d %H:%M:%S") != datetime.datetime.strptime( timeDataRow[0],"%Y-%m-%d %H:%M:%S.%f"):
                print "timestamps not equal..." + str(mpiData[0]) + " - " + str(timeDataRow[0])
                quit()

        index += 1
        #for mpiDataItem in mpiData:
        for x in range(1,len(mpiData)): #skip time attribute
            mpiDataItem = mpiData[x]
            if mpiDataItem.strip() != "":
                if mpiDataItem[-1] == "\n":
                    timeDataRow.append(mpiDataItem[0:-1])
                else:
                    timeDataRow.append(mpiDataItem)
        
        newCollection.append(timeDataRow)
        
    print "Writing file..."
    fileData = open(outputFile,"w")
    for data in newCollection:
        row = ""
        for rowData in data:
            if str(rowData).strip() != "":
                #fileData.write(str(rowData.strip()))
                #row = row + str(rowData.strip())
            #else:
                #fileData.write(str(rowData.strip()) + ",")
                row = row + str(rowData.strip()) + ","
        
        fileData.write(row[0:-1] + "\n")
    fileData.close()
    
    
main()