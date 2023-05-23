# -*- coding: utf-8 -*-
import codecs
def word_tokenize(text):
    return list(text)
from nltk.tokenize import RegexpTokenizer
import glob
import re
import spacy
import copy
import os
# thai cut

with open(os.path.join(".","data","repo.json"),"r",encoding="utf-8-sig") as f:
    reqo=eval(f.read())

thaicut="newmm"
CLEANR = re.compile('\$(.*?)\$') 
#จัดการประโยคซ้ำ
data_not=[]
# เตรียมตัวตัด tag ด้วย re
pattern = r'\[(.*?)\](.*?)\[\/(.*?)\]'
tokenizer = RegexpTokenizer(pattern) # ใช้ nltk.tokenize.RegexpTokenizer เพื่อตัด [TIME]8.00[/TIME] ให้เป็น ('TIME','ไง','TIME')
# จัดการกับ tag ที่ไม่ได้ tag
def toolner_to_tag(text):
 text=text.strip()
 text=re.sub('\{.*?\}','',text)
 text=re.sub("<[^>]*>","",text).replace("“",'"').replace("”",'"')
 text=re.sub("(\[\/(.*?)\])","\\1***",text)#.replace('(\[(.*?)\])','***\\1')# text.replace('>','>***') # ตัดการกับพวกไม่มี tag word
 text=re.sub("(\[\w+\])","***\\1",text)
 text2=[]
 for i in text.split('***'):
  if "[" in i:
   text2.append(i)
  else:
   text2.append("[word]"+i+"[/word]")
 text="".join(text2)#re.sub("[word][/word]","","".join(text2))
 #print("toolner_to_tag:" +text)
 return text.replace("[word][/word]","")

# เตรียมตัวตัด tag ด้วย re
pattern2 = r'\{(.*?)\}(.*?)\{\/(.*?)\}'
tokenizer2 = RegexpTokenizer(pattern2)
def toolner_to_tag2(text):
 text=text.strip()
 text=re.sub('\[.*?\]','',text)
 text=re.sub("<[^>]*>","",text).replace("“",'"').replace("”",'"')
 text=re.sub("(\{\/(.*?)\})","\\1***",text)#.replace('(\[(.*?)\])','***\\1')# text.replace('>','>***') # ตัดการกับพวกไม่มี tag word
 text=re.sub("(\{\w+\})","***\\1",text)
 text2=[]
 for i in text.split('***'):
  if "{" in i:
   text2.append(i)
  else:
   text2.append("{word}"+i+"{/word}")
 text="".join(text2)#re.sub("[word][/word]","","".join(text2))
 #print("toolner_to_tag2:" +text)
 return text.replace("{word}{/word}","")
# แปลง text ให้เป็น conll2002
def text2conll2002(text,pos=True):
    """
    ใช้แปลงข้อความให้กลายเป็น conll2002
    """
    text=toolner_to_tag(text)
    text=text.replace("''",'"')
    text=text.replace("’",'"').replace("‘",'"')#.replace(" ","<_>")#.replace(" ","<_>")#.replace('"',"")
    tag=tokenizer.tokenize(text)
    #print(tag)
    j=0
    conll2002=""
    for tagopen,text,tagclose in tag:
        word_cut=word_tokenize(text)
        i=0
        txt5=""
        while i<len(word_cut):
            if word_cut[i]=="''" or word_cut[i]=='"':pass
            elif i==0 and tagopen!='word' and (tagopen.startswith("p") or tagopen.startswith("g")):
                txt5+=word_cut[i]
                txt5+='\tB-'+tagopen
            elif tagopen!='word'  and (tagopen.startswith("p") or tagopen.startswith("g")):
                txt5+=word_cut[i]
                txt5+='\tI-'+tagopen
            else:
                txt5+=word_cut[i]
                txt5+='\t'+'Null'
            txt5+='\n'
            i+=1
        conll2002+=txt5
    return conll2002
