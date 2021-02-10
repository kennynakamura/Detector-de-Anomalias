# Detector de Anomalias

As investigações digitais têm enfrentado um aumento exponencial da quantidade de dados disponíveis para serem analisados em uma investigação. Esses dados são produzidos de inúmeras formas, desde de e-mails, transações bancárias, troca de mensagens instantâneas, localizações geográficas, acesso de sites, entre outras. Desta forma, é inviável que um analista investigue de maneira eficiente todos os dados coletados durante uma investigação sem o auxílio de ferramentas de análise [Nicole B et all 2005]. Essas ferramentas são softwares que buscam encontrar dados relacionados especificamente a investigação, além de significados, padrões e anormalidades sobre todo o conjunto de arquivos, esse processo é chamado de Data Mining.

O escopo deste trabalho é sobre o processo de análise dos grandes conjuntos de dados, especificamente de diálogos em texto, buscando encontrar códigos ocultos que sejam relacionados a atividades criminosas. A demanda desta aplicação se dá pelo amplo uso de codinomes com intuito de dissuadir uma investigação, e a não produção de provas que comprometam o criminoso.  Assim espera-se que o projeto desenvolvido identifique codinomes, mesmo com uma alta taxa de erro esperada dada a complexidade do problema. 

Nicole B, Jan C (2005) Dealing with Terabyte Data Sets in Digital Investigations. DigitalForensics 2005: Advances in Digital Forensics pp 3-16. 

## Como usar o programa

Os arquivos a serem analisados devem ser preparados para a análise, separando as frases por sentença em cada linha e apagando as linhas que ficarem com somente uma palavra.\
Recomenda-se que a sentença "Bom dia" e suas variações sejam retiradas.\
Estas alterações no texto original podem ser feitas usando regex.

Exemplo  
**Original**:     
Levei o carro para o mecânico hoje, ontem estava ocupado.  

**Alteradas**\
Levei o carro para o mecânico hoje\
ontem eu estava ocupado
              
**Cria-se 3 pastas: ArquivoTxT, result, todos. Todas elas devem ficar em uma mesma pasta principal com o arquivo RUN.py**

**ArquivoTxT**\
Onde os arquivos txt a serem analisados devem ser colocados, somente nesse que o usuário deve interagir\
**result**\
Onde o arquivo único com todos os textos juntos será criado automaticamente\
**todos**\
Arquivos separados com o mesmo número de linhas será criado automaticamente

Na mesma pasta principal deve-se ter uma pasta chamada **"bert-base-multilingual-uncased"** 
Dentro desta pasta deve haver 3 arquivos: vocab.txt, config.json e pytorch_model que podem ser baixados o seuinte link:  
https://huggingface.co/bert-base-multilingual-uncased/tree/main \
ou podem ser baixados pelo drive\
https://drive.google.com/drive/folders/10L_3YAtaHT0AC0XGoXPj-UGoNErgtnu3?usp=sharing \
Estes são arquivos que auxiliaram a análise do texto.

Neste script foram usados as bibliotecas Torch e Transformers, sendo necessário instalar (pip install).

Em seguida, execute o script RUN.py 

#### Ao final da análise, será criado um arquivo txt na pasta principal com as sentenças selecionadas e em qual linhas elas se encontram no arquivo de origem. Vale ressaltar que sentenças podem ser repetidas ao longo dos textos de origem, desta forma, todas as linhas que possuirem alguma das sentenças selecionadas durante a analise serão descritas.

![alt text](https://github.com/kennynakamura/Detector-de-Anomalias/blob/main/fluxograma.png?raw=true)
