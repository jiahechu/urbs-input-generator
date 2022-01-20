from generate_structure import *
import pandas as pd


# generate global sheet tuple
global_tuple = [('CO2 limit', co2_limit), ('Cost limit', cost_limit)]
global_df = pd.DataFrame(global_tuple, columns=['Property', 'Value'])


# generate site sheet tuple 
site_tuple = [(site_trafo.name, site_trafo.area, site_trafo.base_voltage, site_trafo.min_voltage, site_trafo.ref_node),
              (site_main_busbar.name, site_main_busbar.area, site_main_busbar.base_voltage,
               site_main_busbar.min_voltage, site_main_busbar.ref_node)]
for line in sites_load:
    for load in line:
        site_tuple.append((load.name, load.area, load.base_voltage, load.min_voltage, load.ref_node))
site_df = pd.DataFrame(site_tuple, columns=['Name', 'area', 'base-voltage', 'min-voltage', 'ref-node'])


# generate commodity sheet tuple
commodity_tuple = []
for com in site_trafo.commodities:
    commodity_tuple.append((site_trafo.name, com.name, com.type, com.price, com.max, com.max_per_hour))
for com in site_main_busbar.commodities:
    commodity_tuple.append((site_main_busbar.name, com.name, com.type, com.price, com.max, com.max_per_hour))
for line in sites_load:
    for load in line:
        for com in load.commodities:
            commodity_tuple.append((load.name, com.name, com.type, com.price, com.max, com.max_per_hour))
commodity_df = pd.DataFrame(commodity_tuple, columns=['Site', 'Commodity', 'Type', 'price', 'max', 'maxperhour'])


# generate process sheet tuple
process_tuple = []
for pro in site_trafo.processes:
    process_tuple.append((site_trafo.name, pro.name, pro.inst_cap, pro.cap_lo, pro.cap_up, pro.max_grad, pro.ramp_down_grad,
                          pro.min_fraction, pro.inv_cost, pro.fix_cost, pro.var_cost, pro.wacc, pro.depreciation, pro.area_per_cap,
                          pro.cap_block, pro.start_price, pro.on_off, pro.pf_min))
for pro in site_main_busbar.processes:
    process_tuple.append((site_main_busbar.name, pro.name, pro.inst_cap, pro.cap_lo, pro.cap_up, pro.max_grad, pro.ramp_down_grad,
                          pro.min_fraction, pro.inv_cost, pro.fix_cost, pro.var_cost, pro.wacc, pro.depreciation, pro.area_per_cap,
                          pro.cap_block, pro.start_price, pro.on_off, pro.pf_min))
for line in sites_load:
    for load in line:
        for pro in load.processes:
            process_tuple.append((load.name, pro.name, pro.inst_cap, pro.cap_lo, pro.cap_up, pro.max_grad, pro.ramp_down_grad,
                                  pro.min_fraction, pro.inv_cost, pro.fix_cost, pro.var_cost, pro.wacc, pro.depreciation, pro.area_per_cap,
                                  pro.cap_block, pro.start_price, pro.on_off, pro.pf_min))
process_df = pd.DataFrame(process_tuple, columns=['Site', 'Process', 'inst-cap', 'cap-lo', 'cap-up', 'max-grad', 'ramp-down-grad',
                                                  'min-fraction', 'inv-cost', 'fix-cost', 'var-cost', 'wacc', 'depreciation', 'area-per-cap',
                                                  'cap-block', 'start-price', 'on-off', 'pf-min'])


# generate process-comodity sheet tuple
process_commodity_tuple = []
for pro in site_trafo.processes:
    for com_in in pro.com_in:
        process_commodity_tuple.append((pro.name, com_in.name, 'in', pro.ratio, pro.ratio_min))
    for com_out in pro.com_out:
        process_commodity_tuple.append((pro.name, com_out.name, 'out', pro.ratio, pro.ratio_min))
for pro in site_main_busbar.processes:
    for com_in in pro.com_in:
        process_commodity_tuple.append((pro.name, com_in.name, 'in', pro.ratio, pro.ratio_min))
    for com_out in pro.com_out:
        process_commodity_tuple.append((pro.name, com_out.name, 'out', pro.ratio, pro.ratio_min))
