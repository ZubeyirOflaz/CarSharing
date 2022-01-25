import pandas as pd
import api_func as apf
import Preprocessing as prp
import Plotter as plt


def set_coordinates(data_df):
    coord_multiplier = 10000
    x_coord = data_df['Long'].to_list()
    y_coord = data_df['Lat'].to_list()
    x_coord_normalized = apf.rounding_func([x * coord_multiplier for x in x_coord])
    y_coord_normalized = apf.rounding_func([y * coord_multiplier for y in y_coord])
    destination_x = max(x_coord_normalized[1:len(x_coord_normalized)]) + 100
    destination_y = max(y_coord_normalized[1:len(y_coord_normalized)]) + 100
    x_coord_normalized[0] = destination_x
    y_coord_normalized[0] = destination_y
    x_coord_normalized = [(i - min(x_coord_normalized))+ 10 for i in x_coord_normalized]
    y_coord_normalized = [(i - min(y_coord_normalized))+ 10 for i in y_coord_normalized]

    coordinates = []
    for i in range(0, len(x_coord_normalized)):
        coordinates.append((x_coord_normalized[i], y_coord_normalized[i]))
    return coordinates

def get_routes(route_list):
    routes = []
    for route in route_list:
        path = []
        for i in range(0,len(route)):
            #print(f'{str(i + 1)} <-> {str(route[i])}')
            if i + 1 != route[i]:
                path.append(route[i])
        if len(path) > 0:
            path_2 = [i-1 for i in path]
            routes.append(path_2)
    return routes


if __name__ == '__main__':
    df = pd.read_csv('Groups.csv')
    df_filtered = prp.filter_cases(df, 'small', 2)
    test = set_coordinates(df_filtered)
    path_1 = [0,5,3]
    path_2 = [2,1,4,5]
    path = [path_1, path_2]
    a = [[6, 2, 4, 5, 0, 1], [3, 0]]
    a = [[6, 2, 4, 5, 0, 1], [0,3,0,3,0,3]]
    #test = get_routes(path)
    plt.plotTSP(a,test,2,'test2.png')
