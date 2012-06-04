DataCleansingTool
=================

This is a set of Python scripts used to cleanse and analyze the output data from the PNNL's Energy Smart Data Center Facility.
Each script is used as part of a pipeline process to get the data into an integrated and useful form for holistic analysis.

MasterRun.py
-This will run all of the scripts below in a pipeline.
-It will handle the intermediary steps and call each script with the appropriate parameters.

ParseMetricData.py
-This script is the first step in the pipeline.  It will parse through a directory containing the metric data and gather all metric runs into a single large csv file.  This file will have the timestamp as the first column, and the superset of all captured metrics as the columns.
-Note that this produces a fairly sparse matrix of data - as the metrics are captured at different timestamps so much of the timestamps have blank cells for the metric data
-The user has the ability to specify the size of the time slices.  This is done with an additional parameter of milliseconds.

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

GenerateDeltas.py
-This iterates over the previous file and finds all the deltas for each metric.
-These deltas are output to a new column added to each metric column.

RemoveUnchangingMetrics.py
-This will drop any metric columns that do not have a minimum number of deltas.
-This will produce a new output file with only "interesting" metrics retained.

FindHighestChangingMetrics.py
-This will find the highest changing metrics and produce a set of charts for them.
-Note this script requires both the numpy and matplotlib third party libraries to use.
