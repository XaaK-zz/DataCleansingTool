import sys
import os

def main():

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
    
    os.system("python CombineRunDataMetricData.py " + os.path.join(outputPath,"NormalizedTimeData1.csvConverted.csv") + " " + os.path.join(outputPath,"MPICountsRun1.csv") + " " + os.path.join(outputPath,"FinalOutput1.csv"))
    os.system("python CombineRunDataMetricData.py " + os.path.join(outputPath,"NormalizedTimeData2.csvConverted.csv") + " " + os.path.join(outputPath,"MPICountsRun2.csv") + " " + os.path.join(outputPath,"FinalOutput2.csv"))
    os.system("python CombineRunDataMetricData.py " + os.path.join(outputPath,"NormalizedTimeData3.csvConverted.csv") + " " + os.path.join(outputPath,"MPICountsRun3.csv") + " " + os.path.join(outputPath,"FinalOutput3.csv"))
    

main()