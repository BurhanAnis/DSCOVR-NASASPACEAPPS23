"""
NAME:
    mean_std_dev.py - Calculate mean and standard deviation from DSCOVR data

SYNOPSIS:
    mean_std_dev.py [OPTIONS] <INPUT_FILE> <OUTPUT_FILE>

DESCRIPTION:
    Calculates the mean and standard deviation of faraday cup histogram
    data from a DSCOVR raw data file.
    
    -h, --help
        Show this help and exit
    -s, --strip
        Strip the first 4 columns off the input data
"""

import numpy as np
import sys
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs", ("help", "strip"))
except getopt.GetoptError as err:
    print(f"{sys.argv[0]}: {err!s}")
    print(f"Try '{sys.argv[0]} --help' for more information")
    sys.exit(-1)

strip = False

for o, a in opts:
    if o in ('-s', '--strip'):
        strip = True
    if o in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)

if len(args) != 2:
    print(f"There are two required filenames")
    print(f"Try '{sys.argv[0]} --help' for more information")
    sys.exit(-2)

infile = args[0]
outfile = args[1]

data = np.genfromtxt(infile, delimiter=',')
if strip:
    data = data[:,4:]

print(data.shape)

mids = 0.5 + np.linspace(0,data.shape[1])

op = []
for x in data:
    if np.sum(x) == 0:
        mean = 0
        var = 0
    else:
        mean = np.average(mids, weights=x)
        var = np.average((mids-mean)**2, weights=x)
    op.append([mean, var])

with open(outfile, "w") as fw:
    for l in op:
        fw.write(",".join([str(x) for x in l]) + "\n")
