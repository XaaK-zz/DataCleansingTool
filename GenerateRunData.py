import os
import sys
import datetime

runData = []
timeSlices = []
finalMPIData = []

def readFile(file):
    tempCollection = []
    fileData = open(file,"r")
    fileData.readline() #skip first line
    while True:
        lineData = fileData.readline()
        if(lineData == ""):
            break
        splitData = lineData.strip().split(" ")
        #print str([splitData[0],splitData[1][1:] + " " + splitData[2][:-1]])
        tempCollection.append([splitData[0],
                               datetime.datetime.strptime(splitData[1][1:] + " " + splitData[2][:-1],"%Y-%m-%d %H:%M:%S.%f")])
    fileData.close()
    runData.append(tempCollection)

def main():

    if (len(sys.argv) < 2):
        print("Please provide a file name to parse for the time slices...")
        quit()
    else:
        print("Reading time slices from: " + sys.argv[1])
    
    if (len(sys.argv) < 3):
        print("Please provide a directory containing .cg files (NWChem result files)...")
        quit()
    else:
        print("Reading NWChem result files from: " + sys.argv[2])
        
    if (len(sys.argv) < 4):
        print("Please provide an output file name...")
        quit()
    else:
        print("Writing results to: " + sys.argv[3])
    
    print "Analyzing time slices..."

    fileData = open(sys.argv[1],"r")
    fileData.readline() #skip first line
    while True:
        lineData = fileData.readline()
        if(lineData == ""):
            break
        data = lineData.split(",")[0]
        timeSlices.append(datetime.datetime.strptime(data,"%Y-%m-%d %H:%M:%S.%f"))
            
    print "Gathering data from files located in " + os.path.join(os.getcwd(),sys.argv[2])
    
    files = os.listdir(os.path.join(os.getcwd(),sys.argv[2]))
    
    #Loop through files
    for file in files:
        if os.path.isfile(os.path.join(sys.argv[2],file)) and os.path.splitext(file)[1] == ".cg":
            print "Adding " + str(file)
            readFile(os.path.join(sys.argv[2],file))
    
    currentBottomTime = datetime.datetime(1900,1,1)
    currentTopTime = timeSlices[0]
    
    MPIBarrierCount = 0
    MPISend = 0
    MPIBCast = 0
    MPIAllGather = 0
    MPIAllReduce = 0
    MPIRecv = 0
    
    print "Placing data into time slices"
    for timeSlice in timeSlices:
        MPIBarrierCount = 0
        MPISend = 0
        MPIBCast = 0
        MPIAllGather = 0
        MPIAllReduce = 0
        MPIRecv = 0
        currentTopTime = timeSlice
        print "Time Slice: " + str(timeSlice)
        for rankData in runData:
            for metricData in rankData:
                if metricData[1] > currentBottomTime and metricData[1] <= currentTopTime:
                    #inside time slice
                    #add to counts
                    if metricData[0] == "MPI_Barrier":
                        MPIBarrierCount += 1
                    elif metricData[0] == "MPI_Send":
                        MPISend += 1
                    elif metricData[0] == "MPI_Bcast":
                        MPIBCast += 1
                    elif metricData[0] == "MPI_Allgather":
                        MPIAllGather += 1
                    elif metricData[0] == "MPI_Allreduce":
                        MPIAllReduce += 1
                    elif metricData[0] == "MPI_Recv":
                        MPIRecv += 1
                    else:
                        print "Unknown value - " + metricData[0]
                        quit()
                elif metricData[1] > currentBottomTime and metricData[1] > currentTopTime:
                    #outside time slice
                    break
        #done with rank data for timeslice
        #add counts into collections
        finalMPIData.append([currentTopTime,MPISend,MPIRecv,MPIBCast,MPIAllGather,MPIAllReduce,MPIBarrierCount])
        #update timeslice top/bottom
        currentBottomTime = timeSlice
        
    print "Writing data..."
    #fileData = open("MPIMetrics.csv","w")
    fileData = open(sys.argv[3],"w")
    fileData.write("Time,MPI_Send,MPI_Recv,MPI_Bcast,MPI_Allgather,MPI_Allreduce,MPI_Barrier\n")
    for data in finalMPIData:
        for mpiData in data:
            fileData.write(str(mpiData) + ", ")
        fileData.write("\n")
    
    fileData.close()
    
main()