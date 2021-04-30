import re
import sys
import time

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def limpar(data, Path, databans):
    novo = []
    for line in data:
       line = line.lower()
       line = re.sub('^(.*: )',"", line)
       line = re.sub('.*(:.. - ).*\r?\n', "",line)
       line = re.sub(r'https?:\/\/.*[\r\n]*', '', line, flags=re.MULTILINE)
       if not any(databan in line for databan in databans):
           novo.append(line)

    novo2 = []
    for item in novo:
       div = item.split()
       for i in div:
          cont = i.count('k') + i.count('ha') + i.count('hsu') + i.count('rs')
          if cont >= 2:
             div.remove(i)
       dd = ' '.join(map(str, div))
       novo2.append(dd)

    novo3 = []
    for item in novo2:
        jj = deEmojify(item)
        novo3.append(jj)

    out = open(Path + '/alterados/opa.txt','w', encoding = 'utf-8-sig')     
    for item in novo3:
        out.write(item + '\n')
    return
       
def datacleaning(content2, path):
  pattern = [',','.','!','?','that ','que ']
  f = open(path+'/alterados/novo.txt', 'w', encoding='utf-8')
  for line in content2:
    line = line.lower()
    for word in line:
      for character in word:
        for i in pattern:
          if character  in pattern:
            character = re.sub(i, '\n', character)
      f.write(character)
  f.close()
  
  t = open(path + "/alterados/novo2.txt", "w", encoding = "utf-8")
  p = open(path + "/alterados/novo.txt", "r+", encoding = "utf-8")
  ff = p.readlines()
  for line in ff:
    if line[0] != " ":
      t.write(line)
    else:
      t.write(line[1:])
  t.close()
  p.close()
  
  gg = open(path + "/alterados/novo2.txt", "r", encoding = "utf-8")
  f = open(path + "/alterados/novo3.txt", "w", encoding = "utf-8")
  hh = gg.readlines()
  ignore = ['bom dia', 'boa noite', 'legal',  'boa tarde', 'tudo bem','ok', 'oi ']
  for line in hh:
    if " " in line and not any(item in line for item in ignore):
      f.write(line)
  f.close()
  gg.close()
  
  kk = open(path + "/alterados/novo3.txt", encoding = "utf-8")
  ll = open(path + "/alterados/novo4.txt", "w", encoding = "utf-8")
  pp = kk.readlines()
  for line in pp:
     line = line.rstrip()
     if " " in line:
        ll.write(line+ '\n')
  ll.close()
  kk.close()
  
  lines = [i for i in open(path + "/alterados/novo4.txt", encoding = "utf-8") if i[:-1]]
  final = open(path + "/ArquivosTxT/final.txt", 'w', encoding = "utf-8")
  pattern2 = [',','.',':','"',':',')','(','*','“','”']
  for line in lines:
    line = line.lower()
    for word in line:
      for character in word:
        for i in pattern2:
          if character in pattern2:
            character = re.sub(i,"", character)
      final.write(character)
  final.close()
