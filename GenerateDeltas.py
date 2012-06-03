import os
import sys
import datetime

runDataCollection = []
deltaCollection = []
finalDataCollection = []

def main():
    
    if (len(sys.argv) < 2):
        print("Usage: python GenerateDeltas.py <RunData.csv> <OutputFile.csv>")
        quit()
    else:
        runDataFile = sys.argv[1]
    
    if (len(sys.argv) < 3):
        print("Usage: python GenerateDeltas.py <RunData.csv> <OutputFile.csv>")
        quit()
    else:
        outputFile = sys.argv[2]
        
    print "Opening RunData file: " + runDataFile
    
    fileData = open(runDataFile,"r")
    while fileData:
            line = fileData.readline()
            if line == "":
                break;
            lineData = line.split(",")
            runDataCollection.append(lineData)
    
    print "Calculating Deltas..."
    for row in range(1,len(runDataCollection)):
        deltaCollectionRow = []
        for column in range(1,len(runDataCollection[row])):
            cellData = runDataCollection[row][column]
            #print "Row: " + str(row) + " Column: " + str(column) + " Data: " + str(cellData)
            if row == 1:
                delta = 0
            else:
                previousCellData = runDataCollection[row-1][column]
                #print "Row: " + str(row) + " Column: " + str(column) + " previousCellData: " + str(previousCellData)
                delta = float(cellData) - float(previousCellData)
            deltaCollectionRow.append(delta)
        
        deltaCollection.append(deltaCollectionRow)
        
    print "Combining data..."
    
    
    rowIndex = 0
    for runDataRow in runDataCollection:
        newRowData = []
        colIndex = 0
        if rowIndex == 0:
            #First row - add new columns of data
            for cellData in runDataRow:
                newRowData.append(cellData)
                if colIndex > 0 and cellData.strip() != "":
                    if cellData[-1] == "\n":
                        newRowData.append(cellData[0:-1] + "_Delta\n")
                    else:
                        newRowData.append(cellData + "_Delta")
                colIndex += 1
        else:
            #subsequent rows - add deltas
            deltaRow = deltaCollection[rowIndex-1]
            for cellData in runDataRow:
                newRowData.append(cellData)
                if colIndex > 0:
                    newRowData.append(str(deltaRow[colIndex-1]))
                colIndex += 1
        finalDataCollection.append(newRowData)
        rowIndex += 1
        
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