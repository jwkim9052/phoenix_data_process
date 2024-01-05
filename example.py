################################ simple usage ##########################################
from phoenix_data_mix import PhoenixDataMix


data_root="/media/kevin/seagate_ssd/phoenix2014-release/phoenix-2014-multisigner"
result_root="./data"
phoenix = PhoenixDataMix(data_root, result_root)

#res = phoenix.mix("data01", '01February_2011_Tuesday_heute_default-5', 3, 'MINUS', 
#            '01December_2011_Thursday_tagesschau_default-7', 5, 'MINUS')
#if res:
#    print("mix done!")
#else:
#    print("mix failed!")

phoenix.pick_one('dir_name', '01February_2011_Tuesday_heute_default-5', 1)
phoenix.pick_one('dir_name', '01February_2011_Tuesday_heute_default-5', 3)
phoenix.pick_one('dir_name', '06June_2010_Sunday_tagesschau_default-2', 10)
phoenix.pick_one('dir_name', '06June_2010_Sunday_tagesschau_default-2', 11)
phoenix.pick_one('dir_name', '06June_2010_Sunday_tagesschau_default-2', 12)
phoenix.pick_one('dir_name', '06June_2010_Sunday_tagesschau_default-2', 13)
#phoenix.print_id_files('06June_2010_Sunday_tagesschau_default-2')

########################################################################################
#print("=================================================")
#phoenix.print_id_files('01February_2011_Tuesday_heute_default-5') # minus 3   - 16 png
#phoenix.print_id_files('01December_2011_Thursday_tagesschau_default-7') # minus 5 - 12 png

#phoenix.print_id_files('06January_2010_Wednesday_tagesschau_default-12') # __ON__ 0 - 6 png __OFF__ 4 - 5 png
#phoenix.print_id_files('06January_2011_Thursday_tagesschau_default-5') # __ON__ 6  - 11 png
#res = phoenix.mix("data02", '06January_2010_Wednesday_tagesschau_default-12', 0, '__ON__', 
#            '06January_2011_Thursday_tagesschau_default-5', 6, '__ON__')
#
#phoenix.print_id_files('06January_2010_Wednesday_tagesschau_default-10') # __OFF__ 5 - 6 png
#
#res = phoenix.mix("data03", '06January_2010_Wednesday_tagesschau_default-12', 4, '__OFF__', 
#            '06January_2010_Wednesday_tagesschau_default-10', 5, '__OFF__')
#
#phoenix.print_id_files('06May_2010_Thursday_heute_default-9') # __OFF__ 2 - 6 png 
#
#
#res = phoenix.mix("data04", '06May_2010_Thursday_heute_default-9', 2, '__OFF__',  # 2 -> 3
#            '06January_2010_Wednesday_tagesschau_default-10', 5, '__OFF__')
