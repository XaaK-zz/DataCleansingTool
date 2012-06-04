###########################################################
# MasterRun.py
# Copyright © Zach Greenvoss 
# Licensed under the MIT license - http://www.opensource.org/licenses/mit-license.php
###########################################################
import sys
import os

def main():

    minMetricDelta = 5
    
    if (len(sys.argv) < 2):
        print("Usage: python MasterRun.py [Path to Power Metric Data] [Output Path]")
        quit()
    else:
        powerMetricDir = sys.argv[1]
        print "Power Metric Directory: " + powerMetricDir
    
    if (len(sys.argv) < 3):
        print("Usage: python MasterRun.py [Path to Power Metric Data] [Output Path]")
        quit()
    else:
        outputPath = sys.argv[2]
        print "Output Directory: " + outputPath

    if (len(sys.argv) < 4):
        print("Usage: python MasterRun.py [Path to Power Metric Data] [Output Path] [Time Delta In Milliseconds]")
        quit()
    else:
        timeSliceSize = sys.argv[3]
        print "Time Slice Size: " + timeSliceSize
    
    print "Calling ParseMetricData.py"
    os.system("python ParseMetricData.py " + os.path.join(powerMetricDir,"POWER-COOLING_perMetricPerTrial") + " " + outputPath + " " + timeSliceSize)
    
    print "--------------------------------------------------------\n"
    
    print "Calling PopulateSparseData.py"
    
    os.system("python PopulateSparseData.py " + os.path.join(outputPath,"NormalizedTimeData1.csv"))
    os.system("python PopulateSparseData.py " + os.path.join(outputPath,"NormalizedTimeData2.csv"))
    os.system("python PopulateSparseData.py " + os.path.join(outputPath,"NormalizedTimeData3.csv"))
    
    print "--------------------------------------------------------\n"
    
    print "Calling GenerateRunData.py"
    
    os.system("python GenerateRunData.py " + os.path.join(outputPath,"NormalizedTimeData1.csv") + " " + os.path.join(powerMetricDir,"t1/output/sysmpi-parsed/") + " " + os.path.join(outputPath,"MPICountsRun1.csv"))
    os.system("python GenerateRunData.py " + os.path.join(outputPath,"NormalizedTimeData2.csv") + " " + os.path.join(powerMetricDir,"t2/output/sysmpi-parsed/") + " " + os.path.join(outputPath,"MPICountsRun2.csv"))
    os.system("python GenerateRunData.py " + os.path.join(outputPath,"NormalizedTimeData3.csv") + " " + os.path.join(powerMetricDir,"t3/output/sysmpi-parsed/") + " " + os.path.join(outputPath,"MPICountsRun3.csv"))
    
    print "--------------------------------------------------------\n"
    
    print "Calling CombineRunDataMetricData.py"
    
    os.system("python CombineRunDataMetricData.py " + os.path.join(outputPath,"NormalizedTimeData1.csvConverted.csv") + " " + os.path.join(outputPath,"MPICountsRun1.csv") + " " + os.path.join(outputPath,"CombinedData1.csv"))
    os.system("python CombineRunDataMetricData.py " + os.path.join(outputPath,"NormalizedTimeData2.csvConverted.csv") + " " + os.path.join(outputPath,"MPICountsRun2.csv") + " " + os.path.join(outputPath,"CombinedData2.csv"))
    os.system("python CombineRunDataMetricData.py " + os.path.join(outputPath,"NormalizedTimeData3.csvConverted.csv") + " " + os.path.join(outputPath,"MPICountsRun3.csv") + " " + os.path.join(outputPath,"CombinedData3.csv"))
    
    print "--------------------------------------------------------\n"
    print "Calling GenerateDeltas.py"
    os.system("python GenerateDeltas.py " + os.path.join(outputPath,"CombinedData1.csv") + " " + os.path.join(outputPath,"CombinedDataWithDeltas1.csv"))
    os.system("python GenerateDeltas.py " + os.path.join(outputPath,"CombinedData2.csv") + " " + os.path.join(outputPath,"CombinedDataWithDeltas2.csv"))
    os.system("python GenerateDeltas.py " + os.path.join(outputPath,"CombinedData3.csv") + " " + os.path.join(outputPath,"CombinedDataWithDeltas3.csv"))
    
    print "--------------------------------------------------------\n"
    print "Calling RemoveUnchangingMetrics.py"
    os.system("python RemoveUnchangingMetrics.py " + os.path.join(outputPath,"CombinedDataWithDeltas1.csv") + " " + os.path.join(outputPath,"FinalOutput1.csv") + " " + str(minMetricDelta))
    os.system("python RemoveUnchangingMetrics.py " + os.path.join(outputPath,"CombinedDataWithDeltas2.csv") + " " + os.path.join(outputPath,"FinalOutput2.csv") + " " + str(minMetricDelta))
    os.system("python RemoveUnchangingMetrics.py " + os.path.join(outputPath,"CombinedDataWithDeltas3.csv") + " " + os.path.join(outputPath,"FinalOutput3.csv") + " " + str(minMetricDelta))

main()