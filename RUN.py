import os
os.environ["PYTORCH_JIT"] = "0"
import glob
import time
import json
import re
import hashlib
import threading
import sys
import itertools
import shutil
import itertools
import numpy as np
import multiprocessing as mp
from torch.nn.functional import softmax
from multiprocessing import Process, freeze_support
from transformers import BertTokenizer, BertForNextSentencePrediction

from func import limpar, deEmojify, datacleaning

# Pegando os arquivos de configuração e importando o modelo de NSP
path = os.getcwd()
bert_file = '/drive/MyDrive/bert-base-multilingual-uncased (1)'
tokenizer = BertTokenizer.from_pretrained(path + bert_file)
model = BertForNextSentencePrediction.from_pretrained(path + bert_file)

def get_result(result):
    global Listao
    Listao.append(result)

def comparar(caminho, filtro):
    with open(caminho, 'r', encoding = 'utf-8-sig') as file:
       data = file.read().lower()
       data = data.split('\n')
       data = [x for x in data if x] 
       FrasesComp = []
       Listao= []
       combinations = itertools.combinations(data, 2)
    for a, b in combinations:
       encoded = tokenizer.encode_plus(a, text_pair=b, return_tensors='pt')
       seq_relationship_logits = model(**encoded)[0]
       probs = softmax(seq_relationship_logits, dim=1)
       dd = probs.detach().numpy()
       valor = (dd[0, 0])
       if valor < filtro:
         FrasesComp.append(b)
         FrasesComp.append(a)
    Lista = {i:FrasesComp.count(i) for i in set(FrasesComp)}
    Ranking = sorted(Lista, key=Lista.get, reverse=True)[:5]
    return Ranking
	
def animate():
   for c in itertools.cycle(['|', '/', '-', '\\']):
      if done:
          break
      sys.stdout.write('\rCarregando ' + c)
      sys.stdout.flush()
      time.sleep(0.1)
   sys.stdout.write('\rTerminado!     ')

def work(files):
    #long process here
    
    for i in files:
        pool.apply_async(comparar, args=(path + "/todos/" + i,filtro,), callback=get_result)
    pool.close()
    pool.join()
    done = True
    return done # Aqui você retorna o valor 

def digitar_cores():
    # Interação com o Usuário
    print("\nDetector de Anomalias\n\nO uso é limitado para que sobre 2 cores da máquina")
    cpus = mp.cpu_count()
    # cpusu = cpus - 2
    cpusu = cpus
    while True:
      try:
        cores = int(input("Digite o número de cores que deseja usar ou enter para default(2): ") or "2")
        if cores <= cpusu:
          break
          print("Número de cores maior do que possível")
      except Exception as e:
        print(e)
      
    numerofiles = int(input("\nCada divisão irá selecionar 5 frases suspeitas\n \
    Digite a quantidade que o arquivo será dividido para análise ou enter para default(1): ") or "1")

    print("\nO limite de filtro deve estar entre 0.1 e 0.99")
    
    while True:
      try:
        filtro = float(input("Digite o limite para a analise ou enter para default(0.8): ") or "0.8")
        if 0.99 > filtro > 0.1:
          break
          print("Número fora dos limites")
      except Exception as e:
        print(e)

    return numerofiles, cores, filtro

