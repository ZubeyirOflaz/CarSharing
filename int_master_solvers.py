import sys
import minizinc as mn
import Preprocessing as prp
import pandas as pd
import api_func as apf

trip_duration = 2
fuel_price_multiplier = 1

fuel_price = float(apf.get_fuel_price("Germany","gasoline").replace(",","."))

fuel_price_adjusted = fuel_price * fuel_price_multiplier * 100


locations = pd.read_csv("Groups.csv")
car_set = pd.read_csv("AvailableCars.csv",encoding = 'unicode_escape')
driver: mn.Driver = mn.find_driver([r"F:\Program Files\Minizinc"],name="minizinc.exe")
driver.make_default()
print(mn.default_driver.minizinc_version)


datasets = ["small", "medium", "large"]
destinations = [1, 2, 3, 4]
solvers = ["gecode","chuffed","globalizer"]

location_filtered = prp.filter_cases(locations,datasets[0],1)
car_filtered = prp.filter_cases(car_set,datasets[0])
distance_matrix = prp.get_distance(location_filtered)
distance_matrix_kilometer = []
for i in distance_matrix:
    distance_row = [x / 1000 for x in i]
    distance_matrix_kilometer.append(distance_row)
distance_matrix_integer = apf.rounding_func(distance_matrix_kilometer)

model = mn.Model("int_solver.mzn")
solver = mn.Solver.lookup(solvers[0])

instance = mn.Instance(solver,model)
# Get locations and vehicles
instance['Vehicles'] = car_filtered['Car Name'].to_list()
instance['n_locations'] = len(location_filtered)
# Get data regarding the cars to the instance
instance['passanger_capacity'] = car_filtered['Number of Seats'].to_list()
total_rental_cost = [i * trip_duration for i in car_filtered['rent fee'].to_list()]
instance['rental_fee'] = total_rental_cost
car_fuel_price = [i * fuel_price_adjusted for i in car_filtered['liter per kilometer'].to_list()]
instance['cent_per_kilometer'] = apf.rounding_func(car_fuel_price)
instance['has_large_luggage'] = apf.rounding_func(car_filtered['Large Luggage Space'].to_list())

instance["number_of_people"] = apf.rounding_func(location_filtered['Number of People'].to_list())
instance["needs_large_luggage"] = apf.rounding_func(location_filtered['Needs Large Luggage'].to_list())
instance['distances'] = distance_matrix_integer

result = instance.solve()
#result[solver][dataset][destination]
