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

# assign transmissions to sites


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


# # get building demand time series
# for i in range(len(needed_demand_name)):
#     for load in sites_load:
#         timeseries_file_name = timeseries_path+'/BuildingHeatDemand_3.0_2.0_0.0_bID-'+str(load.building_id)+'.0.csv'
#         load.demands.append(demand(commodity=demand_commodities[i], value=pd.read_csv(timeseries_file_name)[needed_demand_name[i]]))

# # get building supim time series
# for i in range(len(needed_supim_name)):
#     for load in sites_load:
#         timeseries_file_name = timeseries_path+'/BuildingHeatDemand_3.0_2.0_0.0_bID-'+str(load.building_id)+'.0.csv'
#         load.demands.append(supim(commodity=supim_commodities[i], value=pd.read_csv(timeseries_file_name)[needed_supim_name[i]]))

# # get building time-var-eff time series
# for i in range(len(needed_timevareff_name)):
#     for load in sites_load:
#         timeseries_file_name = timeseries_path+'/BuildingHeatDemand_3.0_2.0_0.0_bID-'+str(load.building_id)+'.0.csv'
#         load.demands.append(time_var_eff(process=timevareff_processes[i], value=pd.read_csv(timeseries_file_name)[needed_timevareff_name[i]]))