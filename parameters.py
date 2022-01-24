from pyparsing import col
from classes import commodity, process, transmisson, storage
from get_building_data import get_building_data
import pandas as pd


save_path = './urbs-test.xlsx'                      # path to save exported excel file
building_data_file_path = './dataset/building_data/building_data2.csv'    # path of building information file
pandapower_networks_path = './dataset/pandapower-networks/kerber_landnetz_freileitung_1.xlsx'  # path which includes pandapower network files
selected_buildings_path = './dataset/selected_buildings.csv' # path of selected buildings file
timeseries_path = './time_series_per_building'      # path which includes building informations in time series

com_conf_path = './dataset/conf/com_conf.csv'
pro_conf_path = './dataset/conf/pro_conf.csv'
sto_conf_path = './dataset/conf/sto_conf.csv'
com_prop_path = './dataset/prop/com_prop.csv'
pro_prop_path = './dataset/prop/pro_prop.csv'
sto_prop_path = './dataset/prop/sto_prop.csv'


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
electricity_import = commodity(name='electricity_import', type='Buy', price='1', max='inf', max_per_hour='inf')
electricity_feed_in = commodity(name='electricity_feed_in', type='Sell', price='1', max='inf', max_per_hour='inf')

trafo_commodities = [electricity, electricity_feed_in, electricity_import]      # add commodities at trafo-station here
main_busbar_commodities = [electricity]     # add commodities at main busbar here
load_commodities = []    # add commodities at every load here
building_relevant_commodities = []  # place of commodity in load_commodities list, attribute of commodity, value of attribute

com_conf = pd.read_csv(com_conf_path, sep=';')
com_prop = pd.read_csv(com_prop_path, sep=';')

for i in range(len(com_prop['name'])):
    com = commodity()
    for column in com_prop.columns.tolist():
        com.set_attr_value(column, com_prop[column][i])
    load_commodities.append(com)
    building_relevant_commodities.append((i, 'exist', com_conf[com_prop['name'][i]]))


# define processes
import_trafo = process(name='import', com_in=[electricity_import], com_out=[electricity])
feed_in = process(name='feed_in', com_in=[electricity], com_out=[electricity_feed_in])
slack = process(name='Slack', com_in=[electricity], com_out=[electricity])

trafo_processes = [import_trafo, feed_in, slack]    # add processes at trafo-station here
main_busbar_processes = []      # add processes at main busbar here
load_processes = []     # add processes at every load here
building_relevant_processes = []    # place of process in load_processes list, attribute of process, value of attribute

pro_conf = pd.read_csv(pro_conf_path, sep=';')
pro_prop = pd.read_csv(pro_prop_path, sep=';')

for i in range(len(pro_prop['name'])):
    pro = process()
    for column in pro_prop.columns.tolist():
        pro.set_attr_value(column, pro_prop[column][i])
    load_processes.append(pro)
    if pro.name == 'charging_station':
        building_relevant_processes.append((i, 'inst_cap', charging_station_inst_cap))
        building_relevant_processes.append((i, 'cap_up', charging_station_cap_up))
    building_relevant_processes.append((i, 'exist', pro_conf[pro_prop['name'][i]]))

# define transmissions
trafo = transmisson(name='trafo', commodity='electricity')
new_trafo_160 = transmisson(name='new_trafo_160', commodity='electricity')
new_trafo_250 = transmisson(name='new_trafo_250', commodity='electricity')
new_trafo_400 = transmisson(name='new_trafo_400', commodity='electricity')
new_trafo_630 = transmisson(name='new_trafo_630', commodity='electricity')


trafo_transmissions = [trafo, new_trafo_160, new_trafo_250, new_trafo_400, new_trafo_630]   # add transmissions at trafo-station here


# define storages
trafo_storages = []     # add storages at trafo-station here
main_busbar_storages = []       # add storages at main busbar here
load_storages = []    # add storages at every load here
building_relevant_storages = []     # place of storage in load_storages list, attribute of storage, value of attribute

sto_conf = pd.read_csv(sto_conf_path, sep=';')
sto_prop = pd.read_csv(sto_prop_path, sep=';')

for i in range(len(sto_prop['name'])):
    sto = storage()
    for column in sto_prop.columns.tolist():
        sto.set_attr_value(column, sto_prop[column][i])
    load_storages.append(sto)
    if sto.name == 'mobility_storage':
        building_relevant_storages.append((i, 'inst_cap_c', mobility_storage_inst_cap_c))
        building_relevant_storages.append((i, 'cap_up_c', mobility_storage_cap_up_c))
    building_relevant_storages.append((i, 'exist', sto_conf[sto_prop['name'][i]]))


# get building time series
needed_demand_name = ['HotWaterD_W', 'SpaceHeatingD_W', 'TotalD_W']
demand_commodities = []

needed_supim_name = ['sol_gains_W']
supim_commodities = []

needed_timevareff_name = ['Occupants']
timevareff_processes = []