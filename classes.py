from typing import Match


class commodity:
    def __init__(self, name='', type='', price='', max='inf', max_per_hour='inf', exist=1):
        self.name = name
        self.type = type
        self.price = price
        self.max = max
        self.max_per_hour = max_per_hour
        self.exist = exist

    def set_attr_value(self, attr, value):
        if attr == 'name':
            self.name = value
        elif attr == 'type':
            self.type = value
        elif attr == 'price':
            self.price = value
        elif attr == 'max':
            self.max = value
        elif attr == 'max_per_hour':
            self.max_per_hour = value
        elif attr == 'exist':
            self.exist = value
        else:
            raise ValueError('no valid attribute found')


class process:
    def __init__(self, name='', inst_cap='0', cap_lo='0', cap_up='inf', max_grad='inf', ramp_down_grad='0',
                 min_fraction='0', inv_cost='0', fix_cost='0', var_cost='0', wacc='0.07', depreciation='30',
                 area_per_cap='', cap_block='', start_price='',	on_off='', pf_min='', com_in=[],
                 com_out=[], ratio='1', ratio_min='0', exist=1):
        self.name = name
        self.inst_cap = inst_cap
        self.cap_lo = cap_lo
        self.cap_up = cap_up
        self.max_grad = max_grad
        self.ramp_down_grad = ramp_down_grad
        self.min_fraction = min_fraction
        self.inv_cost = inv_cost
        self.fix_cost = fix_cost
        self.var_cost = var_cost
        self.wacc = wacc
        self.depreciation = depreciation
        self.area_per_cap = area_per_cap
        self.cap_block = cap_block
        self.start_price = start_price
        self.on_off = on_off
        self.pf_min = pf_min
        self.com_in = com_in
        self.com_out = com_out
        self.ratio = ratio
        self.ratio_min = ratio_min
        self.exist = exist

    def set_attr_value(self, attr, value):
        if attr == 'name':
            self.name = value
        elif attr == 'inst_cap':
            self.inst_cap = value
        elif attr == 'cap_lo':
            self.cap_lo = value
        elif attr == 'cap_up':
            self.cap_up = value
        elif attr == 'max_grad':
            self.max_grad = value
        elif attr == 'ramp_down_grad':
            self.ramp_down_grad = value
        elif attr == 'min_fraction':
            self.min_fraction = value
        elif attr == 'inv_cost':
            self.inv_cost = value
        elif attr == 'fix_cost':
            self.fix_cost = value
        elif attr == 'var_cost':
            self.var_cost = value
        elif attr == 'wacc':
            self.wacc = value
        elif attr == 'depreciation':
            self.depreciation = value
        elif attr == 'area_per_cap':
            self.area_per_cap = value
        elif attr == 'cap_block':
            self.cap_block = value
        elif attr == 'start_price':
            self.start_price = value
        elif attr == 'on_off':
            self.on_off = value
        elif attr == 'pf_min':
            self.pf_min = value
        elif attr == 'com_in':
            self.com_in = value
        elif attr == 'com_out':
            self.com_out = value
        elif attr == 'ratio':
            self.ratio = value
        elif attr == 'ratio_min':
            self.ratio_min = value
        elif attr == 'exist':
            self.exist = value
        else:
            raise ValueError('no valid attribute found')


class transmisson:
    def __init__(self, name='', site_in='', site_out='', commodity='', eff='1', inv_cost='0',
                 fix_cost='0', var_cost='0', inst_cap='0', cap_lo='0', cap_up='inf', wacc='0.07', depreciation='30',
                 reactance='', difflimit='', base_voltage='', tra_block='',exist=1):
        self.name = name
        self.site_in = site_in
        self.site_out = site_out
        self.commodity = commodity
        self.eff = eff
        self.inv_cost = inv_cost
        self.fix_cost = fix_cost
        self.var_cost = var_cost
        self.inst_cap = inst_cap
        self.cap_lo = cap_lo
        self.cap_up = cap_up
        self.wacc = wacc
        self.depreciation = depreciation
        self.reactance = reactance
        self.difflimit = difflimit
        self.base_voltage = base_voltage
        self.tra_block = tra_block
        self.exist = exist
    
    def set_attr_value(self, attr, value):
        if attr == 'name':
            self.name = value
        elif attr == 'site_in':
            self.site_in = value
        elif attr == 'site_out':
            self.site_out = value
        elif attr == 'commodity':
            self.commodity = value
        elif attr == 'eff':
            self.eff = value
        elif attr == 'inv_cost':
            self.inv_cost = value
        elif attr == 'fix_cost':
            self.fix_cost = value
        elif attr == 'var_cost':
            self.var_cost = value
        elif attr == 'inst_cap':
            self.inst_cap = value
        elif attr == 'cap_lo':
            self.cap_lo = value
        elif attr == 'cap_up':
            self.cap_up = value
        elif attr == 'wacc':
            self.wacc = value
        elif attr == 'depreciation':
            self.depreciation = value
        elif attr == 'reactance':
            self.reactance = value
        elif attr == 'difflimit':
            self.difflimit = value
        elif attr == 'base_voltage':
            self.base_voltage = value
        elif attr == 'tra_block':
            self.tra_block = value
        elif attr == 'exist':
            self.exist = value
        else:
            raise ValueError('no valid attribute found')


