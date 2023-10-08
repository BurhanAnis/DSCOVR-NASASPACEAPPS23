"""
NAME:
    anomalies2.py - A tool for finding and removing bad data from DSCOVR

SYNOPSIS:
    anomalies2.py [OPTIONS] <INPUT_FILE> <OUTPUT_FILE>

DESCRIPTION:
    Reads an input file of raw CSV data from DSCOVR and looks for anomalies
    in the faraday cup instrument.  Any lines found to be anomolous are
    set to zero and the file written out again.

    -h, --help
        Show this help and exit
    -a, --a=ALGORITHM
        Selects the outlier algorithm supported ALGORITHMs are:
            oneclasssvm
            elliptic [default]
"""

import sys
import getopt
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
import numpy as np

try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:", ("help", "algorithm="))
except getopt.GetoptError as err:
    print(f"{sys.argv[0]}: {err!s}")
    print(f"Try '{sys.argv[0]} --help' for more information")
    sys.exit(-1)

algorithm = "elliptic"

for o, a in opts:
    if o in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    elif o in ("-a", "--algorithm"):
        algorithm = a

if len(args) != 2:
    print("Two filenames are required arguments")
    print("Try '{sys.argv[0]} --help' for more information")
    sys.exit(-1)

input_file = args[0]
output_file = args[1]

if algorithm == "elliptic":
    al = EllipticEnvelope(contamination=0.1, random_state=42)
elif algorithm == "oneclasssvm":
    al = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)

training_data = np.genfromtxt(input_file, delimiter=',')
training_data = training_data[:,4:]

al.fit(training_data)

op = []
for x in training_data:
    if al.predict(x.reshape(1, -1)) == 1:
        op.append(x)
    else:
        op.append(np.zeros(x.shape))

with open(output_file, "w") as fw:
    for d in op:
        fw.write(",".join([str(x) for x in list(d)]) + "\n")