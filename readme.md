Ceres is a asteroid mining data analysis tool which sanitizes and interprets drilling data provided to it in the form of .csv files. Sanitized .csv files are generated, replacing bad data erroniously placed in the given csv files with acceptable filler data which is generated from the values of its neighbors. Ceres then uses these sanitized csv files to create Run instances in python, which contain a number of statistics about each run. Finally, the CSVMain script in Ceres provides an out-of-the box way to get the average efficiency of any bits.