# Token sale

## Objectives

> This token contract allows you to buy and sell tokens at an even exchange rate of 1 token per ether.
> The contract starts off with a balance of 1 ether. See if you can take some of that away.

## Solution

While _incredibly_ simple, this problem took me _days_ to solve, as I was not aware (or forgot) of a few things:

* Floating point numbers do not exist in Solidity (as of writing this).
* Operations in Solidity between whole numbers which would yield a floating point number are immediately rounded down at _every step_, so an arithmetic equation consisting of multiple operations would be applied a floor function at every step of the operation, e.g. $2 \div 3 * 7 \div 2 \rightarrow \lfloor\lfloor\lfloor 2 \div 23 \rfloor * 7 \rfloor \div 2 \rfloor$.
* It is extremely difficult to get a perfect 0 after an integer overflow using products, therefore, in order to solve this problem, it's nearly impossible that the price for which I'll be able to buy the tokens (each worth 1 ether) will be _exactly_ zero wei.
* I completely forgot that python will do things in the background with math, like for example: `1e18` is immediately considered a float, even though it's a whole number, therefore, to have `1e18` as an integer, I should be writing `int(1e18)`. 

To solve it:


All that's needed to be passed to `numTokens` is a value that when multiplied by $10^{18}$ will yield a number that we can:

1. Pay for in wei that is lower than  $10^{18}$ itself
2. As low as possible (ideally) as long as condition 1 holds

For this you can create a simple function that will be the base to the overflow exploit, for example:

$$f(x) = \lfloor (\frac{2^{256} * x}{10^{18}} + 1) * 10^{18}\rfloor\mod 2^{256}$$

Then optimize for $min(f(x))$ while $x > 0$. I did this by bruteforce and made a simple neat table with the best numbers I got:

|             f(x) |                           x | 
|-----------------:|----------------------------:|
|     265665118208 |                      549972 |
|     531330236416 |                     1099944 |
|     730579075072 |                     1512423 |
|     996244193280 |                     2062395 |
|    1261909311488 |                     2612367 |

I used this simple script to do it and then neatly pack it on one dataframe:

```python
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

```

In this case, I'd simply choose the lowest one for `f(x)` and make the function calls:

1. Call `buy()` passing in $(\frac{2^{256} * 549972}{10^{18}} + 1)$ as `numTokens`.

2. Call `sell()` passing in $1$ as `numTokens`.

3. Check if the challenge is complete by calling `isComplete()` or just clicking on _Check Solution_ on the Capture The Ether site.

## Alternative (better) solution

I asked a question on the Ethereum StackExchange regarding some of my lack of understanding of solidity mathematical operations and Usmann was kind enough to write a better solution than mine which allows you to solve this while being able to send 0 wei to the contract. His solution was layed out in his answer to my question [here](https://ethereum.stackexchange.com/a/131705/104415).

## Submission transaction

https://ropsten.etherscan.io/tx/0x8b95f854e11e1b9a50f38f689d44bc018f65abc19753af497838b1ad5987b6ca
