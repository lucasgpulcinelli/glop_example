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
# to separate the data and nutrients from the python program to
# a pandas dataframe
# Copyright 2021 Lucas Eduardo Gulka Pulcinelli

from ortools.linear_solver import pywraplp
import pandas as pd


#read data
foods = pd.read_csv("foods.csv")
nutrients = pd.read_csv("nutrients.csv")

# Instantiate a Glop solver
solver = pywraplp.Solver('StiglerDietExample',
                    pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Declare an array to hold our variables.
food_vars = [solver.NumVar(0.0, solver.infinity(), row.name) 
                for row in foods.iloc]

print('Number of variables =', solver.NumVariables())

# Create the constraints, one per nutrient.
constraints = []
for i, nutrient in enumerate(nutrients.iloc[0]):
    constraints.append(solver.Constraint(nutrient, solver.infinity()))
    for j, item in enumerate(foods.iloc):
        constraints[i].SetCoefficient(food_vars[j], item[i+1])

print('Number of constraints =', solver.NumConstraints())

# Objective function: Minimize the sum of (price-normalized) foods.
objective = solver.Objective()
for food in food_vars:
    objective.SetCoefficient(food, 1)
objective.SetMinimization()

status = solver.Solve()

# Check that the problem has an optimal solution.
if status != solver.OPTIMAL:
    print('The problem does not have an optimal solution!')
    if status == solver.FEASIBLE:
        print('A potentially suboptimal solution was found.')
    else:
        print('The solver could not solve the problem.')
        exit(1)

# Display the amounts (in dollars) to purchase of each food.
nutrients_result = [0] * len(nutrients.iloc[0])

print('\nAnnual Foods:')
for i, food in enumerate(food_vars):
    if food.solution_value() > 0.0:

        print(f'{foods.iloc[i].name}: ${365*food.solution_value()}')

        for j, _ in enumerate(nutrients.iloc[0]):
            nutrients_result[j] += foods.iloc[i][j+1]*food.solution_value()

print(f'\nOptimal annual price: ${365*objective.Value():.4f}')

print('\nNutrients per day:')

for i, nutrient in enumerate(nutrients.iloc[0]):
    print(f'{foods.columns[i+1]}: {nutrients_result[i]:.2f} (min {nutrient})')

print('\nAdvanced usage:')
print('Problem solved in ', solver.wall_time(), ' milliseconds')
print('Problem solved in ', solver.iterations(), ' iterations')
