from distutils.command.build import build
from json import loads
from parameters import *
from classes import *
from copy import deepcopy
import pandas as pd


# assign network file
if kerber_network_name == 'ln-f1':
    pandapower_networks_path += '/kerber_landnetz_freileitung_1.xlsx'
if kerber_network_name == 'ln-f2':
    pandapower_networks_path += '/kerber_landnetz_freileitung_2.xlsx'
if kerber_network_name == 'ln-k1':
    pandapower_networks_path += '/kerber_landnetz_kabel_1.xlsx'
if kerber_network_name == 'ln-k2':
    pandapower_networks_path += '/kerber_landnetz_kabel_2.xlsx'
if kerber_network_name == 'vn-k1':
    pandapower_networks_path += '/kerber_vorstadtnetz_kabel_1.xlsx'
if kerber_network_name == 'vn-k1':
    pandapower_networks_path += '/kerber_vorstadtnetz_kabel_2.xlsx'
if kerber_network_name == 'dn':
    pandapower_networks_path += '/kerber_dorfnetz.xlsx'

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


# assign transmissions to trafo and main busbar
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
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in='main_busbar', site_out=selected_buildings.iloc[site_out-2]['urbs_name']))
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in=selected_buildings.iloc[site_out-2]['urbs_name'], site_out='main_busbar'))
    else:
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in=selected_buildings.iloc[site_in-2]['urbs_name'], site_out=selected_buildings.iloc[site_out-2]['urbs_name']))
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in=selected_buildings.iloc[site_out-2]['urbs_name'], site_out=selected_buildings.iloc[site_in-2]['urbs_name']))



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