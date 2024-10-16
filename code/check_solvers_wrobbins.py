from DumbSAT_wrobbins import DumbSAT
from TwoSAT_wrobbins import TwoSAT
import pandas as pd

import csv

# Initialize an empty list to store the 'U' or 'S' values
real_result = []

# Open the CSV file
with open('../data/check_kSAT_wrobbins.cnf.csv', 'r',  encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)

    # Iterate through the rows of the CSV
    for row in csv_reader:
        # Check if the row starts with 'c'
        if row[0] == 'c':
            # Append the 4th element ('U' or 'S') to the result list
            if row[3] == 'S':
                real_result.append(True)
            else:
                real_result.append(False)

# initialize satSolver to the TwoSAT class
fastSolver = TwoSAT('../data/check_kSAT_wrobbins.cnf.csv')

# solve the file with known satisfiability
fastSolver.solve()

# Get the satsifiability array from the TwoSAT class
fastResult = fastSolver.getSatisfiableArray()

file = open("../output/output_TwoSAT_check.txt", 'w')

# Compare the results of the TwoSAT class with the known satisfiability
if fastResult == real_result:
    file.write("TwoSAT: Pass")
else:
    file.write("TwoSAT: Fail")
