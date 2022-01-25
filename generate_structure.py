from parameters import *
from classes import *
from copy import deepcopy
from generate_mobility_information import generate_mobility_demand, generate_chargingstation_timevareff
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
vn_lv_kv = pd.read_excel(pandapower_networks_path, sheet_name='trafo')['vn_lv_kv'][0]
for i in pp_file_tra.index:
    tra = pp_file_tra.iloc[i]
    site_in = tra['from_bus']
    site_out = tra['to_bus']
    if site_in == 1:
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in='main_busbar',
                                  site_out=selected_buildings.iloc[site_out-2]['urbs_name'], inst_cap=tra['max_i_ka'] * 1000 * vn_lv_kv,
                                  inv_cost=1000 * tra['length_km'] * 1000 / (tra['max_i_ka'] * 1000 * vn_lv_kv)))
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in=selected_buildings.iloc[site_out-2]['urbs_name'], 
                                  site_out='main_busbar', inst_cap=tra['max_i_ka'] * 1000 * vn_lv_kv, inv_cost=1000 * tra['length_km'] * 1000 / (tra['max_i_ka'] * 1000 * vn_lv_kv)))
    else:
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in=selected_buildings.iloc[site_in-2]['urbs_name'],
                                  site_out=selected_buildings.iloc[site_out-2]['urbs_name'], inst_cap=tra['max_i_ka'] * 1000 * vn_lv_kv,
                                  inv_cost=1000 * tra['length_km'] * 1000 / (tra['max_i_ka'] * 1000 * vn_lv_kv)))
        load_transmissions.append(transmisson(name=tra['name'], commodity=electricity, site_in=selected_buildings.iloc[site_out-2]['urbs_name'],
                                  site_out=selected_buildings.iloc[site_in-2]['urbs_name'], inst_cap=tra['max_i_ka'] * 1000 * vn_lv_kv,
                                  inv_cost=1000 * tra['length_km'] * 1000 / (tra['max_i_ka'] * 1000 * vn_lv_kv)))


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
mob_dem = generate_mobility_demand(building_data_file_path, selected_buildings_path)
j = 0
for load in sites_load:
    i = 0
    dem_list = []
    timeseries_file_name = timeseries_path+'/d-'+str(load.building_id)+'.csv'
    demand_file = pd.read_csv(timeseries_file_name, sep=';')
    for dem_name in needed_demand_name:
        value = demand_file[dem_name].tolist()
        value.insert(0, 0)
        for com in load.commodities:
            if demand_commodities[i].name == com.name and com.exist == 1:
                dem_list.append(demand(commodity=demand_commodities[i], value=value))
        i += 1
    for com in load.commodities:
        if com.name == 'mobility' and com.exist == 1:
            dem_list.append(mob_dem[j])  
    load.demands = deepcopy(dem_list)
    j += 1


# get building supim time series
for load in sites_load:
    i = 0
    supim_list = []
    timeseries_file_name = timeseries_path+'/d-'+str(load.building_id)+'.csv'
    supim_file = pd.read_csv(timeseries_file_name, sep=';')
    for supim_name in needed_supim_name:
        value = [i / 100000 for i in supim_file[supim_name].tolist()]
        value.insert(0, 0)
        for com in load.commodities:
            if supim_commodities[i].name == com.name and com.exist == 1:
                supim_list.append(supim(commodity=supim_commodities[i], value=value))
        i += 1
    load.supim = deepcopy(supim_list)


# get building time-var-eff time series
char_sta_timevareff = generate_chargingstation_timevareff()
for load in sites_load:
    i = 0
    cop_file = pd.read_csv(cop_file_path, sep=';')
    timevareff_list = []
    for timevareff_name in needed_timevareff_name:
        value = cop_file[timevareff_name].tolist()
        value.insert(0, 0)
        for pro in load.processes:
            if timevareff_processes[i].name == pro.name and pro.exist == 1:
                timevareff_list.append(time_var_eff(process=timevareff_processes[i], value=value))
        i += 1
    load.time_var_eff = deepcopy(timevareff_list)
    for pro in load.processes:
        if pro.name == 'charging_station' and pro.exist == 1:
            load.time_var_eff.append(char_sta_timevareff)
        
