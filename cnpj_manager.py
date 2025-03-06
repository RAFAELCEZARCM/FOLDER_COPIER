import os
import shutil
import sqlite3
import pandas as pd
import yaml
import logging
from datetime import datetime

# Carregar configuração do arquivo YAML
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Definição de variáveis de configuração
EXCEL_FILE = config["path_cnpj_list"]
SOURCE_DIR = config["path_files"]
DESTINATION_DIR = config["path_pasta_destino"]
LOG_FILE = config["path_arquivo_log"]
DB_FILE = "database.db"

# Configuração do log
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Criar banco de dados SQLite para registrar os arquivos XML já processados
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT UNIQUE,
        timestamp TEXT
    )
""")
conn.commit()

def read_cnpjs_from_excel():
    """Lê os CNPJs do arquivo Excel."""
    df = pd.read_excel(EXCEL_FILE, dtype=str)
    return df.iloc[:, 0].tolist()

def check_if_file_processed(file_name):
    """Verifica se um arquivo XML já foi processado no banco de dados."""
    cursor.execute("SELECT 1 FROM processed_files WHERE file_name = ?", (file_name,))
    return cursor.fetchone() is not None

def mark_file_as_processed(file_name):
    """Marca um arquivo XML como processado no banco de dados."""
    cursor.execute("INSERT INTO processed_files (file_name, timestamp) VALUES (?, ?)", (file_name, datetime.now()))
    conn.commit()

def process_cnpj_files(cnpj):
    """Processa os arquivos XML do CNPJ."""
    source_path = os.path.join(SOURCE_DIR, cnpj)
    dest_path = os.path.join(DESTINATION_DIR, cnpj)

    if not os.path.exists(source_path):
        logging.warning(f"Pasta {cnpj} não encontrada.")
        print(f"[❌] Pasta {cnpj} não encontrada. Verifique se o CNPJ consta no arquivo excel.")
        return

    arquivos_processados = 0
    for root, _, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith(".xml"):
                file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_path, os.path.relpath(file_path, source_path))

                if check_if_file_processed(file):
                    logging.info(f"Arquivo {file} ja processado. Pulando...")
                    print(f"[>>] Arquivo {file} já foi processado. Pulando...")
                    continue
                
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy2(file_path, dest_file_path)

                mark_file_as_processed(file)
                arquivos_processados += 1
                logging.info(f"Arquivo {file} copiado para {dest_file_path}")
                print(f"[✔] Arquivo {file} copiado.")

    if arquivos_processados == 0:
        print(f"[⚠] Nenhum novo arquivo XML encontrado para {cnpj}.")
    else:
        print(f"[✅] {arquivos_processados} arquivos XML processados para {cnpj}.")

def main():
    """Executa o script de processamento dos CNPJs."""
    print("\n[🔄] Processando... Aguarde!\n")
    cnpjs = read_cnpjs_from_excel()
    total = len(cnpjs)

    print(f"\n[🔍] Processando {total} CNPJs...\n")

    for cnpj in cnpjs:
        cnpj = str(cnpj).strip()
        process_cnpj_files(cnpj)

    print(f"\n[✅] Processamento finalizado.\n")
    logging.info(f"Processamento finalizado.")

if __name__ == "__main__":
    main()
