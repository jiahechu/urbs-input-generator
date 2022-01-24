from classes import commodity, process, transmisson, storage
from get_building_data import get_building_data


save_path = './urbs-test.xlsx'                      # path to save exported excel file
building_data_file_path = './dataset/building_data/building_data2.csv'    # path of building information file
pandapower_networks_path = './dataset/pandapower-networks'  # path which includes pandapower network files
selected_buildings_path = './dataset/selected_buildings.csv' # path of selected buildings file
timeseries_path = './dataset/building_data/time_series_per_building'      # path which includes building informations in time series

# define some building relevanted parameters
building_data = get_building_data(building_data_file_path, selected_buildings_path)

charging_station_inst_cap = [i * 11 for i in building_data['number_of_cars'].tolist()]
charging_station_cap_up = [i * 11 for i in building_data['number_of_cars'].tolist()]
mobility_storage_inst_cap_c = [i * 100 for i in building_data['car_demand_daily_total_MW'].tolist()]
mobility_storage_cap_up_c = [i * 100 for i in building_data['car_demand_daily_total_MW'].tolist()]

# define global information
co2_limit = '0'
cost_limit = 'inf'

kerber_network_name = 'ln-f1'   # ln-f1, ln-f2, ln-k1, ln-k2, dn, vn-k1, vn-k2
lines_number = 0
loads_number = []

elec_import_price = '0,3'
elec_feed_in_price = '0,07'


# define commodities
electricity = commodity(name='electricity', type='Demand')
space_heat = commodity(name='space_heat', type='Demand')
water_heat = commodity(name='water_heat', type='Demand')
mobility = commodity(name='mobility', type='Demand')
natural_gas = commodity(name='natural_gas', type='Stock', price='0', max='inf', max_per_hour='inf')
common_heat = commodity(name='common_heat', type='Stock', price='0', max='0', max_per_hour='0')
solar = commodity(name='solar', type='SupIm')
co2 = commodity(name='CO2', type='Env')
electricity_import = commodity(name='electricity_import', type='Buy', price='1', max='inf', max_per_hour='inf')
electricity_feed_in = commodity(name='electricity_feed_in', type='Sell', price='1', max='inf', max_per_hour='inf')

trafo_commodities = [electricity, electricity_feed_in, electricity_import]      # add commodities at trafo-station here
main_busbar_commodities = [electricity]     # add commodities at main busbar here
load_commodities = [electricity, space_heat, water_heat, mobility, natural_gas, common_heat, solar, co2]    # add commodities at every load here
building_relevant_commodities = []  # place of commodity in load_commodities list, attribute of commodity, value of attribute


# define processes
import_trafo = process(name='import', com_in=[electricity_import], com_out=[electricity])
feed_in = process(name='feed_in', com_in=[electricity], com_out=[electricity_feed_in])
slack = process(name='Slack', com_in=[electricity], com_out=[electricity])
rooftop_pv = process(name='Rooftop PV', com_in=[solar], com_out=[electricity])
gas_boiler = process(name='Gas Boiler', com_in=[natural_gas], com_out=[common_heat, co2])
heat_dummy_space = process(name='Heat_dummy_space', com_in=[common_heat], com_out=[space_heat])
heat_dummy_water = process(name='Heat_dummy_space', com_in=[common_heat], com_out=[water_heat])
heatpump_air = process(name='heatpump_air', com_in=[electricity], com_out=[common_heat])
charging_station = process(name='charging_station', com_in=[electricity], com_out=[mobility])
curtailment = process(name='curtailment', com_in=[electricity])

trafo_processes = [import_trafo, feed_in, slack]    # add processes at trafo-station here
main_busbar_processes = []      # add processes at main busbar here
load_processes = [rooftop_pv, gas_boiler, heat_dummy_space, heat_dummy_water, heatpump_air, charging_station, curtailment]     # add processes at every load here
building_relevant_processes = [(5, 'inst_cap', charging_station_inst_cap), (5, 'cap_up', charging_station_cap_up)]    # place of process in load_processes list, attribute of process, value of attribute


# define transmissions
trafo = transmisson(name='trafo', commodity=electricity)
new_trafo_160 = transmisson(name='new_trafo_160', commodity=electricity)
new_trafo_250 = transmisson(name='new_trafo_250', commodity=electricity)
new_trafo_400 = transmisson(name='new_trafo_400', commodity=electricity)
new_trafo_630 = transmisson(name='new_trafo_630', commodity=electricity)

trafo_transmissions = [trafo, new_trafo_160, new_trafo_250, new_trafo_400, new_trafo_630]   # add transmissions at trafo-station here


# define storages
battery_private = storage(name='battery_private', commodity=electricity)
thermochem_heat_storage = storage(name='thermochem_heat_storage', commodity=common_heat)
mobility_storage = storage(name='mobility_storage', commodity=mobility)

trafo_storages = []     # add storages at trafo-station here
main_busbar_storages = []       # add storages at main busbar here
load_storages = [battery_private, thermochem_heat_storage, mobility_storage]    # add storages at every load here
building_relevant_storages = [(2, 'inst_cap_c', mobility_storage_inst_cap_c), (2, 'cap_up_c', mobility_storage_cap_up_c)]     # place of storage in load_storages list, attribute of storage, value of attribute


# get building time series
needed_demand_name = ['HotWaterD_W', 'SpaceHeatingD_W', 'TotalD_W']
demand_commodities = [water_heat, space_heat, electricity]

needed_supim_name = ['sol_gains_W']
supim_commodities = [solar]

needed_timevareff_name = ['Occupants']
timevareff_processes = [charging_station]