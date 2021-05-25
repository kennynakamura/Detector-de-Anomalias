import spacy
import re, os, itertools
from java.lang import System
from collections import OrderedDict

configFile  = 'AnomalyDetectorConfig.txt'
filtroProp  = 'filtro_det'

class AnomalyDetectorTask:
    
    enabled = False
    configDir = None
    
    def isEnabled(self):
        return True
        
    def init(self, confProps, configFolder):   
        
        model = caseData.getCaseObject('spacy_model')
        file = System.getProperty('iped.root') + '/models/modeloSpacyLG/pt_core_news_lg/pt_core_news_lg-3.0.0'
        global pln
        pln = spacy.load(file)
        
        from java.io import File
        from dpf.sp.gpinf.indexer.util import UTF8Properties
        extraProps = UTF8Properties()
        extraProps.load(File(configFolder, configFile))
        filtro_det = extraProps.getProperty(filtroProp)      
        global filtro 
        if filtro_det is not None:
           filtro  = float(filtro_det) 
           
        return
    
    def finish(self):      
        return 
        
    def process(self, item):

        categories = item.getCategorySet().toString()
        if not ("Chats" in categories or "Emails" in categories):
           return 

        def Convert(string):
           li = list(string.split("\n"))
           return li
        
        texto = str(item.getParsedTextCache())
        
        #Separa o texto em linhas dentro de uma list
        # ['oi, camila', 'tudo bem?', 'tchau', ...] 
        lista = Convert(texto)
        
        def datacleannig(lista):
           #Data Cleanning das linhas dentro da lista
           FrasesSeparadas = []
           for item in lista:
              item = re.split('[,.!?]', str(item).lower())
              FrasesSeparadas.append(item)
           FrasesSeparadas = ([j for i in FrasesSeparadas for j in i])
           unwanted = {'',' ', 'bom dia', 'boa tarde', 'boa noite'}
           FrasesSeparadas = [x for x in FrasesSeparadas if x not in unwanted]
           FrasesSeparadas = [x for x in FrasesSeparadas if ' ' in x]
           FrasesSeparadas = [s.strip() for s in FrasesSeparadas]
           FrasesSeparadas = [x for x in FrasesSeparadas if any(y in x for y in ' ')]      
           return FrasesSeparadas
        
        FrasesSeparadas = datacleanning(lista)
        
        #Função para dividir o texto em partes iguais
        def chunks(l, n):
            n = max(1, n)
            return (l[i:i+n] for i in range(0, len(l), n))

        #Conta o número de linhas depois do Data Cleanning
        Counter = 0 
        for i in FrasesSeparadas:
          if i:
             Counter += 1
        lines_per_file = round(Counter/(Counter*0.05))
       
        #Dividi a lista em tamanho iguais
        Partes = (list(chunks(FrasesSeparadas,lines_per_file)))
        
        #Função para comparar as linhas.
        def comparar(data, filtro):
            selecao = 1
            FrasesComp = []
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
        
        #Função para executar a função de comparação em todas as partes divididas
        def compararTudo(filelist):
            for item in filelist:
                resultado = comparar(item, filtro)
                Listao.append(resultado)
            return
        
        #Comparando todas as linhas de todas as partes
        # Listao é a lista onde será armazenado as linhas selecionadas de cada parte
        # [ [linha suspeita da parte 1], [linha suspeita da parte 2], [linha suspeita da parte 3]]
        # [[L],[L],[L]]
        Listao = []
        compararTudo(Partes)
        
        #Suspeitas é a lista final com todas as linhas suspeitas
        # [ linha suspeita da parte 1, linha suspeita da parte 2, linha suspeita da parte 3]
        # [ L, L, L ] 
        def separando(Listao):
           suspeitas = []
           for item in Listao:
              for i in item:
                 suspeitas.append(i)
        
        suspeitas = separando(Listao)
        
        item.setExtraAttribute('possiblyAnomaly', suspeitas)
            
