###########################################################
# FindHighestChangingMetrics.py
# Copyright © Zach Greenvoss 
# Licensed under the MIT license - http://www.opensource.org/licenses/mit-license.php
###########################################################
import os
import sys
import datetime
import operator
import matplotlib.pyplot as plt
import numpy
import matplotlib

runDataCollection = []
deltaCollection = []
finalDataCollection = []
formatList = ["b-","g-"]
        
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)

def f(data):
    return datetime.datetime.strptime(str(data),"%Y-%m-%d %H:%M:%S.%f")
    
def main():
    
    if (len(sys.argv) < 2):
        print("Usage: python FindHighestChangingMetrics.py <RunData.csv> <OutputDir.csv> <Number Of Metrics To Keep>")
        quit()
    else:
        runDataFile = sys.argv[1]
    
    if (len(sys.argv) < 3):
        print("Usage: python FindHighestChangingMetrics.py <RunData.csv> <OutputDir.csv> <Number Of Metrics To Keep>")
        quit()
    else:
        outputDir = sys.argv[2]
    
    if (len(sys.argv) < 4):
        print("Usage: python FindHighestChangingMetrics.py <RunData.csv> <OutputDir.csv> <Number Of Metrics To Keep>")
        quit()
    else:
        metricCount = int(sys.argv[3])
         
    print "Opening RunData file: " + runDataFile
    
    runDataCollection = []
    fileData = open("FinalOutput/ProjectData/LD_output_1000ms/NormalizedTimeData3.csv","r")
    while fileData:
            line = fileData.readline()
            if line == "":
                break;
            lineData = line.split(",")
            runDataCollection.append(lineData)
    fileData.close()
    print(len(runDataCollection))
    
    runDataCollectionX = numpy.array(runDataCollection)
    timeList = map(f,runDataCollectionX[1:,0])
    
    mpiSendIndex = runDataCollection[0].index("MPI_Send")
    mpiRecvIndex = runDataCollection[0].index("MPI_Recv")
    
    columnsToKeep = [0]
    columnCountDict = {}
    
    print "Calculating Metric Deltas..."
    for column in range(2,mpiSendIndex-1,2):
        columnCount = 0
        for row in range(1,len(runDataCollectionX)):
            cellData = float(runDataCollectionX[row][column])
            if cellData != 0.0:
                columnCount += 1
         
        columnCountDict[column] = columnCount;
        
    print "Building charts..."
    for x in range(0,metricCount):
        
        fig = plt.figure()
        fig.subplots_adjust(right=0.75)
        host = fig.add_subplot(111)
        p1, = host.plot_date(x=matplotlib.dates.date2num(timeList),y=runDataCollectionX[1:,mpiSendIndex],fmt="k-",label=str(runDataCollectionX[0,mpiSendIndex]),
                             alpha=.25)
        host.set_xlabel("Time")
        host.set_ylabel(str(runDataCollectionX[0,mpiSendIndex]))
        
        index = 0
        savedColumns = []
        for column in sorted(columnCountDict.iteritems(), key=operator.itemgetter(1),reverse=True):
            savedColumns.append(column[0])
            parX = host.twinx()
            if index > 0:
                parX.spines["right"].set_position(("axes",index * 1.2))
                make_patch_spines_invisible(parX)
                parX.spines["right"].set_visible(True)
            p2, = parX.plot_date(x=matplotlib.dates.date2num(timeList),y=runDataCollectionX[1:,column[0]-1],fmt=formatList[index],label=str(runDataCollectionX[0,column[0]-1]))
            parX.set_ylabel(str(runDataCollectionX[0,column[0]-1]))
            parX.yaxis.label.set_color(p2.get_color())
            
            index += 1
            if index >= 2:
                break
        
        plt.savefig(os.path.join(outputDir,str(x) + ".png"))
        for savedColumn in savedColumns:
            columnCountDict.pop(savedColumn)
    
main()