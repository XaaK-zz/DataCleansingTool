###########################################################
# RemoveUnchangingMetrics.py
# Copyright © Zach Greenvoss 
# Licensed under the MIT license - http://www.opensource.org/licenses/mit-license.php
###########################################################
import os
import sys
import datetime

runDataCollection = []
deltaCollection = []
finalDataCollection = []

def main():
    
    if (len(sys.argv) < 2):
        print("Usage: python RemoveUnchangingMetrics.py <RunData.csv> <OutputFile.csv> <Minimum Occurance>")
        quit()
    else:
        runDataFile = sys.argv[1]
    
    if (len(sys.argv) < 3):
        print("Usage: python RemoveUnchangingMetrics.py <RunData.csv> <OutputFile.csv> <Minimum Occurance>")
        quit()
    else:
        outputFile = sys.argv[2]
    
    if (len(sys.argv) < 4):
        print("Usage: python RemoveUnchangingMetrics.py <RunData.csv> <OutputFile.csv> <Minimum Occurance>")
        quit()
    else:
        minMetricDeltas = int(sys.argv[3])
         
    print "Opening RunData file: " + runDataFile
    
    fileData = open(runDataFile,"r")
    while fileData:
            line = fileData.readline()
            if line == "":
                break;
            lineData = line.split(",")
            runDataCollection.append(lineData)
    
    columnsToKeep = [0]
    
    print "Calculating Metric Deltas..."
    for column in range(2,len(runDataCollection[0]),2):
        columnCount = 0
        for row in range(1,len(runDataCollection)):
            cellData = float(runDataCollection[row][column])
            if cellData != 0.0:
                columnCount += 1
        if columnCount >= minMetricDeltas:
            columnsToKeep.append(column-1)
            columnsToKeep.append(column)
            print "Keeping " + str(column)
            
    print "Removing columns..."
    
    for runDataRow in runDataCollection:
        newRowData = []
        colIndex = 0
        print str(runDataRow[0])
        for cellData in runDataRow:
            if columnsToKeep.__contains__(colIndex):
                newRowData.append(cellData)
            colIndex += 1
        
        finalDataCollection.append(newRowData)
        
    print "Writing file..."
    fileData = open(outputFile,"w")
    for data in finalDataCollection:
        row = ""
        for rowData in data:
            if str(rowData).strip() != "":
                row = row + str(rowData.strip()) + ","
        
        fileData.write(row[0:-1] + "\n")
    fileData.close()
    
    
main()