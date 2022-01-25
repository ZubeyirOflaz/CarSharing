include "subcircuit.mzn";

int: n_locations;
enum Vehicles;
set of int: Locations = 1..n_locations;
array[Vehicles, Locations] of var Locations: next;
array[Locations] of var set of Vehicles: groups_to_cars;
array[Vehicles] of var set of Locations: cars_to_groups;


array[Vehicles] of int: rental_fee;
array[Vehicles] of int: cent_per_kilometer;


%distance array that is imported from Python
array[Locations, Locations] of int:distances;

%creation of subcircuit constraint
constraint forall(v in Vehicles) (subcircuit([next[v,s]| s in Locations]));

%linked decision variables
constraint forall(l in Locations, v in Vehicles) ( l in cars_to_groups[v] <-> v in groups_to_cars[l]);

%constraint to make sure any location other than the destination is visited once
constraint forall(l in Locations where l != 1) (card(groups_to_cars[l])=1);

%Cost function
array[Vehicles] of var int: travel_cost;
constraint forall(v in Vehicles) (
  sum(l in Locations where next[v,l] != l)(distances[l,next[v,l]]*cent_per_kilometer[v]) = travel_cost[v]) ;
array[Vehicles] of var int: rental_cost;
%constraint forall(v in Vehicles where travel_cost[v] != 0) (rental_cost[v]=rental_fee[v]);
constraint forall(v in Vehicles) (rental_cost[v] = bool2int(travel_cost[v] != 0) * rental_fee[v]);
var int: total_cost;
constraint total_cost = sum(v in Vehicles)(travel_cost[v]+rental_cost[v]);
%constraint total_cost = sum(v in Vehicles)(travel_cost[v]);
solve minimize total_cost;

%%[HELP] Further linking of decision variables
%constraint next['Volkswagen\xa0Golf',1] != 1;
%constraint forall(l in Locations, v in Vehicles where next[v,l] != l) (next[v,l] in cars_to_groups[v]);
constraint forall(v in Vehicles, l in Locations)(l in cars_to_groups[v] <-> next[v,l] != l);
%constraint forall(l in Locations, v in Vehicles where next[v,l] != l) (row(next,v) in cars_to_groups[v]);
%constraint forall(v in Vehicles)(among(row(next,v in Vehicles), cars_to_groups[v]));

array[Vehicles] of int: has_large_luggage;
array[Locations] of int: number_of_people;
array[Locations] of int: needs_large_luggage;
array[Vehicles] of int: passanger_capacity;

%Making sure that cars carry number of passangers that is below their capacity  
constraint forall(v in Vehicles) (
  sum(l in cars_to_groups[v]) (number_of_people[l])<= passanger_capacity[v]);

%Making sure that the last location that is visited in the subcircuit is the destination
constraint forall(v in Vehicles)(next[v,1] = 1 <-> forall(l in Locations)(next[v, l] = l));

%Making sure that Families get the cars with large luggage
constraint forall(l in Locations where needs_large_luggage[l] = 1)(forall(v in groups_to_cars[l]) (has_large_luggage[v] ==  1));

