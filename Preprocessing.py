import json as j
import sys

import requests as r
import pandas as pd
from time import sleep
import datetime


# This function returns the travel distance by car between two points

def get_distance(data_df):
    success_wait_time = 1
    fail_wait_time = 10
    distance_list = list()
    for index, row in data_df.iterrows():
        distance_row = []
        print(row['Group Name'])
        for index2, row2 in data_df.iterrows():
            # If group name is same set distance to zero
            if row['Group Name'] == row2['Group Name']:
                distance_row.append(0)
            else:
                # Try to fetch the distance. If successfull, append it to the list of distances, wait and get another
                print(f"{row['Group Name']} to {row2['Group Name']}")
                response = r.get(
                    f"http://router.project-osrm.org/route/v1/car/{row['Long']},{row['Lat']};{row2['Long']},{row2['Lat']}?overview=false""")
                if response.status_code == 200:
                    route_content = j.loads(response.content)
                    route_distance = route_content['routes'][0]['distance']
                    distance_row.append(route_distance)
                    sleep(success_wait_time)
                else:
                    # If getting distance was unsuccessfull, try it until get a successful response or try five times
                    # If still unsuccessfull warn user and return none
                    print(response.status_code)
                    i = 1
                    while i <= 5:
                        response = r.get(
                            f"http://router.project-osrm.org/route/v1/car/{row['Long']},{row['Lat']};{row2['Long']},{row2['Lat']}?overview=false""")
                        if response.status_code != 200:
                            sleep(fail_wait_time)
                            i += 1
                        else:
                            route_content = j.loads(response.content)
                            route_distance = route_content['routes'][0]['distance']
                            distance_row.append(route_distance)
                            break
                    if i <= 5:
                        sys.exit('The function is not able to get all the distances, please check the problem')
        # Add the distance row for the current location to the list
        distance_list.append(distance_row)
    # Return the distance matrix to the user
    return distance_list

# This function lets us filter specific value groups and destinations

def filter_cases(dataframe, case_size, destination=None):
    dataframe_filter = []
    if case_size == 'small':
        dataframe_filter = [f'Destination {destination}', 'Small']
    elif case_size == 'medium':
        dataframe_filter = [f'Destination {destination}', 'Small', 'Medium']
    elif case_size == 'large':
        dataframe_filter = [f'Destination {destination}', 'Small', 'Medium', 'Large']
    else:
        sys.exit('invalid case size')
    case_df = dataframe[dataframe['Case Type'].isin(dataframe_filter)]
    return case_df

#data = pd.read_csv('Groups.csv')
#data = filter_cases(data,'large',1)
#test_distance = get_distance(data)




    # response = r.get(f"http://router.project-osrm.org/route/v1/car/{long_1},{lat_1};{long_2},{lat_2}?overview=false""")
    # route = j.loads(response.content)
    # print(response.status_code)
    # return route
