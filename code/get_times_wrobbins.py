from DumbSAT_wrobbins import DumbSAT
from TwoSAT_wrobbins import TwoSAT
import pandas as pd

# check to make sure they both get same results

# twosat
fastSolver = TwoSAT("check_2SAT_wrobbins.csv")
fastSolver.solve(output_file=True)
fastAnswers = fastSolver.getSatisfiableArray()

# dumbsat
slowSolver = DumbSAT("check_2SAT_wrobbins.csv")
slowSolver.solve(output_file=True)
slowAnswers = slowSolver.getSatisfiableArray()

# show that the answers are the same meaning that the 2SAT solver is working correctly
if fastAnswers == slowAnswers:
    print("Both solvers returned the same answers")
else:
    print("Solvers returned different answers")

# save the execution times for each SAT solver as csv to load into notebook to graph
fastTimes = fastSolver.getTimeArray()
slowTimes = slowSolver.getTimeArray()

# save as df to save as csv
df = pd.DataFrame({'TwoSAT': fastTimes, 'DumbSAT': slowTimes})
df.to_csv('times.csv', index=False)
