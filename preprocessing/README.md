# Anomaly detection and removal for DSCOVR data

These scripts are used to process the raw CSV files from DSCOVR and remove anomalies.  To assess the quality of the scripts some processing is carried out on the data to plot the mean and standard deviation of the Faraday cup data.

## mean\_std\_dev.py

The CSV data from DSCOVR presents 50 columns of data from the Faraday cup.  This script treats these as a histogram with uniform bin size and claculates the mean and standard deviation for each line in the CSV.  This should give two line plots which are related to the velocity and the volume of solar wind detected.  These two lines can then be plotted agains sample number to give a visual representation of the data.

## anomalies2.py

This script uses SKLearn to train an anomaly detector to classify data as part of the dataset or an outlier.  At the moment it then processes the same data again one line at a time classifying each data point.  Points that are found to be outliers are zeroed out.

# Analysis

This does seem to be working but the tuning is not great.  A few anomalies are still getting through and there are several cases where valid data are zeroed out.
