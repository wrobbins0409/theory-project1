import csv
import itertools
import time


class DumbSAT:
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

    def __brute_force(self, formula):
        # Extract all unique literals from the given formula
        literals = set()
        for clause in formula:
            for literal in clause:
                # Use absolute values for variable names
                literals.add(abs(literal))

        literals = list(literals)
        n = len(literals)

        # Generate all combinations of truth assignments
        for seq in itertools.product([True, False], repeat=n):
            assignment = dict(zip(literals, seq))

            # Check if the current assignment satisfies the CNF
            if self.__is_satisfiable(formula, assignment):
                return True, assignment

        return False, None

    def __is_satisfiable(self, formula, assignment):
        for clause in formula:
            satisfied = False
            for literal in clause:
                # Check if any literal in the clause is satisfied by the current assignment
                if (literal > 0 and assignment[literal]) or (literal < 0 and not assignment[abs(literal)]):
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True

    def solve(self, output_file=False, verbose=False):
        if output_file:
            file = open("DumbSATresults.txt", 'w')

        for problem, formula in enumerate(self.formulas, 1):
            start = time.time()  # Start timer
            result, _ = self.__brute_force(formula)
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
