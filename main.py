#!/usr/bin/env python3

from ortools.linear_solver import pywraplp


def LinearProgrammingExample():
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
    LinearProgrammingExample()

