from distutils.command.build import build
from json import loads
from unicodedata import name
from parameters import *
from classes import *
from copy import deepcopy
import pandas as pd


# generate sites
site_trafo = site(name='Trafostation_OS', pp_id=0)
site_main_busbar = site(name='main_busbar', pp_id=1)
sites_load = []
selected_buildings = pd.read_csv(selected_buildings_path, sep=';')
pp_id = selected_buildings['pandapower_id'].tolist()
urbs_name = selected_buildings['urbs_name'].tolist()
bui_id = selected_buildings['building_id'].tolist()
for i in range(len(pp_id)):
    sites_load.append(site(name=urbs_name[i], pp_id=pp_id[i], building_id=bui_id[i]))


# assign commodities to sites
site_trafo.commodities = trafo_commodities
site_main_busbar.commodities = main_busbar_commodities
i = 0
for load in sites_load:
    load.commodities = deepcopy(load_commodities)
    if building_relevant_commodities:
        for br_com in building_relevant_commodities:
            load.commodities[br_com[0]].set_attr_value(br_com[1], br_com[2][i])
    i += 1


# assign processes to sites
site_trafo.processes = trafo_processes
site_main_busbar.processes = main_busbar_processes
i = 0
for load in sites_load:
    load.processes = deepcopy(load_processes)
    if building_relevant_processes:
        for br_pro in building_relevant_processes:
            load.processes[br_pro[0]].set_attr_value(br_pro[1], br_pro[2][i])
    i += 1


# assign transmissions to trafostation and main busbar
site_trafo.transmissions = deepcopy(trafo_transmissions)
for tra in site_trafo.transmissions:
    tra.site_in = site_trafo.name
    tra.site_out = site_main_busbar.name

site_main_busbar.transmissions = deepcopy(trafo_transmissions)
for tra in site_main_busbar.transmissions:
    tra.site_out = site_trafo.name
    tra.site_in = site_main_busbar.name


# generate transmissions between loads according to the pandapower file
load_transmissions = []
pp_file_tra = pd.read_excel(pandapower_networks_path, sheet_name='line')
for i in pp_file_tra.index:
    tra = pp_file_tra.iloc[i]
    site_in = tra['from_bus']
    site_out = tra['to_bus']
    if site_in == 1:
        load_transmissions.append(transmisson(name=tra['name'], commodity='electricity', site_in='main_busbar', site_out=selected_buildings.iloc[site_out-2]['urbs_name']))
        load_transmissions.append(transmisson(name=tra['name'], commodity='electricity', site_in=selected_buildings.iloc[site_out-2]['urbs_name'], site_out='main_busbar'))
    else:
        load_transmissions.append(transmisson(name=tra['name'], commodity='electricity', site_in=selected_buildings.iloc[site_in-2]['urbs_name'], site_out=selected_buildings.iloc[site_out-2]['urbs_name']))
        load_transmissions.append(transmisson(name=tra['name'], commodity='electricity', site_in=selected_buildings.iloc[site_out-2]['urbs_name'], site_out=selected_buildings.iloc[site_in-2]['urbs_name']))


# assign storages to sites
site_trafo.storages = trafo_storages
site_main_busbar.storages = main_busbar_storages
i = 0
for load in sites_load:
    load.storages = deepcopy(load_storages)
    if building_relevant_storages:
        for br_sto in building_relevant_storages:
            load.storages[br_sto[0]].set_attr_value(br_sto[1], br_sto[2][i])
    i += 1


# get building demand time series

# get building supim time series

# get building time-var-eff time series