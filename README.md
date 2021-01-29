# Detector-de-Anomalias

Cria-se 3 pastas: ArquivoTxT, result, todos   

ArquivoTxT    - Onde os arquivos txt a serem analisados devem ser colocados  
result - Onde o arquivo único com todos os textos juntos  
todos  - Arquivos separados com o mesmo número de linhas.    

Os modelos pré-treinados podem ser baixados no HugginsFaces, procurar pelo bert-base-multilingual-uncased.  

Dentro dos modelos deve haver 3 arquivos: vocab.txt, config.json e pytorch_model.  
Link para o bert multilingual uncased: https://huggingface.co/bert-base-multilingual-uncased/tree/main 

Neste script foi usado os modelos do Torch, do PyTorch. Por isso é necessário instalar as bibliotecas Torch e Transformers (pip install)

![alt text](https://github.com/kennynakamura/Detector-de-Anomalias/blob/main/fluxograma.png?raw=true)