if __name__ == '__main__':

  # Verifica se este é um processo falso em um executável.
  # Se for, executa o código especificado pela linha de comando e sai.
  freeze_support()
  
  # Criação de pastas auxiliares
  auxiliares  = ['/ArquivosTxT/', "/alterados/", "/todos/", "/resultado_regex/", '/Resultado/']
  for titulo in auxiliares:
    if os.path.isdir(path+titulo) == True:
      pasta = path+titulo
      arquivos_pasta = os.listdir(pasta)
      for file in arquivos_pasta:
         if file.endswith('.txt'):
           os.remove(path+titulo+file)
    else:
      os.mkdir(path+titulo)

  # Captura e lê os arquivos a serem processados
  for file in os.listdir(path + "/analise"):
     if file.endswith(".txt"):
         with open(path + "/analise/" + file,encoding = "utf-8-sig") as fn:
           content = fn.readlines()  

  # Expressões de arquivos de WhatsApp que devem ser ignoradas
  ban = open(path + '/ban.txt', mode = 'r', encoding='utf-8')
  databans = ban.readlines()
  ban.close()

  # Limpando dados irrelevantes do arquivo (para arquivos de whatsapp)
  limpar(content, path, databans)

  # Abrindo o arquivo limpo (saida do limpar)
  limpo = open(path + '/alterados/opa.txt', 'r', encoding = 'utf=8')
  content2 = limpo.readlines()
  limpo.close()

  # Divide as sentenças, retira palavras indesejadas/risadas e linhas em branco
  datacleaning(content2, path)

  # Inicio da contagem de tempo
  start_time = time.time()

  # Valores definidos pelo usuário
  cores, numerofiles, filtro = digitar_cores()
  
  # Lê todos os arquivos limpos junta em apenas um arquivo
  read_files = glob.glob(path + "/ArquivosTxT/*.txt")
  with open(path + "/resultado_regex/result.txt", "wb") as outfile:
    for f in read_files:
      with open(f, "rb") as infile:
        outfile.write(infile.read())
  list = os.listdir(path + '/ArquivosTxT/')

  # Conta as linhas do arquivo criado
  file = open(path + "/resultado_regex/result.txt","r",encoding = "utf-8-sig")
  Counter = 0 
  Content = file.read() 
  CoList = Content.split("\n") 
  for i in CoList:
    if i:
      Counter += 1

  lines_per_file = round(Counter/numerofiles)
  smallfile = None

  #Etapa de codificação dos dados em bytes
  completed_lines_hash = set()
    
  out = open(path + '/resultado_regex/out.txt','w', encoding = 'utf-8-sig')
  for line in open(path + "/resultado_regex/result.txt","r",encoding = "utf-8-sig"):
    hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
    if hashValue not in completed_lines_hash:
      out.write(line)
      completed_lines_hash.add(hashValue)
  out.close()

  # Divide o arquivo maior na quantidade de arquivos definidos pelo usuário
  with open(path + '/resultado_regex/out.txt',encoding = "utf-8-sig") as bigfile:
    for lineno, line in enumerate(bigfile):
      if lineno % lines_per_file == 0:
        if smallfile:
          smallfile.close()
        small_filename = path + '/todos/{}.txt'.format(lineno + lines_per_file)
        smallfile = open(small_filename, "w",encoding = "utf-8-sig")
      smallfile.write(line)
    if smallfile:
      smallfile.close()
  file.close()

  # Captura o tempo de saída e contabiliza os cores usados no multiprocessamento
  results = []
  ts = time.time()
  pool = mp.Pool(cores)

  # Lista os arquivos criados
  filelist = os.listdir(path + "/todos/")
  done = False
  Listao = []

  # Mostra a animação de carregando na tela e inicia o multiprocessamento
  load = threading.Thread(target=animate)
  load.start() 
  worker = threading.Thread(target=work)
  done = work(filelist)  #Aqui você recebe o valor True

  # Escrevendo linhas suspeitas de cada arquivo
  suspeitas = []
  for item in Listao:
    for i in item:
      suspeitas.append(i)
  Tudo = {}
  filelist = os.listdir(path + "/analise/")
  from collections import defaultdict
  Tudo = defaultdict(lambda:[])
  for x in filelist:
    if x.endswith(".txt"):
      nome = os.path.basename(x)
      with open(path + "/analise/" + x,encoding = "utf-8-sig") as y:
        content = y.readlines()
        content = [s.replace('\n', '') for s in content]
        for num, line in enumerate(content, 1):
          line = line.lower()
          for i in suspeitas:
            if i in line:
              Tudo[nome].append(line + " --- linha " + str(num))
  finalmente = dict(Tudo)
  y.close()
  tempo = round(((time.time() - start_time)/60),2)
    
  # Criação de arquivo final com a descrição dos parâmetros
  linhas = [] 
  with open(path + '/Resultado/' + nome +' - Resultado -'+ 'C'+str(cores)+'-'+'D'+str(numerofiles)+'-'+'F'+str(filtro)+'.txt','w', encoding = "utf-8-sig") as f:
    f.write("Análise Detector de Anomalias\n")
    f.write("\nOs parâmetros utilizados foram\nNúmero de processamentos paralelos(cores):" + str(cores) + "\nDivisão do arquivo:" + str(numerofiles) + "\nFiltro:" + str(filtro))
    f.write("\n\nArquivos e as sentenças suspeitas com o número da linha\n") 
    for value, key in finalmente.items():
      a = str(value)
      f.write("\n" +a + "\n\n")
      linhas.append(key)
      for linha in linhas:
        for i in linha:
          f.write(str(i) + "\n")            
        
      f.write("\n\n--- Tempo de Execução: %s minutos ---" % tempo)
      f.close
    
  # Apagando arquivos auxiliares criados
  shutil.rmtree(path + "/todos/")
  os.remove(path + "/resultado_regex/result.txt")
  shutil.rmtree(path + "/resultado_regex/") # result do regex
  shutil.rmtree(path +'/ArquivosTxT/')
  shutil.rmtree(path + '/alterados/')

