#!/usr/bin/env python3

from ortools.linear_solver import pywraplp
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def ShowProblem():
    sns.set_style("whitegrid", {"grid.color": ".6", "grid.linestyle": ":"})
    x = np.arange(-4, 9, 0.01)

    y1 = (14 - x)/2
    y2 = 3*x
    y3 = x - 2

    ax = sns.lineplot(x=x, y=y1, color="red", label="x + 2y = 14")
    sns.lineplot(x=x, y=y2, color="green", label="3x - y = 0")
    sns.lineplot(x=x, y=y3, color="purple", label="x - y = 2")

    ymax = np.minimum(y1,y2)
    ax.fill_between(x, y3, ymax, where=y3<ymax, color="#0000FF55")

    plt.xlim(-2.5, 7.5)
    plt.ylim(-3.5, 6.5)

    plt.show()


def LinearSolveExample():
    # Instantiate a Glop solver
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Create the two variables and let them take on any non-negative value
    x = solver.NumVar(0, solver.infinity(), 'x')
    y = solver.NumVar(0, solver.infinity(), 'y')

    # Add the constrains
    solver.Add(x + 2 * y <= 14.0)
    solver.Add(3 * x - y >= 0.0)
    solver.Add(x - y <= 2.0)


    # Objective function: 3x + 4y
    solver.Maximize(3 * x + 4 * y)

    # Solve the system
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', x.solution_value())
        print('y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')


if __name__ == "__main__":
    ShowProblem()
    LinearSolveExample()

