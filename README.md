# Detector de Anomalias

As investigações digitais têm enfrentado um aumento exponencial da quantidade de dados disponíveis para serem analisados em uma investigação. Esses dados são produzidos de inúmeras formas, desde de e-mails, transações bancárias, troca de mensagens instantâneas, localizações geográficas, acesso de sites, entre outras. Desta forma, é inviável que um analista investigue de maneira eficiente todos os dados coletados durante uma investigação sem o auxílio de ferramentas de análise [Nicole B et all 2005]. Essas ferramentas são softwares que buscam encontrar dados relacionados especificamente a investigação, além de significados, padrões e anormalidades sobre todo o conjunto de arquivos, esse processo é chamado de Data Mining.

O escopo deste trabalho é sobre o processo de análise dos grandes conjuntos de dados, especificamente de diálogos em texto, buscando encontrar códigos ocultos que sejam relacionados a atividades criminosas. A demanda desta aplicação se dá pelo amplo uso de codinomes com intuito de dissuadir uma investigação, e a não produção de provas que comprometam o criminoso.  Assim espera-se que o projeto desenvolvido identifique codinomes, mesmo com uma alta taxa de erro esperada dada a complexidade do problema.  

O algoritmo funciona com as seguintes etapas:
- Extração dos dados no dispositivos.
- Processamento dos dados, organizando de maneira que a ferramenta posso ler os arquivos.
- Seleção dos dados suspeitos.
- Agrupamento dos dados selecionados e criado o arquivo para a visualização.
- Análise pelo investigador a procura de informações relevantes.

![alt text](https://github.com/kennynakamura/Detector-de-Anomalias/blob/main/Apresentação1.png?raw=true)

Nicole B, Jan C (2005) Dealing with Terabyte Data Sets in Digital Investigations. DigitalForensics 2005: Advances in Digital Forensics pp 3-16. 

## Como funciona o programa

A seleção realizada durante a análise tem como o princípio ponderar a possibilidade de uma frase ser consequente de outra. Essa possibilidade é inferida com um valor entre 0 e 1.\
Desta forma, para que uma frase seja selecionada, é determinado um valor mínimo em que a comparação deve resultar, assim, as frases que mais vezes forem selecionadas serão destacadas.\

Exemplo de sentenças  
**Original**:     
Frase: Levei o carro para o mecânico hoje, ontem estava ocupado.  

**Alteradas**\
Sentença 1: Levei o carro para o mecânico hoje\
Sentença 2: ontem eu estava ocupado

Para essa seleção é utilizada o modelo pré-treinado de NLP, BERT, na funcionalidade Next Sentence Prediction. Foi escolhido este modelo pelo seu treinamento ter ocorrido levando em consideração o contexto das palavras, uma característica essencial nesta tarefa.\
BERT é um modelo de Machine Learning pré-treinado que pode ser treinado novamente para uma tarefa específica, Fine Tunning, mas para a esta tarefa não foi realizado nenhum treinamento adicional, utilizando o model pré-treinado.\

Na mesma pasta principal deve-se ter uma pasta chamada **"bert-base-multilingual-uncased"** 
Dentro desta pasta deve haver 3 arquivos: vocab.txt, config.json e pytorch_model que podem ser baixados o seuinte link:  
https://huggingface.co/bert-base-multilingual-uncased/tree/main \
ou podem ser baixados pelo drive\
https://drive.google.com/drive/folders/10L_3YAtaHT0AC0XGoXPj-UGoNErgtnu3?usp=sharing \
Estes são arquivos que auxiliaram a análise do texto.

Neste script foram usados as bibliotecas Torch e Transformers, sendo necessário instalar (pip install).

#### Ao final da análise, será criado um arquivo txt na pasta principal com as sentenças selecionadas e em qual linhas elas se encontram no arquivo de origem. Vale ressaltar que sentenças podem ser repetidas ao longo dos textos de origem, desta forma, todas as linhas que possuirem alguma das sentenças selecionadas durante a analise serão descritas.

![alt text](https://github.com/kennynakamura/Detector-de-Anomalias/blob/main/fluxograma2.0.jpg?raw=true)
