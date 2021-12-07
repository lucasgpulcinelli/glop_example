#!/usr/bin/env python3
# Copyright 2010-2021 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file was changed by Lucas Eduardo Gulka Pulcinelli
# to include a seaborn plot of the problem and modify the logic 
# for ease of understanding.
# Copyright 2021 Lucas Eduardo Gulka Pulcinelli

from ortools.linear_solver import pywraplp
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


sns.set_style("whitegrid", {"grid.color": ".6", "grid.linestyle": ":"})


def GetPlot():

    #line data for all lines
    x = np.arange(-4, 9, 0.01)
    y1 = (14 - x)/2
    y2 = 3*x
    y3 = x - 2

    #draw the lines
    ax = sns.lineplot(x=x, y=y1, color="blue", label="x + 2y = 14")
    sns.lineplot(x=x, y=y2, color="green", label="3x - y = 0")
    sns.lineplot(x=x, y=y3, color="purple", label="x - y = 2")


    #get the max y for feasible solutions
    ymax = np.minimum(y1,y2)
    #create the area of feasible solutions
    ax.fill_between(x, y3, ymax, where=y3<ymax, color="#0000FF55")

    plt.xlim(-2.5, 7.5)
    plt.ylim(-3.5, 6.5)

    return ax


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
        return x.solution_value(), y.solution_value()
    else:
        raise ValueError("The problem does not have an optimal solution") 



if __name__ == "__main__":
    GetPlot()

    xsol, ysol = LinearSolveExample()

    sns.scatterplot(x=[xsol],y=[ysol], s=100, color="red", 
        label="max value for 3x + 4y", zorder=4)

    plt.show()
