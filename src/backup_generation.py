import os
import subprocess
from datetime import datetime
import logging
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
env_path = os.path.join(os.path.dirname(__file__), '..', 'credentials', '.env')
load_dotenv(env_path)

# Configuração de logging
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'backup_log.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Função para logar e printar simultaneamente
def log(message, level=logging.INFO):
    print(message)
    logging.log(level, message)

# Função para excluir arquivo em caso de erro
def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            log(f"Arquivo {file_path} excluído com sucesso.", level=logging.INFO)
    except Exception as e:
        log(f"Erro ao excluir o arquivo {file_path}: {e}", level=logging.ERROR)

# Obtém a data atual e formata para o formato desejado (YYYY-MM-DD)
formatted_date = datetime.now().strftime('%Y-%m-%d')

# Definindo o diretório de backup
backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
os.makedirs(backup_dir, exist_ok=True)

# Função para fazer o backup do banco de dados PostgreSQL
def backup_postgres(database, user, password, host, port, output_file):
    command = f'PGPASSWORD={password} pg_dump -h {host} -p {port} -U {user} {database} > "{output_file}"'
    try:
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        log(f"Backup do PostgreSQL para {database} concluído com sucesso.")
    except subprocess.CalledProcessError as e:
        log(f"Falha no backup do PostgreSQL para {database}: {e}", level=logging.ERROR)
        delete_file(output_file)

# Função para fazer o backup do MongoDB
def backup_mongodb(connection_string, output_file):
    command = f'mongodump --uri="{connection_string}" --out="{output_file}"'
    try:
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        log("Backup do MongoDB concluído com sucesso.")
    except subprocess.CalledProcessError as e:
        log(f"Falha no backup do MongoDB: {e}", level=logging.ERROR)
        delete_file(output_file)

# Lista de bancos PostgreSQL (lidos do .env)
postgres_dbs = os.getenv("POSTGRES_DATABASES", "").split(",")

# Criar backups PostgreSQL
for db in postgres_dbs:
    db = db.strip()
    if db:
        output_file = os.path.join(backup_dir, f'backup_{db}_{formatted_date}.sql')
        backup_postgres(
            database=db,
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            output_file=output_file
        )

# Criar backup do MongoDB
mongodb_connection_string = os.getenv("MONGODB_URI")
if mongodb_connection_string:
    mongodb_backup = os.path.join(backup_dir, f'backup_mongodb_{formatted_date}')
    backup_mongodb(mongodb_connection_string, mongodb_backup)
