from generate_structure import *
import pandas as pd


# generate global sheet tuple
global_tuple = [('CO2 limit', co2_limit), ('Cost limit', cost_limit)]
global_df = pd.DataFrame(global_tuple, columns=['Property', 'Value'])


# generate site sheet tuple 
site_tuple = [(site_trafo.name, site_trafo.area, site_trafo.base_voltage, site_trafo.min_voltage, site_trafo.ref_node),
              (site_main_busbar.name, site_main_busbar.area, site_main_busbar.base_voltage,
               site_main_busbar.min_voltage, site_main_busbar.ref_node)]
for load in sites_load:
    site_tuple.append((load.name, load.area, load.base_voltage, load.min_voltage, load.ref_node))
site_df = pd.DataFrame(site_tuple, columns=['Name', 'area', 'base-voltage', 'min-voltage', 'ref-node'])


# generate commodity sheet tuple
commodity_tuple = []
for com in site_trafo.commodities:
    if com.exist == 1:
        commodity_tuple.append((site_trafo.name, com.name, com.type, com.price, com.max, com.max_per_hour))
for com in site_main_busbar.commodities:
    if com.exist == 1:
        commodity_tuple.append((site_main_busbar.name, com.name, com.type, com.price, com.max, com.max_per_hour))
for load in sites_load:
    for com in load.commodities:
        if com.exist == 1:
            commodity_tuple.append((load.name, com.name, com.type, com.price, com.max, com.max_per_hour))
commodity_df = pd.DataFrame(commodity_tuple, columns=['Site', 'Commodity', 'Type', 'price', 'max', 'maxperhour'])


# generate process sheet tuple
process_tuple = []
for pro in site_trafo.processes:
    if pro.exist == 1:
        process_tuple.append((site_trafo.name, pro.name, pro.inst_cap, pro.cap_lo, pro.cap_up, pro.max_grad, pro.ramp_down_grad,
                            pro.min_fraction, pro.inv_cost, pro.fix_cost, pro.var_cost, pro.wacc, pro.depreciation, pro.area_per_cap,
                            pro.cap_block, pro.start_price, pro.on_off, pro.pf_min))
for pro in site_main_busbar.processes:
    if pro.exist == 1:
        process_tuple.append((site_main_busbar.name, pro.name, pro.inst_cap, pro.cap_lo, pro.cap_up, pro.max_grad, pro.ramp_down_grad,
                            pro.min_fraction, pro.inv_cost, pro.fix_cost, pro.var_cost, pro.wacc, pro.depreciation, pro.area_per_cap,
                            pro.cap_block, pro.start_price, pro.on_off, pro.pf_min))
for load in sites_load:
    for pro in load.processes:
        if pro.exist == 1:
            process_tuple.append((load.name, pro.name, pro.inst_cap, pro.cap_lo, pro.cap_up, pro.max_grad, pro.ramp_down_grad,
                                    pro.min_fraction, pro.inv_cost, pro.fix_cost, pro.var_cost, pro.wacc, pro.depreciation, pro.area_per_cap,
                                    pro.cap_block, pro.start_price, pro.on_off, pro.pf_min))
process_df = pd.DataFrame(process_tuple, columns=['Site', 'Process', 'inst-cap', 'cap-lo', 'cap-up', 'max-grad', 'ramp-down-grad',
                                                  'min-fraction', 'inv-cost', 'fix-cost', 'var-cost', 'wacc', 'depreciation', 'area-per-cap',
                                                  'cap-block', 'start-price', 'on-off', 'pf-min'])


# generate process-comodity sheet tuple
process_commodity_df = pd.read_csv('./dataset/prop/pro_com_prop.csv',sep=';')


# generate transmission sheet tuple
transmission_tuple = []
for tra in site_trafo.transmissions:
    transmission_tuple.append((tra.site_in, tra.site_out, tra.name, tra.commodity, tra.eff, tra.inv_cost, tra.fix_cost, tra.var_cost,
                              tra.inst_cap, tra.cap_lo, tra.cap_up, tra.wacc, tra.depreciation, tra.reactance, tra.difflimit, tra.base_voltage,
                              tra.tra_block))

