import math, time
from test_cases import cases
from old_test_cases import cases as otc
from scipy.optimize import linprog

class SimplexSolver():
    ''' Solves linear programs using simplex algorithm
    '''
    def __init__(self):
        self.A = []
        self.b = []
        self.c = []
        self.tableau = []
        self.entering = []
        self.departing = []
        self.ineq = []
        self.prob = "max"

    def run_simplex(self, A, b, c, prob='max', ineq=[],
                    enable_msg=False, latex=False):
        ''' Run simplex algorithm.
        '''
        self.prob = prob

        # Add slack & artificial variables
        self.set_simplex_input(A, b, c)
            
        # Are there any negative elements on the bottom (disregarding
        # right-most element...)
        while (not self.should_terminate()):
            # ... if so, continue.

            # Attempt to find a non-negative pivot.
            pivot = self.find_pivot()
            if pivot[1] < 0:
                if (enable_msg):
                    print ("There exists no non-negative pivot. "
                           "Thus, the solution is infeasible.")
                return None

            # Do row operations to make every other element in column zero.
            self.pivot(pivot)

        solution = self.get_current_solution()
        return solution
        
    def set_simplex_input(self, A, b, c):
        ''' Set initial variables and create tableau.
        '''
        # Convert all entries to fractions for readability.
        for a in A:
            self.A.append([x for x in a])    
        self.b = [x for x in b]
        self.c = [x for x in c]
        if not self.ineq:
            if self.prob == 'max':
                self.ineq = ['<='] * len(b)
            elif self.prob == 'min':
                self.ineq = ['>='] * len(b)
            
        self.update_enter_depart(self.get_Ab())

        # If this is a minimization problem...
        if self.prob == 'min':
            # ... find the dual maximum and solve that.
            m = self.get_Ab()
            m.append(self.c + [0])
            m = [list(t) for t in zip(*m)] # Calculates the transpose
            self.A = [x[:(len(x)-1)] for x in m]
            self.b = [y[len(y) - 1] for y in m]
            self.c = m[len(m) -1]
            self.A.pop()
            self.b.pop()
            self.c.pop()
            self.ineq = ['<='] * len(self.b)

        self.create_tableau()
        self.ineq = ['='] * len(self.b)
        self.update_enter_depart(self.tableau)

    def update_enter_depart(self, matrix):
        self.entering = []
        self.departing = []
        # Create tables for entering and departing variables
        for i in range(0, len(matrix[0])):
            if i < len(self.A[0]):
                prefix = 'x' if self.prob == 'max' else 'y'
                self.entering.append("%s_%s" % (prefix, str(i + 1)))
            elif i < len(matrix[0]) - 1:
                self.entering.append("s_%s" % str(i + 1 - len(self.A[0])))
                self.departing.append("s_%s" % str(i + 1 - len(self.A[0])))
            else:
                self.entering.append("b")

    def add_slack_variables(self):
        ''' Add slack & artificial variables to matrix A to transform
            all inequalities to equalities.
        '''
        slack_vars = self._generate_identity(len(self.tableau))
        for i in range(0, len(slack_vars)):
            self.tableau[i] += slack_vars[i]
            self.tableau[i] += [self.b[i]]

    def create_tableau(self):
        ''' Create initial tableau table.
        '''
        self.tableau = [[x for x in y] for y in self.A]
        self.add_slack_variables()
        c = [x for x in self.c]
        for index, value in enumerate(c):
            c[index] = -value
        self.tableau.append(c + [0] * (len(self.b)+1))

    def find_pivot(self):
        ''' Find pivot index.
        '''
        enter_index = self.get_entering_var()
        depart_index = self.get_departing_var(enter_index)
        return [enter_index, depart_index]

    def pivot(self, pivot_index):
        ''' Perform operations on pivot.
        '''
        j,i = pivot_index

        pivot = self.tableau[i][j]
        self.tableau[i] = [element / pivot for
                           element in self.tableau[i]]
        for index, row in enumerate(self.tableau):
           if index != i:
              row_scale = [y * self.tableau[index][j]
                          for y in self.tableau[i]]
              self.tableau[index] = [x - y for x,y in
                                     zip(self.tableau[index],
                                         row_scale)]

        self.departing[i] = self.entering[j]
        
    def get_entering_var(self):
        ''' Get entering variable by determining the 'most negative'
            element of the bottom row.
        '''
        bottom_row = self.tableau[len(self.tableau) - 1]
        most_neg_ind = 0
        most_neg = bottom_row[most_neg_ind]
        for index, value in enumerate(bottom_row):
            if value < most_neg:
                most_neg = value
                most_neg_ind = index
        return most_neg_ind
            

    def get_departing_var(self, entering_index):
        ''' To calculate the departing variable, get the minimum of the ratio
            of b (b_i) to the corresponding value in the entering collumn. 
        '''
        skip = 0
        min_ratio_index = -1
        min_ratio = 0
        for index, x in enumerate(self.tableau):
            if x[entering_index] != 0 and x[len(x)-1]/x[entering_index] > 0:
                skip = index
                min_ratio_index = index
                min_ratio = x[len(x)-1]/x[entering_index]
                break
        
        if min_ratio > 0:
            for index, x in enumerate(self.tableau):
                if index > skip and x[entering_index] > 0:
                    ratio = x[len(x)-1]/x[entering_index]
                    if min_ratio > ratio:
                        min_ratio = ratio
                        min_ratio_index = index
        
        return min_ratio_index

    def get_Ab(self):
        ''' Get A matrix with b vector appended.
        '''
        matrix = [[x for x in y] for y in self.A]
        for i in range(0, len(matrix)):
            matrix[i] += [self.b[i]]
        return matrix

    def should_terminate(self):
        ''' Determines whether there are any negative elements
            on the bottom row
        '''
        result = True
        index = len(self.tableau) - 1
        for i, x in enumerate(self.tableau[index]):
            if x < 0 and i != len(self.tableau[index]) - 1:
                result = False
        return result

    def get_current_solution(self):
        ''' Get the current solution from tableau.
        '''
        solution = {}
        for x in self.entering:
            if x != 'b':
                if x in self.departing:
                    solution[x] = self.tableau[self.departing.index(x)]\
                                  [len(self.tableau[self.departing.index(x)])-1]
                else:
                    solution[x] = 0
        solution['z'] = self.tableau[len(self.tableau) - 1]\
                          [len(self.tableau[0]) - 1]
        
        # If this is a minimization problem...
        if (self.prob == 'min'):
            # ... then get x_1, ..., x_n  from last element of
            # the slack columns.
            bottom_row = self.tableau[len(self.tableau) - 1]
            for v in self.entering:
                if 's' in v:
                    solution[v.replace('s', 'x')] = bottom_row[self.entering.index(v)]    

        return solution

    def _generate_identity(self, n):
        ''' Helper function for generating a square identity matrix.
        '''
        I = []
        for i in range(0, n):
            row = []
            for j in range(0, n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            I.append(row)
        return I

def minimum_transportation_price(suppliers, consumers, costs):
    # Build the standard optimization problem form
    c = []
    for row in costs:
        for el in row:
            c.append(el)
    
    b = []
    for supp in suppliers:
        b.append(supp)
        #b.append(-supp)
    for cons in consumers:
        b.append(cons)
        #b.append(-cons)
        
    # We need a constraint for total quantity
    b.append(sum(suppliers))
    #b.append(-sum(suppliers))

    A = []
    # Build the supplier constraint rows
    zeros = [0]*len(consumers)
    ones = [1]*len(consumers)
    for i in range(len(suppliers)):
        row = []
        for j in range(len(suppliers)):
            if i == j:
                row.extend(ones)
            else:
                row.extend(zeros)
        A.append(row)
        antirow = [-x for x in row]
        #A.append(antirow)

    # Next, the consumer constraint rows
    for i in range(len(consumers)):
        row = []
        for j in range(len(suppliers)):
            for k in range(len(consumers)):
                if i == k:
                    row.append(1)
                else:
                    row.append(0)
                    
        A.append(row)
        antirow = [-x for x in row]
        #A.append(antirow)

    A.append([1]*len(consumers)*len(suppliers))
    #A.append([-1]*len(consumers)*len(suppliers))
    #sol = SimplexSolver().run_simplex(A,b,c,prob='min',enable_msg=False,latex=False)
    sol = linprog(c, A_eq=A, b_eq=b)

    if sol.x is None:
        return 999999999
    
    z = round(sol.fun)
    xsum = sum([round(x) for x in sol.x])
    print(f'Some summary stats. z:{z}, xs:{sol.x}, sum:{xsum}, constraint:{sum(suppliers)}, other constraint:{sum(consumers)}')

    return z

def assert_equals(a, b):
    if a != b:
        print(f'ERROR: {a} does not equal {b}.')

def run_test_case(s, c, cs, exp):
    print(f'Running test case with size {len(s)}')
    start = time.time()
    assert_equals(minimum_transportation_price(s, c, cs), exp)
    end = time.time()
    print(f'Test case took: {end - start} seconds.')

def sample_tests():
    # for (suppliers, consumers, costs, expected) in cases:
    #     run_test_case(suppliers, consumers, costs, expected)
    #     
    for (suppliers, consumers, costs, expected) in otc:
        run_test_case(suppliers, consumers, costs, expected)

if __name__ == '__main__':
    sample_tests()
