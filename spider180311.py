#coding:utf-8
# import scrapy
import requests
# import urllib3
import sys
from bs4 import BeautifulSoup as bs

'''
url of zhidao question consists of:target_url+question_number+.html
the question is:how can question_number be generated?
'''

target_url = 'https://zhidao.baidu.com/search'
#https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=%B4%F2%D3%F0%C3%AB%C7%F2%D4%F5%C3%B4%CE%D5%C5%C4
#https://zhidao.baidu.com/question/564519151.html?fr=iks&word=%B4%F2%D3%F0%C3%AB%C7%F2%D4%F5%C3%B4%CE%D5%C5%C4&ie=gbk
#https://zhidao.baidu.com/search?word=%B4%F2%D3%F0%C3%AB%C7%F2%D4%F5%C3%B4%CE%D5%C5%C4&ie=gbk&site=-1&sites=0&date=0&pn=10
#keyword = input("search questions:")
keyword = "描写爸爸的英语小短文"

k = 0#k is used to count how many questions there are
for i in range(0,76):
	payload = {'lm':'0','rn':'10','pn':str(i)+'0','fr':'search','ie':'gbk','word':keyword}
	#to get one page's url
	r = requests.get(target_url,params = payload)
	r.encoding = 'gbk'
	bs_obj = bs(r.text,'lxml')
	'''to locate where the target urls are first'''
	for link in bs_obj.find_all('a'):
		ques_url = link.get('href')
		if(isinstance(ques_url,str) and ques_url.find('zhidao.baidu.com') > 0 and ques_url.find('question') > 0 and ques_url[-3:] == 'gbk'):
			#to get each page's url
			temp_obj = requests.get(ques_url)
			temp_obj.encoding = 'gbk'
			temp_text = bs(temp_obj.text,'lxml')
			res_ques = temp_text.find_all('span',{'class':'ask-title'})

			#prepare to write something into your .txt
			file_path = "D:\\FDU\\Template\\NLP(ZhipengXie)\\Corpus\\180316.txt"
			str_file = open(file_path,'a',encoding = 'utf-8')

			#to get questions_string
			str_ques = res_ques[0].text
			str_ques = 'Q'+str(k+1)+':'+str_ques+'\n'
			str_file.write(str_ques)
			k = k+1


			#to get answers_string_best-answer
			res_ans = temp_text.find_all('pre',{'accuse':'aContent'})
			ans_len = len(res_ans)
			for j in range(ans_len):
				add_str = res_ans[j].text
				add_str = 'A'+str(j)+':'+add_str+'\n'
				str_file.write(add_str)
			
			#to get answers_string_no-best-answer
			res_ans = temp_text.find_all('div',{'accuse':'aContent'})
			#print(len(res_ans))
			#ans_len:the number of answers
			ans_len = len(res_ans)
			for j in range(ans_len):
				#ans_len_1 = len(res_ans[j])
				#print(type(res_ans[j]))
				#print(len(res_ans[j]))
				#if not res_ans[j].has_attr('img'):
				add_str = res_ans[j].text
				add_str = 'A'+str(j+1)+':'+add_str+'\n'
				str_file.write(add_str)
