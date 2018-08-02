#coding:utf-8  
import jieba
from gensim import models
import numpy as np
import gensim.models.word2vec as w2v
import sys,os
import io
from sklearn import preprocessing

CODE_TYPE = 'gb18030'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=CODE_TYPE)

fin = open('D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\civil_case\\yuliaoku.txt','r')
with open('D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\yuliaoku_segmented.txt','wb') as fou:
  line = fin.readline()
  while line:
      newline = jieba.cut(line,cut_all = False)
      str_out = ' '.join(newline).replace('，','').replace('。','').replace('？','').replace('！','')\
        .replace('“','').replace('”','').replace('：','').replace('‘','').replace('’','').replace('-','')\
        .replace('（','').replace('）','').replace('《','').replace('》','').replace('；','').replace('·','')\
        .replace('、','').replace('…','').replace('.','').replace(',','').replace('?','').replace('!','')\
        .replace(':','').replace('\n','').replace('[','').replace(']','').replace('{','').replace('}','')\
        .replace('【','').replace('】','').replace('￥','').replace('$','').replace('#','').replace('@','')\
        .replace('&','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','')\
        .replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('a','')\
        .replace('b','').replace('c','').replace('d','').replace('e','').replace('f','').replace('g','')\
        .replace('h','').replace('i','').replace('j','').replace('k','').replace('l','').replace('m','')\
        .replace('n','').replace('o','').replace('p','').replace('q','').replace('r','').replace('s','')\
        .replace('t','').replace('u','').replace('v','').replace('w','').replace('x','').replace('y','')\
        .replace('z','').replace('A','').replace('B','').replace('C','').replace('D','').replace('E','')\
        .replace('F','').replace('G','').replace('H','').replace('I','').replace('J','').replace('K','')\
        .replace('L','').replace('M','').replace('N','').replace('O','').replace('P','').replace('Q','')\
        .replace('R','').replace('S','').replace('T','').replace('U','').replace('V','').replace('W','')\
        .replace('X','').replace('Y','').replace('Z','').replace('+','').replace('*','').replace('~','')\
        .replace('/','').replace(';','').replace('／','').replace('<','').replace('>','')
      fou.write(str_out.encode('utf-8'))
      line = fin.readline()
fin.close()
fou.close()

#model training 
model_file_name = 'D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\writ_vector.bin'
sentences = w2v.LineSentence('D:\\FDU\\Template\\NLP(ZhipengXie)\\Spider\\yuliaoku_segmented.txt')  
model = w2v.Word2Vec(sentences, size=50, window=5, min_count=1, workers=4)   
model.save(model_file_name)  

#Model = models.KeyedVectors.load_word2vec_format(model_file_name,binary = True,unicode_errors = 'ignore')

max_str_len = 23
title_num = 0
title_split = []
for i in range(0,500):
  try:
    str_temp = "D:\\FDU\\Template\\NLP(ZhipengXie)\\data\\data_"+str(i)+"_cooked.txt"
    word_str = open(str_temp).readline()
    newline_temp = jieba.cut(word_str,cut_all = False)
    str_out = ' '.join(newline_temp).replace('，','').replace('。','').replace('？','').replace('！','')\
      .replace('“','').replace('”','').replace('：','').replace('‘','').replace('’','').replace('-','')\
      .replace('（','').replace('）','').replace('《','').replace('》','').replace('；','').replace('·','')\
      .replace('、','').replace('…','').replace('.','').replace(',','').replace('?','').replace('!','')\
      .replace(':','').replace('\n','').replace('[','').replace(']','').replace('{','').replace('}','')\
      .replace('【','').replace('】','').replace('￥','').replace('$','').replace('#','').replace('@','')\
      .replace('&','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','')\
      .replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('a','')\
      .replace('b','').replace('c','').replace('d','').replace('e','').replace('f','').replace('g','')\
      .replace('h','').replace('i','').replace('j','').replace('k','').replace('l','').replace('m','')\
      .replace('n','').replace('o','').replace('p','').replace('q','').replace('r','').replace('s','')\
      .replace('t','').replace('u','').replace('v','').replace('w','').replace('x','').replace('y','')\
      .replace('z','').replace('A','').replace('B','').replace('C','').replace('D','').replace('E','')\
      .replace('F','').replace('G','').replace('H','').replace('I','').replace('J','').replace('K','')\
      .replace('L','').replace('M','').replace('N','').replace('O','').replace('P','').replace('Q','')\
      .replace('R','').replace('S','').replace('T','').replace('U','').replace('V','').replace('W','')\
      .replace('X','').replace('Y','').replace('Z','').replace('+','').replace('*','').replace('~','')\
      .replace('/','').replace(';','').replace('／','').replace('<','').replace('>','')
    str_list = str_out.split()
    max_str_len = max(len(str_list),max_str_len)
    title_split.append(str_list)
    title_num += 1
  except Exception as err:
    continue

title_vec = np.ones(max_str_len*50)
for t in range(title_num):
  str_list = title_split[t]
  str_np = model.wv[str_list[0]]
  for j in range(1,len(str_list)):
    str_np = np.hstack((str_np,model.wv[str_list[j]]))
  for k in range(len(str_list),max_str_len):
    str_np = np.hstack((str_np,np.zeros(50)))
  title_vec = np.vstack((title_vec,str_np))

title_vec_N = preprocessing.normalize(title_vec)
res_simi = []
for i in range(1,title_num+1):
  res_temp = []
  for j in range(1,title_num+1):
    if i != j:
      res_temp.append(np.dot(title_vec_N[i],title_vec_N[j]))
    else:
      res_temp.append(-1)
  res_simi.append(res_temp)

for s in range(title_num):
  if max(res_simi[s]) > 0.8:
    print('s:'+str(s)+' '+str(res_simi[s].index(max(res_simi[s]))))

#print(model.wv['天津'])
