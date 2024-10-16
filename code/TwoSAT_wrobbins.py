import random
import csv
import time


class TwoSAT:
    def __init__(self, fileName):
        self.formulas = self.__read_cnf_csv(fileName)
        self.satisfiableArray = []
        self.timeArray = []

    def __read_cnf_csv(self, file_name):
        formulas = []
        current_formula = []

        with open(file_name, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)

            for line in csv_reader:
                # Skip any empty lines
                if not line or all(col == '' for col in line):
                    continue

                # Process comment lines
                if line[0].startswith('c'):
                    # Start a new formula if there's an existing one
                    if current_formula:
                        formulas.append(current_formula)
                        current_formula = []
                    continue

                # Process the problem line
                if line[0].startswith('p'):
                    continue  # We can ignore the problem line in this context

                # Process clause lines
                clause = [int(literal)
                          for literal in line if literal and literal != '0']
                if clause:  # Only add non-empty clauses
                    current_formula.append(tuple(clause))

            # Append the last formula if any
            if current_formula:
                formulas.append(current_formula)

        return formulas

    def __select_literal(self, cnf):
        for c in cnf:
            for literal in c:
                return abs(literal)

    def __dpll(self, cnf, assignments={}):

        if len(cnf) == 0:
            return True, assignments

        if any([len(c) == 0 for c in cnf]):
            return False, None

        l = self.__select_literal(cnf)

        new_cnf = [c for c in cnf if l not in c]
        new_cnf = [set(c).difference({-l}) for c in new_cnf]
        sat, vals = self.__dpll(new_cnf, {**assignments, **{l: True}})
        if sat:
            return sat, vals

        new_cnf = [c for c in cnf if -l not in c]
        new_cnf = [set(c).difference({l}) for c in new_cnf]
        sat, vals = self.__dpll(new_cnf, {**assignments, **{l: False}})
        if sat:
            return sat, vals

        return False, None

    def solve(self, output_file=False, verbose=False):
        if output_file:
            file = open("TwoSATresults.txt", 'w')

        for problem, formula in enumerate(self.formulas, 1):
            start = time.time()  # Start timer
            result, _ = self.__dpll(formula)
            end = time.time()  # End timer
            exec_time = int((end-start)*1e6)
            if verbose:
                output_string = f"Problem: {problem} Result: {'S' if result else 'U'} Execution time: {exec_time} us"
                print(output_string)
            if output_file:
                file.write(output_string+'\n')
            self.satisfiableArray.append(result)
            self.timeArray.append(exec_time)

    def getSatisfiableArray(self):
        return self.satisfiableArray

    def getTimeArray(self):
        return self.timeArray
