# FOLDER_COPIER
Este script realiza o processamento e varredura de arquivos XML associados a uma lista de CNPJs extraída de um arquivo Excel. 

## ARQUIVO CONFIG.YAML
O arquivo config desse script cordena os caminhos de processamento, são eles:
- path_cnpj_list: "C:/cnpjs/cnpjs.xlsx" (Caminho para o arquivo excel que contém a lista de CNPJ's).
- path_files: "C:/files" (Pasta que será varrida).
- path_pasta_destino: "C:/pasta_destino" (Pasta para destino dos arquivos encontrados).
- path_arquivo_log: "C:/logs/script.log" (Arquivo de log para acompanhamento do processamento).

## OBERSERVAÇÕES GERAIS DO PROJETO
- Esse projeto contribui para ocasiões na qual precisamos varrer diversos arquivos XML em diferentes locais.

## CRIAÇÃO DO AMBIENTE VIRTUAL
python -m venv venv

## ATIVAÇÃO DO AMBIENTE VIRTUAL
venv\Scripts\activate

## BAIXAR LIBS 
pip install -r requirements.txt

