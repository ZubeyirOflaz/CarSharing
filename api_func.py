import logging
import requests
import math

session = requests.Session()


def get_fuel_price(target_country, fuel_type):
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5sdbB26Heujgp9nLu4SBrZ:2IqgUiah8rO5U9PLYibIXC"
    }
    url = "https://api.collectapi.com/gasPrice/europeanCountries"
    response = session.get(url=url, headers=headers)
    if str(response.status_code).startswith("2"):
        data = response.json()
        fuel_price = [country[fuel_type] for country in data["results"] if country["country"] == target_country]
        return fuel_price[0]
    else:
        logging.error('request to get fuel price failed with status code {}'.format(response.status_code))


def round_half_up(n, decimals):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def round_number(n, decimals):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)


def rounding_func(n, decimals=0):
    new_list = []
    if isinstance(n, float) or isinstance(n, int):
        return round_number(n, decimals)
    if isinstance(n, list):
        if isinstance(n[0], list):
            for i in n:
                new_list.append([round_number(t, decimals) for t in i])
        else:
            new_list = [round_number(i, decimals) for i in n]
        return new_list