class storage:
    def __init__(self, name='', commodity='', inst_cap_c='0', cap_lo_c='0', cap_up_c='inf', 
                 inst_cap_p='0', cap_lo_p='0', cap_up_p='inf', eff_in='1', eff_out='1', inv_cost_p='0', inv_cost_c='0',
                 fix_cost_p='0', fix_cost_c='0', var_cost_p='0', var_cost_c='0', wacc='0.07', depreciation='20',
                 init='', discharge='0', ep_ratio='3', c_block='', p_block='', exist=1):
        self.name = name
        self.commodity = commodity
        self.inst_cap_p = inst_cap_p
        self.cap_lo_p = cap_lo_p
        self.cap_up_p = cap_up_p
        self.inst_cap_c = inst_cap_c
        self.cap_lo_c = cap_lo_c
        self.cap_up_c = cap_up_c
        self.eff_in = eff_in
        self.eff_out = eff_out
        self.inv_cost_p = inv_cost_p
        self.fix_cost_p = fix_cost_p
        self.var_cost_p = var_cost_p
        self.inv_cost_c = inv_cost_c
        self.fix_cost_c = fix_cost_c
        self.var_cost_c = var_cost_c
        self.wacc = wacc
        self.depreciation = depreciation
        self.init = init
        self.discharge = discharge
        self.ep_ratio = ep_ratio
        self.c_block = c_block
        self.p_block = p_block
        self.exist = exist

    def set_attr_value(self, attr, value):
        if attr == 'name':
            self.name = value
        elif attr == 'commodity':
            self.commodity = value
        elif attr == 'inst_cap_p':
            self.inst_cap_p = value
        elif attr == 'cap_lo_p':
            self.cap_lo_p = value
        elif attr == 'cap_up_p':
            self.cap_up_p = value
        elif attr == 'inst_cap_c':
            self.inst_cap_c = value
        elif attr == 'cap_lo_c':
            self.cap_lo_c = value
        elif attr == 'cap_up_c':
            self.cap_up_c = value
        elif attr == 'eff_in':
            self.eff_in = value
        elif attr == 'eff_out':
            self.eff_out = value
        elif attr == 'inv_cost_p':
            self.inv_cost_p = value
        elif attr == 'fix_cost_p':
            self.fix_cost_p = value
        elif attr == 'var_cost_p':
            self.var_cost_p = value
        elif attr == 'inv_cost_c':
            self.inv_cost_c = value
        elif attr == 'fix_cost_c':
            self.fix_cost_c = value
        elif attr == 'var_cost_c':
            self.var_cost_c = value
        elif attr == 'wacc':
            self.wacc = value
        elif attr == 'depreciation':
            self.depreciation = value
        elif attr == 'init':
            self.init = value
        elif attr == 'discharge':
            self.discharge = value
        elif attr == 'ep_ratio':
            self.ep_ratio = value
        elif attr == 'c_block':
            self.c_block = value
        elif attr == 'p_block':
            self.p_block = value
        elif attr == 'exist':
            self.exist = value
        else:
            raise ValueError('no valid attribute found')


class demand:
    def __init__(self, commodity=commodity(), value=[]):
        self.commodity = commodity
        self.value = value


class supim:
    def __init__(self, commodity=commodity(), value=[]):
        self.commodity = commodity
        self.value = value


class time_var_eff:
    def __init__(self, process=process(), value=[]):
        self.process = process
        self.value = value


class site:
    def __init__(self, name='', commodities=[], processes=[], transmissions=[], storages=[], demands=[], supim=[],
                 buy_sell_prices=[], time_var_eff=[], area='', base_voltage='', min_voltage='', ref_node='', pp_id=0,
                 building_id=0):
        self.name = name
        self.commodities = commodities
        self.processes = processes
        self.transmissions = transmissions
        self.storages = storages
        self.demands = demands
        self.supim = supim
        self.buy_sell_prices = buy_sell_prices
        self.time_var_eff = time_var_eff
        self.area = area
        self.base_voltage = base_voltage
        self.min_voltage = min_voltage
        self.ref_node = ref_node
        self.pp_id = pp_id
        self.building_id = building_id