for pro in sites_load[0][0].processes:
    for com_in in pro.com_in:
        process_commodity_tuple.append((pro.name, com_in.name, 'in', pro.ratio, pro.ratio_min))
    for com_out in pro.com_out:
        process_commodity_tuple.append((pro.name, com_out.name, 'out', pro.ratio, pro.ratio_min))
process_commodity_df = pd.DataFrame(process_commodity_tuple, columns=['Process', 'Commodity', 'Direction', 'ratio',	'ratio-min'])


# generate transmission sheet tuple
transmisson_tuple = []
for tra in site_trafo.transmissions:
    transmisson_tuple.append((tra.site_in, tra.site_out, tra.name, tra.commodity.name, tra.eff, tra.inv_cost, tra.fix_cost, tra.var_cost,
                              tra.inst_cap, tra.cap_lo, tra.cap_up, tra.wacc, tra.depreciation, tra.reactance, tra.difflimit, tra.base_voltage,
                              tra.tra_block))

transmisson_df = pd.DataFrame(transmisson_tuple, columns=['Site In', 'Site Out', 'Transmission', 'Commodity', 'eff', 'inv-cost', 'fix-cost', 'var-cost',
                                                          'inst-cap', 'cap-lo', 'cap-up', 'wacc', 'depreciation', 'reactance', 'difflimit', 'base_voltage',
                                                          'tra-block'])


# generate storage sheet tuple
storage_tuple = []
for sto in site_trafo.storages:
    storage_tuple.append((site_trafo.name, sto.name, sto.commodity.name, sto.inst_cap_c, sto.cap_lo_c, sto.cap_up_c, sto.inst_cap_p, sto.cap_lo_p, sto.cap_up_p,
                          sto.eff_in, sto.eff_out, sto.inv_cost_p, sto.inv_cost_c, sto.fix_cost_p, sto.fix_cost_c, sto.var_cost_p, sto.var_cost_c, sto.wacc,
                          sto.depreciation, sto.init, sto.discharge, sto.ep_ratio, sto.c_block, sto.p_block))
for sto in site_main_busbar.storages:
    storage_tuple.append((site_main_busbar.name, sto.name, sto.commodity.name, sto.inst_cap_c, sto.cap_lo_c, sto.cap_up_c, sto.inst_cap_p, sto.cap_lo_p, sto.cap_up_p,
                          sto.eff_in, sto.eff_out, sto.inv_cost_p, sto.inv_cost_c, sto.fix_cost_p, sto.fix_cost_c, sto.var_cost_p, sto.var_cost_c, sto.wacc,
                          sto.depreciation, sto.init, sto.discharge, sto.ep_ratio, sto.c_block, sto.p_block))
for line in sites_load:
    for load in line:
        for sto in load.storages:
            storage_tuple.append((load.name, sto.name, sto.commodity.name, sto.inst_cap_c, sto.cap_lo_c, sto.cap_up_c, sto.inst_cap_p, sto.cap_lo_p, sto.cap_up_p,
                                  sto.eff_in, sto.eff_out, sto.inv_cost_p, sto.inv_cost_c, sto.fix_cost_p, sto.fix_cost_c, sto.var_cost_p, sto.var_cost_c, sto.wacc,
                                  sto.depreciation, sto.init, sto.discharge, sto.ep_ratio, sto.c_block, sto.p_block))
storage_df = pd.DataFrame(storage_tuple, columns=['Site', 'Storage', 'Commodity', 'inst-cap-c', 'cap-lo-c', 'cap-up-c', 'inst-cap-p', 'cap-lo-p', 'cap-up-p', 'eff-in',
                                                  'eff-out', 'inv-cost-p', 'inv-cost-c', 'fix-cost-p', 'fix-cost-c', 'var-cost-p', 'var-cost-c', 'wacc', 'depreciation',
                                                  'init', 'discharge', 'ep-ratio', 'c-block', 'p-block'])