def text2conll2002_2(text,pos=True):
    """
    ใช้แปลงข้อความให้กลายเป็น conll2002
    """
    text2=copy.copy(text)
    text2=toolner_to_tag2(text2)
    tag2=tokenizer2.tokenize(text2)
    j=0
    conll2002=""
    for tagopen,text,tagclose in tag2:
        word_cut=word_tokenize(text)
        i=0
        txt5=""
        while i<len(word_cut):
            if word_cut[i]=="''" or word_cut[i]=='"':pass
            elif i==0 and tagopen!='word' and tagopen.startswith("p"):
                txt5+=word_cut[i]
                txt5+='\tB-'+tagopen
            elif tagopen!='word' and tagopen.startswith("p"):
                txt5+=word_cut[i]
                txt5+='\tI-'+tagopen
            else:
                txt5+=word_cut[i]
                txt5+='\t'+'Null'
            txt5+='\n'
            i+=1
        conll2002+=txt5
    return conll2002
# อ่านข้อมูลจากไฟล์
def get_data(fileopen,wanghan=False):
	"""
    สำหรับใช้อ่านทั้งหมดทั้งในไฟล์ทีละรรทัดออกมาเป็น list
    """
	with codecs.open(fileopen, 'r',encoding='utf-8-sig') as f:
		lines = [i.strip().strip('​').replace("​","").replace("\\n"," ") for i in f.read().splitlines()]
	if wanghan:
		lines = [i.replace(" ","<_>") for i in lines]
	return lines # เอาไม่ซ้ำกัน

def alldata(lists):
    text=""
    for data in lists:
        text+=text2conll2002(data)
        text+='\n'
    return text


def alldata_list(lists):
    data_all=[]
    for data in lists:
        data_num=[]
        try:
            data2=copy.copy(data)
            txt=text2conll2002(data,pos=False).split('\n')
            txt2=text2conll2002_2(data2,pos=False).split('\n')
            u=False
            t=''
            for idx, d in enumerate(txt):
                tt=d.split('\t')
                tt2=txt2[idx].split('\t')
                if d!="":
                    if len(tt)==3:
                        data_num.append((tt[0],tt[1],tt[2]))
                    else:
                        data_num.append((tt[0],tt[1],tt2[1]))
            data_all.append(data_num)
        except:
            print("error ",data)
    return data_all

def alldata_list_str(lists):
	string=""
	for data in lists:
		string1=""
		for j in data:
			string1+=j[0]+"	"+j[1]+"	"+j[2]+"\n"
		string1+="\n"
		string+=string1
	return string

def get_data_tag(listd):
	list_all=[]
	c=[]
	for i in listd:
		if i !='':
			c.append((i.split("\t")[0],i.split("\t")[1],i.split("\t")[2]))
		else:
			list_all.append(c)
			c=[]
	return list_all
def getall(lista):
    ll=[]
    for i in lista:
        o=True
        if o==True:
            ll.append(i)
    return ll
def pre(text):
    return text.replace('B-','').replace('I-','')

def get_clusters_strings(v,text):
    _text = []
    for s,e in v:
        _temp = text[s:e]
        if isinstance(_temp,list):
            _text.append(''.join(_temp))
        else:
            _text.append(text[s:e])
    return _text
def get_clusters_strings2(v):
    _text = []
    for s,e in v:
        _text.append([s,e])
    return _text

def encode(example, nlp):
    if 'tokens' in example and example['tokens']:
        pass
    elif example['clusters']==[] and 'text' in example and example['text']:
        example['clusters'] = example['clusters']
        example['error'] = True
    elif 'text' in example and example['text']:
        clusters = example['clusters']
        spacy_doc = nlp(example['text'])
        tokens = [tok.text for tok in spacy_doc]
        #print("text: "+example['text'])

        new_clusters = []
        #new_clusters = [[(spacy_doc.char_span(start, end).start,spacy_doc.char_span(start, end).end - 1) for start, end in cluster] for cluster in clusters]
        for cluster in clusters:
            #print(clusters)
            _cluster=[]
            for start, end in cluster:
                try:
                    _cluster.append((spacy_doc.char_span(start, end).start,spacy_doc.char_span(start, end).end-1))
                except:
                    print(cluster)
                    print( start, end )
                    print(example['text'][start:end])
                    raise NotImplemented()
            if len(_cluster)>1:
                new_clusters.append(_cluster)
    else:
        raise ValueError(f"Example is empty: {example}")

