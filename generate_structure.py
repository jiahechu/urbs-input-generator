from parameters import *
from classes import *
from copy import deepcopy
from read_external_files import read_whole_folder

if __name__ == '__main__':
    # generate sites
    if kerber_network_name == 'ln-f1':
        lines_number = 1
        loads_number = [13]
    if kerber_network_name == 'ln-f2' or kerber_network_name == 'ln-k1':
        lines_number = 2
        loads_number = [6, 2]
    if kerber_network_name == 'ln-k2':
        lines_number = 2
        loads_number = [12, 2]

    site_trafo = site(name='Trafostation_OS')
    site_main_busbar = site(name='main_busbar')
    sites_load = []
    for i in range(lines_number):
        sites_load.append([])         
        for j in range(loads_number[i]):
            sites_load[-1].append(site(name='loadbus_'+str(i+1)+'_'+str(j+1)))


    # assign commodities to sites
    site_trafo.commodities = trafo_commodities
    site_main_busbar.commodities = main_busbar_commodities
    if building_relevant_commodities:
        i = 0
        for line in sites_load:
            for load in line:
                for br_com in building_relevant_commodities:
                    load_commodities_dc = deepcopy(load_commodities)
                    load_commodities_dc[br_com[0]].set_attr_value(br_com[1], br_com[2][i])
                load.commodities = load_commodities_dc
                i += 1
    else:
        for line in sites_load:
            for load in line:
                load.commodities = load_commodities


    # assign processes to sites
    site_trafo.processes = trafo_processes
    site_main_busbar.processes = main_busbar_processes
    if building_relevant_processes:
        i = 0
        for line in sites_load:
            for load in line:
                for br_pro in building_relevant_processes:
                    load_processes_dc = deepcopy(load_processes)
                    load_processes_dc[br_pro[0]].set_attr_value(br_pro[1], br_pro[2][i])
                load.processes = load_processes_dc
                i += 1
                
    else:
        for line in sites_load:
            for load in line:
                load.processes = load_processes


    # assign transmissions to sites
    for trafo_transmission in trafo_transmissions:
        trafo_transmission_dc = deepcopy(trafo_transmission)
        trafo_transmission_dc.site_in = site_trafo.name
        trafo_transmission_dc.site_out = site_main_busbar.name
        site_trafo.transmissions.append(trafo_transmission_dc)
        trafo_transmission_dc = deepcopy(trafo_transmission)
        trafo_transmission_dc.site_in = site_main_busbar.name
        trafo_transmission_dc.site_out = site_trafo.name
        site_main_busbar.transmissions.append(trafo_transmission_dc)


    # assign storages to sites
    site_trafo.storages = trafo_storages
    site_main_busbar.storages = main_busbar_storages
    if building_relevant_storages:
        i = 0
        for line in sites_load:
            for load in line:
                for br_sto in building_relevant_storages:
                    load_storages_dc = deepcopy(load_storages)
                    load_storages_dc[br_sto[0]].set_attr_value(br_sto[1], br_sto[2][i])
                load.storages = load_storages_dc
                i += 1
    else:
        for line in sites_load:
            for load in line:
                load.storages = load_storages


    # # get building demand time series
    # for dem in needed_demand_name:
    #     dem_value  = read_whole_folder(timeseries_folder_path, dem)
        