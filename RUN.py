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

from transformers import BertTokenizer, BertForNextSentencePrediction
tokenizer = BertTokenizer.from_pretrained('C:/Users/kenny.ksn/Desktop/pararelo/bert-base-portuguese-cased_pytorch_checkpoint/')
model = BertForNextSentencePrediction.from_pretrained("C:/Users/kenny.ksn/Desktop/pararelo/bert-base-portuguese-cased_pytorch_checkpoint/")

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
    if valor < 0.9:
      FrasesComp2.append(b)
      FrasesComp2.append(a)
  Lista = {i:FrasesComp2.count(i) for i in set(FrasesComp2)}
  return Lista
		
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
       if valor < 0.9:
         FrasesComp.append(b)
         FrasesComp.append(a)
    Lista = {i:FrasesComp.count(i) for i in set(FrasesComp)}
    Listao.append(Lista)
    return Listao
	
def get_result(result):
    global results
    results.append(result)

if __name__ == '__main__':

    read_files = glob.glob("C:/Users/kenny.ksn/Desktop/pararelo/ttt/*.txt")
    with open("C:/Users/kenny.ksn/Desktop/pararelo/result/result.txt", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    list = os.listdir('C:/Users/kenny.ksn/Desktop/pararelo/ttt/') 
    number_files = len(list)

    file = open("C:/Users/kenny.ksn/Desktop/pararelo/result/result.txt","r",encoding = "utf-8-sig") 
    Counter = 0 
    Content = file.read() 
    CoList = Content.split("\n") 
    for i in CoList: 
       if i: 
          Counter += 1

    lines_per_file = round(Counter/number_files)
    smallfile = None
    with open('C:/Users/kenny.ksn/Desktop/pararelo/result/result.txt', encoding = "utf-8-sig") as bigfile:
       for lineno, line in enumerate(bigfile):
           if lineno % lines_per_file == 0:
              if smallfile:
                  smallfile.close()
              small_filename = 'C:/Users/kenny.ksn/Desktop/pararelo/todos/{}.txt'.format(lineno + lines_per_file)
              smallfile = open(small_filename, "w", encoding = "utf-8-sig")
           smallfile.write(line)
       if smallfile:
           smallfile.close()
          
          
    results = []
    ts = time.time()
    pool = mp.Pool(mp.cpu_count())
    Path = "C:/Users/kenny.ksn/Desktop/pararelo/todos/"
    filelist = os.listdir(Path)
    for i in filelist:
        pool.apply_async(Tudo, args=(Path + i,), callback=get_result)
    pool.close()
    pool.join()
    print('Time in parallel:', time.time() - ts)
    #print(results)
    primeira = results.pop()
    Final = []
    for item in primeira:
      for k, v in item.items():
         if v > 10:
            Final.append(k)
    #print(Final)
    
    FreqComp2 = []
    segunda = comp(Final)
    
    media = mean(segunda[k] for k in segunda)
    Final2 = []
    for i in segunda:
       if segunda[i] > (media*1):
          Final2.append(i)
          #print(i, segunda[i])

    Ranking2 = sorted(segunda, key=segunda.get, reverse=True)[:20]
    print(Ranking2)
    Path = "C:/Users/kenny.ksn/Desktop/pararelo/todos/"
    
    Tudo = {}
    filelist = os.listdir(Path)
    from collections import defaultdict
    Tudo = defaultdict(lambda:[])
    for x in filelist:
       if x.endswith(".txt"):
          nome = os.path.basename(x)
          with open(Path + x, encoding = 'utf-8') as y:
            content = y.readlines()
            content = [s.replace('\n', '') for s in content]
            for num, line in enumerate(content, 1):
               line = line.lower()
               for i in Ranking2:
                  if i in line:
                    Tudo[nome].append(num)
    print(dict(Tudo))