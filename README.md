# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In order to solve Sudoku puzzles the Naked Twins strategy can be applied. 
If there are two identical boxes(twins) with two permitted digits in each box in one unit(row, column or 3x3 subsquare) then 
there is a constraint for their peers' values in this unit. Any box but twins in this unit cannot be equal to digits in twins.
So we can delete digits in twins' peers which presented in twins. This strategy can be applied with other constraints such as 
Elimination and Only choice repeatedly. Applying more constraints faster and more likely take us to the solution.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal Sudoku can be solved as ordinary Sudoku. We only need to add diagonal units to unitlist. After that we can apply 
Elimination, Only choice and Naked Twins repeatedly in order to get to the solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.