for tra in site_main_busbar.transmissions:
    transmission_tuple.append((tra.site_in, tra.site_out, tra.name, tra.commodity, tra.eff, tra.inv_cost, tra.fix_cost, tra.var_cost,
                              tra.inst_cap, tra.cap_lo, tra.cap_up, tra.wacc, tra.depreciation, tra.reactance, tra.difflimit, tra.base_voltage,
                              tra.tra_block))
                            
for tra in load_transmissions:
    transmission_tuple.append((tra.site_in, tra.site_out, tra.name, tra.commodity, tra.eff, tra.inv_cost, tra.fix_cost, tra.var_cost,
                              tra.inst_cap, tra.cap_lo, tra.cap_up, tra.wacc, tra.depreciation, tra.reactance, tra.difflimit, tra.base_voltage,
                              tra.tra_block))

transmission_df = pd.DataFrame(transmission_tuple, columns=['Site In', 'Site Out', 'Transmission', 'Commodity', 'eff', 'inv-cost', 'fix-cost', 'var-cost',
                                                          'inst-cap', 'cap-lo', 'cap-up', 'wacc', 'depreciation', 'reactance', 'difflimit', 'base_voltage',
                                                          'tra-block'])


# generate storage sheet tuple
storage_tuple = []
for sto in site_trafo.storages:
    if sto.exist == 1:
        storage_tuple.append((site_trafo.name, sto.name, sto.commodity, sto.inst_cap_c, sto.cap_lo_c, sto.cap_up_c, sto.inst_cap_p, sto.cap_lo_p, sto.cap_up_p,
                            sto.eff_in, sto.eff_out, sto.inv_cost_p, sto.inv_cost_c, sto.fix_cost_p, sto.fix_cost_c, sto.var_cost_p, sto.var_cost_c, sto.wacc,
                            sto.depreciation, sto.init, sto.discharge, sto.ep_ratio, sto.c_block, sto.p_block))
for sto in site_main_busbar.storages:
    if sto.exist == 1:
        storage_tuple.append((site_main_busbar.name, sto.name, sto.commodity, sto.inst_cap_c, sto.cap_lo_c, sto.cap_up_c, sto.inst_cap_p, sto.cap_lo_p, sto.cap_up_p,
                            sto.eff_in, sto.eff_out, sto.inv_cost_p, sto.inv_cost_c, sto.fix_cost_p, sto.fix_cost_c, sto.var_cost_p, sto.var_cost_c, sto.wacc,
                            sto.depreciation, sto.init, sto.discharge, sto.ep_ratio, sto.c_block, sto.p_block))
for load in sites_load:
    for sto in load.storages:
        if sto.exist == 1:
            storage_tuple.append((load.name, sto.name, sto.commodity, sto.inst_cap_c, sto.cap_lo_c, sto.cap_up_c, sto.inst_cap_p, sto.cap_lo_p, sto.cap_up_p,
                                    sto.eff_in, sto.eff_out, sto.inv_cost_p, sto.inv_cost_c, sto.fix_cost_p, sto.fix_cost_c, sto.var_cost_p, sto.var_cost_c, sto.wacc,
                                    sto.depreciation, sto.init, sto.discharge, sto.ep_ratio, sto.c_block, sto.p_block))
storage_df = pd.DataFrame(storage_tuple, columns=['Site', 'Storage', 'Commodity', 'inst-cap-c', 'cap-lo-c', 'cap-up-c', 'inst-cap-p', 'cap-lo-p', 'cap-up-p', 'eff-in',
                                                  'eff-out', 'inv-cost-p', 'inv-cost-c', 'fix-cost-p', 'fix-cost-c', 'var-cost-p', 'var-cost-c', 'wacc', 'depreciation',
                                                  'init', 'discharge', 'ep-ratio', 'c-block', 'p-block'])

