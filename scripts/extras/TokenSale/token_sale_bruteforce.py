from math import floor
import numpy as np
import pandas as pd

# make list to optimize
best_vals = {'ideal_overflow':[], 'ideal_overflow_multiplier':[], 'loop_range':[]}

# minimizing for the remainder gas to send
overflow_computation = lambda x: (floor(int(int(2**256)*x) // int(1e18)) + 1) * int(1e18) % int(int(2**256))
np_overflow_computation = np.vectorize(overflow_computation)

# loop a bunch of times
for i in range(1, 200):
    range_to_test = np.arange(i*int(5e5), (i+1)*int(5e5), 1)
    tested_range = np_overflow_computation(range_to_test)
    ideal_overflow = np.min(tested_range)
    ideal_overflow_multiplier = np.where(tested_range == ideal_overflow)

    # construct csv
    best_vals['ideal_overflow'].append(ideal_overflow)
    best_vals['ideal_overflow_multiplier'].append(range_to_test[ideal_overflow_multiplier][0])
    best_vals['loop_range'].append((np.min(range_to_test), np.max(range_to_test)))
    
best_vals = pd.DataFrame(best_vals)
best_vals.to_csv('best_vals.csv')
print(best_vals.sort_values(by='ideal_overflow'))
