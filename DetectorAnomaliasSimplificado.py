import os, re, sys, glob, shutil, hashlib, threading, itertools
import numpy as np
import spacy
import warnings
from collections import OrderedDict
from multiprocessing import Process, freeze_support

path = os.getcwd()
pln = spacy.load(path + '\modeloSpacyLG\pt_core_news_lg\pt_core_news_lg-3.0.0')
warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

def comparar(data, filtro):
    selecao = 1
    FrasesComp = []
    Listao= []
    combinations = itertools.combinations(data, 2)
    for a, b in combinations:
       aa = pln(a)
       bb = pln(b)
       valor = aa.similarity(bb)
       if valor < filtro:
         FrasesComp.append(b)
         FrasesComp.append(a)
    Lista = {i:FrasesComp.count(i) for i in set(FrasesComp)}
    Ranking = sorted(Lista, key=Lista.get, reverse=True)[:selecao]
    return Ranking

def digitar_filtro():
    # Interação com o Usuário
    print("\nDetector de Anomalias\n")
    print("O limite de filtro deve estar entre 0.1 e 0.99")    
    while True:
      try:
        filtro = float(input("Digite o limite para a analise ou enter para default(0.8): ") or "0.8")
        if 0.99 > filtro > 0.1:
          break
          print("Número fora dos limites")
      except Exception as e:
        print(e)
    return filtro
    
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))
    
if __name__ == '__main__':

  #Lê os arquivos na pasta análise e armazena na lista content
  for file in os.listdir(path + "/analise"):
     if file.endswith(".txt"):
        with open(path + "/analise/" + file,encoding = "utf-8-sig") as fn:
           content = fn.read().splitlines()
  
  #Data Clean
  FrasesSeparadas = []
  for item in content:
    item = re.split('[,.!?]', str(item).lower())
    FrasesSeparadas.append(item)
  FrasesSeparadas = ([j for i in FrasesSeparadas for j in i])
  unwanted = {'', ' '} 
  FrasesSeparadas = [x for x in FrasesSeparadas if x not in unwanted]
  FrasesSeparadas = [x for x in FrasesSeparadas if ' ' in x]
  FrasesSeparadas = [s.strip() for s in FrasesSeparadas]
  FrasesSeparadas = [x for x in FrasesSeparadas if any(y in x for y in ' ')]
  
  #Conta o número de linhas
  Counter = 0 
  for i in FrasesSeparadas:
    if i:
      Counter += 1
  lines_per_file = round(Counter/(Counter*0.05))
  
  #Dividi a lista em tamanho iguais
  Partes = (list(chunks(FrasesSeparadas,lines_per_file)))
  
  #Recebe o valor do filtro
  filtro = digitar_filtro()

  #Comparação das linhas
  Listao = []
  def ComparacaoArquivos(filelist):
     for item in filelist:
        resultado = comparar(item,filtro)
        Listao.append(resultado)
     return      
  ComparacaoArquivos(Partes)
  print(Listao)