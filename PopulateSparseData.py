import os
import sys

fileDataCollection = []

def getFirstValueInColumn(col):
    for y in range(1,len(fileDataCollection)):          #skip the first row
        if str(fileDataCollection[y][col]).strip() != "":
            return fileDataCollection[y][col]
    
    return -10000

def main():
    
    print "Opening file..."
    
    if (len(sys.argv) < 1):
        print("Please provide a file name to parse.")
        quit()
    
    fileData = open(sys.argv[1],"r")
    index = 0
    while fileData:
            line = fileData.readline()
            if line == "":
                break;
            lineData = line.split(",")
            fileDataCollection.append(lineData)
            index += 1
    
    print "\nLoaded into memory..."
     
    for x in range(1,len(fileDataCollection[0])):   #skip time series column
    #for x in range(1,3):   #skip time series column
        currentSavedValue = -10000
        if str(fileDataCollection[0][x]).strip() == "":
            #end of columns
            break
        for y in range(1,len(fileDataCollection)):          #skip the first row
            #print "Column: " + str(x) + " Row: " + str(y)
            if str(fileDataCollection[y][x]).strip()  == "" and currentSavedValue != -10000:
                #blank value - have found a value already
                fileDataCollection[y][x] = currentSavedValue
                #print "Applying saved value - " + str(currentSavedValue)
            elif str(fileDataCollection[y][x]).strip() == "" and currentSavedValue == -10000:
                #need to get the value for this from the "future"
                currentSavedValue = getFirstValueInColumn(x)
                #print "get first value value - " + str(currentSavedValue)
                if currentSavedValue == -10000:
                    print "Failed to find future value for " + str(x) + ":" + str(y)
                    quit()
                fileDataCollection[y][x] = currentSavedValue
            elif str(fileDataCollection[y][x]).strip()  != "":
                currentSavedValue = fileDataCollection[y][x]
                #print "new column value - " + str(currentSavedValue).strip() + "."
                
    
    print "Writing file..."
    fileData = open(sys.argv[1] + "Converted.csv","w")
    for data in fileDataCollection:
        for rowData in data:
            if str(rowData).strip() == "":
                fileData.write(str(rowData))
            else:
                fileData.write(str(rowData) + ",")
    fileData.close()
    
main()
