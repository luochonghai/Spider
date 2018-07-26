import sys,os
from bs4 import BeautifulSoup as bs

def extract_text(file_path):
    #read data
    fh = open(file_path,"r")
    raw_data = fh.read()
    if len(raw_data) < 50:
        fh.close()
        return 
    fh.close()
    temp_str_list = file_path.split(".")
    new_file_path = temp_str_list[0]+"_cooked.txt"
    #write data
    fw = open(new_file_path,"a+")
    bs_obj = bs(raw_data,"html.parser")
    #bs_obj.prettify()
    list_div = bs_obj.find_all("div")
    result_str = ""
    for str_temp in list_div:
        result_str += str_temp.text+'\n'
    print(result_str)
    fw.write(result_str)
    fw.close()
