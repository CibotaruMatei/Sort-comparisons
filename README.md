# Sort-comparisons
Compares the sorting times of various algorithms

# Input file (input.txt) syntax
number of lists to be generated

list parameters in the format "max value, size"

number of sorting functions to test

sorting function name (currently implemented: bubblesort, countsort, mergesort, radixsortMSD [base <value>], radixsortLSD [base <value>], quicksort <function>)

Note: only the following expressions are accepted as the pivot function for quicksort:

- median
- first
- last
- middle
- random