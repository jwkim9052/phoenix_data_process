from phoenix_data_mix import PhoenixDataMix

PhoenixDataMix.DATA_ROOT="/media/kevin/seagate_ssd/phoenix2014-release/phoenix-2014-multisigner"
PhoenixDataMix.RESULT_ROOT="./jwkim_data"
phoenix = PhoenixDataMix()
master_dict = phoenix.get_master_dict()


print("------------------------------------------------------------------")

#
# 
#
res = phoenix.mix("data01", '01February_2011_Tuesday_heute_default-5', 3, 'MINUS', 
            '01December_2011_Thursday_tagesschau_default-7', 5, 'MINUS')
#print("=================================================")
#phoenix.print_id_files('01February_2011_Tuesday_heute_default-5') # minus 3   - 16 png
#phoenix.print_id_files('01December_2011_Thursday_tagesschau_default-7') # minus 5 - 12 png
