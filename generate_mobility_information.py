from copy import deepcopy
from parameters import *
from classes import *
from get_building_data import get_building_data

def generate_mobility_demand(building_data_file_path, selected_buildings_path):
    building_data = get_building_data(building_data_file_path, selected_buildings_path)
    car_demand = [i * 1000 for i in building_data['car_demand_daily_total_MW'].tolist()]
    mob_demand = []
    for car_dem in car_demand:
        value = []
        value = [0] * 23
        value.append(car_dem)
        value = value * 364
        value.extend([0] * 16)
        value = [0] * 8 + [car_dem / 2] + value
        mob_demand.append(demand(commodity=mobility, value = deepcopy(value)))
    return mob_demand


def generate_chargingstation_timevareff():
    value = [1] * 7 + [0] * 10 + [1] * 7
    value = value * 365
    value.insert(0, 0)
    return(time_var_eff(process=charging_station, value=deepcopy(value)))