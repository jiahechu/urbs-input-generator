import parameters
import generate_structure
import generate_tuples
import pandas as pd


parameters
generate_structure
generate_tuples

writer = pd.ExcelWriter(parameters.save_path, engine='xlsxwriter',
                        engine_kwargs={'options': {'strings_to_numbers': True}})
generate_tuples.global_df.to_excel(writer, sheet_name='Global', index=False)
generate_tuples.site_df.to_excel(writer, sheet_name='Site', index=False)
generate_tuples.commodity_df.to_excel(writer, sheet_name='Commodity', index=False)
generate_tuples.process_df.to_excel(writer, sheet_name='Process', index=False)
generate_tuples.process_commodity_df.to_excel(writer, sheet_name='Process-Commodity', index=False)
generate_tuples.transmission_df.to_excel(writer, sheet_name='Transmission', index=False)
generate_tuples.storage_df.to_excel(writer, sheet_name='Storage', index=False)
generate_tuples.demand_df.to_excel(writer, sheet_name='Demand', index=False)
generate_tuples.supim_df.to_excel(writer, sheet_name='SupIm', index=False)
generate_tuples.buy_sell_df.to_excel(writer, sheet_name='Buy-Sell-Price', index=False)
generate_tuples.timevareff_df.to_excel(writer, sheet_name='TimeVarEff', index=False)
writer.save()
# writer.close()