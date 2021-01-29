import os
import torch
import glob
import itertools
from statistics import mean
import transformers as ppb
import torch.quantization
import torch.nn as nn
from torch.nn.functional import softmax
import multiprocessing as mp
import numpy as np
import time
import json

from transformers import BertTokenizer, BertForNextSentencePrediction
path = os.getcwd()
tokenizer = BertTokenizer.from_pretrained(path + '/bert-base-multilingual-uncased/')
model = BertForNextSentencePrediction.from_pretrained(path + "/bert-base-multilingual-uncased/")

quantized_model = torch.quantization.quantize_dynamic(model, {nn.LSTM, nn.Linear}, dtype=torch.qint8)
def print_size_of_model(model):
    torch.save(model.state_dict(), "temp.p")
    os.remove('temp.p')

def comp(analise):
  FrasesComp2 = []
  Listao= []
  combinations = itertools.combinations(analise, 2)
  for a, b in combinations:
    encoded = tokenizer.encode_plus(a, text_pair=b, return_tensors='pt')
    seq_relationship_logits = model(**encoded)[0]
    probs = softmax(seq_relationship_logits, dim=1)
    dd = probs.detach().numpy()
    valor = (dd[0, 0])
    if valor < 0.75:
      FrasesComp2.append(b)
      FrasesComp2.append(a)
  Lista = {i:FrasesComp2.count(i) for i in set(FrasesComp2)}
  Ranking2 = sorted(Lista, key=Lista.get, reverse=True)[:25]
  return Ranking2
		
def Tudo(caminho):
    with open(caminho, 'r', encoding = 'utf-8-sig') as file:
       data = file.read().lower()
       data = data.split('\n')
       data = [x for x in data if x] 
       #print(data)
       FrasesComp = []
       Listao= []
       combinations = itertools.combinations(data, 2)
    for a, b in combinations:
       encoded = tokenizer.encode_plus(a, text_pair=b, return_tensors='pt')
       seq_relationship_logits = model(**encoded)[0]
       probs = softmax(seq_relationship_logits, dim=1)
       dd = probs.detach().numpy()
       valor = (dd[0, 0])
       if valor < 0.8:
         FrasesComp.append(b)
         FrasesComp.append(a)
    Lista = {i:FrasesComp.count(i) for i in set(FrasesComp)}

    Ranking = sorted(Lista, key=Lista.get, reverse=True)[:5]
    print(Ranking)
    return Ranking
    
Listao = []
def get_result(result):
    Listao.append(result)

if __name__ == '__main__':
    
    Path = os.getcwd()
    print(Path)
    read_files = glob.glob(Path + "/ArquivosTxT/*.txt")
    with open(Path + "/result/result.txt", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    list = os.listdir(Path + '/ArquivosTxT/') 

    number_files = 10
    
    file = open(Path + "/result/result.txt","r",encoding = "utf-8-sig") 
    Counter = 0 
    Content = file.read() 
    CoList = Content.split("\n") 
    for i in CoList: 
       if i: 
          Counter += 1

    lines_per_file = round(Counter/number_files)
    smallfile = None

    with open(Path + '/result/result.txt', encoding = "utf-8-sig") as bigfile:
       for lineno, line in enumerate(bigfile):
           if lineno % lines_per_file == 0:
              if smallfile:
                  smallfile.close()
              small_filename = Path + '/todos/{}.txt'.format(lineno + lines_per_file)
              smallfile = open(small_filename, "w", encoding = "utf-8-sig")
           smallfile.write(line)
       if smallfile:
           smallfile.close()
          
          
    results = []
    ts = time.time()
    pool = mp.Pool(6)

    filelist = os.listdir(Path + "/todos/")

    for i in filelist:
        pool.apply_async(Tudo, args=(Path + "/todos/" + i,), callback=get_result)
    pool.close()
    pool.join()
    print('Time in parallel:', time.time() - ts)

    tt = []
    for item in Listao:
       for i in item:
          tt.append(i)
    
    for item in tt:
      print(item)
    
    hh = comp(tt)
    print(hh)
    
    Tudo = {}
    filelist = os.listdir(Path + "/ArquivosTxT/")
    from collections import defaultdict
    Tudo = defaultdict(lambda:[])
    for x in filelist:
       if x.endswith(".txt"):
          nome = os.path.basename(x)
          with open(Path + "/ArquivosTxT/" + x, encoding = 'utf-8') as y:
            content = y.readlines()
            content = [s.replace('\n', '') for s in content]
            for num, line in enumerate(content, 1):
               line = line.lower()
               for i in tt:
                  if i == line:
                    Tudo[nome].append(num)
    finalmente = dict(Tudo)
    
    
    with open('Resultado.txt','w') as f:
        f.write("Sentenças suspeitas\n\n")
        for item in hh:
          f.write("%s\n" % item)
        f.write("\n\nArquivos e o número da linha onde há uma das sentenças suspeitas\n\n")
        f.write((json.dumps(finalmente)))
        f.close