def to_coref(data):
    #print(data)
    words=[[j[0] for j in i] for i in data][0]
    d={"text":re.sub('\[.*?]','',re.sub('\{.*?}','',''.join(words)))}
    tag=[]
    for i in data:
        for j in i:
            t=pre(j[1])
            if t not in tag and t!='Null':
                tag.append(t)
            t=pre(j[2])
            if t not in tag and t!='Null':
                tag.append(t)
    #print(tag)
    d["clusters"]=[]#*len(tag) #["mention_clusters"]
    d["clusters_strings"]=[]#*len(tag)
    o={}
    for i in tag:
        o[i]=[]
    for idx,i in enumerate(data):
        b=-1
        t=-1
        e=-1
        l=len(i)
        tt=""
        b2=-1
        t2=-1
        e2=-1
        tt2=""
        for in2,j in enumerate(i):
            if pre(j[1])=='Null' and b!=-1 and t!=-1:
                e=in2
                #print(d["mention_clusters"])
                o[tt].append([b,e])
                b=-1
                e=-1
                t=-1
                tt=''
            elif 'B-' in j[1] and in2<l-1:
                b=in2
                t=tag.index(pre(j[1]))
                #print(idx,in2,pre(j[1]),j[0],1,t)
                tt=pre(j[1])
            elif 'B-' in j[1] and in2==l-1:
                b=in2
                t=tag.index(pre(j[1]))
                tt=pre(j[1])
                e=in2+1
                o[tt].append([b,e])
            elif pre(j[1])!='Null' and in2==l-1:
                e=in2+1
                o[tt].append([b,e])
            if pre(j[2])=='Null' and b2!=-1 and t2!=-1:
                e2=in2
                #print(d["mention_clusters"])
                o[tt2].append([b2,e2])
                b2=-1
                e2=-1
                t2=-1
                tt2=''
            elif 'B-' in j[2] and in2<l-1:
                b2=in2
                t2=tag.index(pre(j[2]))
                #print(idx,in2,pre(j[1]),j[0],1,t)
                tt2=pre(j[2])
            elif 'B-' in j[2] and in2==l-1:
                b2=in2
                t2=tag.index(pre(j[2]))
                tt2=pre(j[2])
                e2=in2+1
                o[tt2].append([b2,e2])
            elif pre(j[2])!='Null' and in2==l-1:
                e2=in2+1
                o[tt2].append([b2,e2])
    for key, value in o.items():
        if len(value)<=1:
            continue
        value = sorted(value, key = lambda x: (x[0]))
        d["clusters"].append([])
        d["clusters_strings"].append([])
        d["clusters"][-1]=get_clusters_strings2(value)
        d["clusters_strings"][-1]=get_clusters_strings(value,words)
    return d
import spacy_pythainlp.core
nlp = spacy.blank("th")
nlp.add_pipe(
    "pythainlp", 
    config={
        "pos_engine": "perceptron",
        "pos": False,
        "pos_corpus": "orchid_ud",
        "sent_engine": "crfcut", 
        "sent": False,
        "ner_engine": "thainer",
        "ner": False,
        "tokenize_engine": "newmm",
        "tokenize": True,
        "dependency_parsing": False,
        "dependency_parsing_engine": "esupar",
        "dependency_parsing_model": None,
        "word_vector": False,
        "word_vector_model": "thai2fit_wv"
    }
)

def get_conf(path,wanghan=False):
    d=[]
    ok_reqo = reqo[os.path.basename(path)]
    _temp=[]
    for i in getall(get_data(path,wanghan)):
        try:
            _temp=to_coref(alldata_list([i]))
            encode(_temp,nlp)
            if _temp["clusters"]==[]:
                print(_temp)
                continue
            _i=0
            for ii in _temp["clusters"]:
                if ii==[]:
                    _i+=1
            if _i == len(_temp["clusters"]):
                continue
            _temp["source"]=ok_reqo
            d.append(_temp)
        except Exception as e:
            print(e)
            print("error : "+str(_temp))
    return d
'''
{"sentences":[[list ที่ตัดคำแล้วแต่ละประโยค idx],...],"mention_clusters":[[[sentence_idx, begin_idx, end_idx]],แต่ละชนิด,[[...,...,..],...] ]}
'''