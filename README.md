DataCleansingTool
=================

This is a set of Python scripts used to cleanse and analyze the output data from the PNNL's Energy Smart Data Center Facility.
Each script is used as part of a pipeline process to get the data into an integrated and useful form for holistic analysis.

ParseMetricData.py
-This script is the first step in the pipeline.  It will parse through a directory containing the metric data and gather all metric runs into a single large csv file.  This file will have the timestamp as the first column, and the superset of all captured metrics as the columns.
-Note that this produces a fairly sparse matrix of data - as the metrics are captured at different timestamps so much of the timestamps have blank cells for the metric data

PopulateSparseData.py
-This script consumes the csv file produced by the previous script and fills in the missing components of the sparse matrix.
-It does this by analyzing each metric "column" and finding the appropriate metric reading to fill in for each timestamp.
-The output of this process is a completely filled in matrix of timestamp/metric readings

GenerateRunData.py
-This script reads the MPI measurement data from a specific run of the NWChem chemical package.
-It uses the timeslices defined in ParseMetricData.py to divide the measurement data into slices and then counts each of the MPI events occurring within each time slice.
-The final output of this script is a complete picture of the MPI calls for the NWChem application (across all nodes) for each timestamp period.  This can be directly compared with the output of PopulateSparseData.py to analyze the performance and power metric data.

CombineRunDataMetricData.py
-This combines the previous two output files into a new csv file.
-This new file will contain all the metric data for each available time slice, and will now contain all the MPI counts for the given time slice as well.

--------------------------------

Example calling sequence

Assuming the DataCleansingTool directory is installed at the same level as the extracted run data, the following commands will transform the data and output the required files into an output directory.

    DataCleansingTool: mkdir output
    DataCleansingTool: python ParseMetricData.py ../LD_A1_56p_2ppn_28n_IO-BASIC_even_RAWDATA/POWER-COOLING_perMetricPerTrial/ output/
    DataCleansingTool: python PopulateSparseData.py output/TimeData1.csv
    DataCleansingTool: python PopulateSparseData.py output/TimeData2.csv
    DataCleansingTool: python PopulateSparseData.py output/TimeData3.csv
    Note: The following commands take hours to complete...
    DataCleansingTool: python GenerateRunData.py output/TimeData1.csv ../LD_A1_56p_2ppn_28n_IO-BASIC_even_RAWDATA/t1/output/sysmpi-parsed/  output/MPIResultsTest1.csv
    DataCleansingTool: python GenerateRunData.py output/TimeData2.csv ../LD_A1_56p_2ppn_28n_IO-BASIC_even_RAWDATA/t2/output/sysmpi-parsed/ output/MPIResultsTest2.csv
    DataCleansingTool: python GenerateRunData.py output/TimeData3.csv ../LD_A1_56p_2ppn_28n_IO-BASIC_even_RAWDATA/t3/output/sysmpi-parsed/ output/MPIResultsTest3.csv
    DataCleansingTool: python CombineRunDataMetricData.py output/TimeData1.csvConverted.csv output/MPIResultsTest1.csv output/combinedData1.csv
    DataCleansingTool: python CombineRunDataMetricData.py output/TimeData2.csvConverted.csv output/MPIResultsTest2.csv output/combinedData2.csv
    DataCleansingTool: python CombineRunDataMetricData.py output/TimeData3.csvConverted.csv output/MPIResultsTest3.csv output/combinedData3.csv