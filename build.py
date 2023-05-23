# -*- coding: utf-8 -*-
import glob
import json
from predatanew import get_conf
from datetime import date
import spacy
from sklearn.model_selection import train_test_split
list_file=[]
y_train = []
y_test = []
val = []
val_test_sizq=0.1
for i in sorted(list(glob.glob("./data/*.txt"))):
    _temp = get_conf(i)
    _news=[]
    for j in _temp:
        if j["text"] not in list_file:
            _news.append(j)
    list_file.extend([k["text"] for k in _news])
    _temp=_news
    print(i)
    print(len(_temp))
    #print(_temp)
    _y_train, _y_test = train_test_split(_temp, test_size=val_test_sizq, random_state=42)
    _y_train, _val = train_test_split(_y_train, test_size=float(val_test_sizq/(1.0-val_test_sizq)), random_state=42) # x x 0.9 = 0.1
    y_train.extend(_y_train)
    y_test.extend(_y_test)
    val.extend(_val)
#print(y_train)
print("all data size : "+str(len(y_train)+len(y_test)+len(val)))
print("train size : "+str(len(y_train)))
print("val size : "+str(len(val)))
print("test size : "+str(len(y_test)))
text_train=""
for index,i in enumerate(y_train):
    text_train+=json.dumps(i,ensure_ascii=False)
    if index!=len(y_train)-1:
        text_train+='\n'
text_val=""
for index,i in enumerate(val):
    text_val+=json.dumps(i,ensure_ascii=False)
    if index!=len(val)-1:
        text_val+='\n'
text_test=""
for index,i in enumerate(y_test):
    text_test+=json.dumps(i,ensure_ascii=False)
    if index!=len(y_test)-1:
        text_test+='\n'
today=date.today()
str_today = str(date.today().day)+str(date.today().month)+str(date.today().year)
with open(f"dataset/train_{str_today}_newmm.jsonlines","w",encoding="utf-8") as f:
    f.write(text_train)
with open(f"dataset/val_{str_today}_newmm.jsonlines","w",encoding="utf-8") as f:
    f.write(text_val)
with open(f"dataset/test_{str_today}_newmm.jsonlines","w",encoding="utf-8") as f:
    f.write(text_test)