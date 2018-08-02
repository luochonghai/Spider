import sys,os
from bs4 import BeautifulSoup as bs
import re
CODE_TYPE = 'gb18030'

def extract_text(file_path):
    #read data
    fh = open(file_path,"r",errors = 'ignore')#encoding = 'gb18030'
    raw_datas = fh.read()
    new_data = raw_datas#used to catch 'legalbase' text

    if len(raw_datas) < 150:
        fh.close()
        return 
    fh.close()
    #to find the accurate scope of text body
    sta_pos = raw_datas.find('Html\\\":\\\"')
    end_pos = raw_datas.rfind("</div>")
    raw_data = raw_datas[sta_pos+9:end_pos+6]
    temp_str_list = file_path.split(".")
    #new_file_paths = temp_str_list[0]+"_cooked.txt"
    #new_file_path = new_file_paths.replace("ws","data")
    new_file_path = "D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\civil_case\\yuliaoku.txt"
    # write data
    fw = open(new_file_path,"a+",errors = 'ignore')
    #bs_obj = bs(raw_data,"html.parser")
    ##bs_obj.prettify()
    #list_div = bs_obj.find_all("div")
    
    #used to get title and treat it as the key words extracted from the writ
    title_writ = re.findall(r"attr\(\"title\"\,\"(.+?)\"\)\;\$\(\"\#tdSource",raw_datas)[0]
    fw.write(title_writ+'\n')

    #used to get the function part
    # legal_raw = re.search(r"LegalBase:(.+?)length",new_data)
    # leg_sta,leg_end = legal_raw.span()
    # if leg_end-leg_sta > 20:
    #     legal_fir = new_data[leg_sta:leg_end]
    #     legal_spl = legal_fir.split("法规名称:")
    #     for l1 in range(1,len(legal_spl)):
    #         temp_rule_name = re.findall(r"(.+?),Items",legal_spl[l1])[0]
    #         legal_aspl = legal_spl[l1].split("法条名称:")
    #         for l2 in range(1,len(legal_aspl)):
    #             temp_text_name = re.findall(r"(.+?),法条内容",legal_aspl[l2])[0]
    #             if len(temp_text_name) == 2:
    #                 fw.write(re.findall(r"法条内容:\'(.+?)\[ly\]",legal_aspl[l2])[0])
    #             else:
    #                 fw.write(re.sub('\'','',temp_rule_name+temp_text_name)+'\n')

    #used to catch the reason part 
    seg_type = ["WBSB","DSRXX","SSJL","AJJBQK","CPYZ","PJJG","WBWB"]
    #对应于：首部，（unknown），事实，理由，案件基本情况，判决结果，尾部
    seg_list = []
    for seg_i in seg_type:
        seg_temp = raw_data.find("<a type=\'dir\' name=\'"+seg_i+"\'>")
        if seg_temp < 0:
            if len(seg_list) == 0:
                seg_temp = 0
            else:
                seg_temp = seg_list[-1]
        seg_list.append(seg_temp)
    raw_list = [raw_data[0:seg_list[0]]]
    for raw_i in range(6):
        raw_list.append(raw_data[seg_list[raw_i]:seg_list[raw_i+1]])
    raw_list.append(raw_data[seg_list[-1]:])

    for str_temp in raw_list:
        bs_obj = bs(str_temp,"html.parser")
        list_div = bs_obj.find_all("div")
        temp_res = ""
        for str_cook in list_div:
            if str_cook.text != "":
                temp_res += str_cook.text+'\n'
        fw.write(temp_res)
    result_str = ""
    for str_temp in list_div:
        result_str += str_temp.text+'\n'
    fw.close()

if __name__ == "__main__":
    #extract_text("D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\civil_case\\data\\ws_9.txt")
    extract_text("D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\f.txt")
