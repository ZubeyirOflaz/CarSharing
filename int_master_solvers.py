import sys
import minizinc as mn
import Preprocessing as prp
import pandas as pd
import os

trip_duration = 2

locations = pd.read_csv("Groups.csv")
car_set = pd.read_csv("AvailableCars.csv",encoding = 'unicode_escape')
driver: mn.Driver = mn.find_driver([r"F:\Program Files\Minizinc"],name="minizinc.exe")
driver.make_default()
print(mn.default_driver.minizinc_version)


datasets = ["small", "medium", "large"]
destinations = [1, 2, 3, 4]
solvers = ["gecode"]

location_filtered = prp.filter_cases(locations,datasets[0],1)
car_filtered = prp.filter_cases(car_set,datasets[0])

model = mn.Model("int_solver.mzn")
solver = mn.Solver.lookup("gecode")

instance = mn.Instance(solver,model)

instance['Vehicles'] = car_filtered['Car Name'].to_list()
instance['n_locations'] = len(location_filtered)

instance['passanger_capacity'] = car_filtered['Number of Seats'].to_list()
total_rental_cost = [i * trip_duration for i in car_filtered['rent fee'].to_list()]
instance['rental_fee'] = total_rental_cost

#instance["number_of_people"] = location_filtered['Number of People'].to_list()

result = instance.solve()
