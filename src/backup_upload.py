import os
import shutil
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

# Definir diretórios base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials", "tokens.json")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Google Drive Config
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_ID = "1OaJ7Ro9kcgsY6qghccQF6Mj8z5Xg22Qc"  # ID da pasta no Google Drive

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Função para criar o serviço do Google Drive
def create_drive_service():
    if not os.path.exists(CREDENTIALS_FILE):
        logging.error(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
        return None

    with open(CREDENTIALS_FILE, "r") as token_file:
        tokens = json.load(token_file)

    creds = Credentials.from_authorized_user_info(info=tokens, scopes=SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("drive", "v3", credentials=creds)

# Função para compactar diretórios
def compress_directory(directory_path):
    zip_file = f"{directory_path}.zip"
    shutil.make_archive(directory_path, "zip", directory_path)
    return zip_file

# Função para verificar a existência de um arquivo
def verify_file_exists(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Arquivo não encontrado: {file_path}")
        return False
    return True

# Função para upload do arquivo para o Google Drive
def upload_file_to_drive(service, file_path, folder_id):
    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
    media = MediaFileUpload(file_path, mimetype="application/octet-stream", resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        logging.info(f"Arquivo {file_path} enviado para {folder_id} com ID: {file.get('id')}")
        return True
    except Exception as e:
        logging.error(f"Erro ao fazer upload de {file_path}: {e}")
        return False

# Criar o serviço do Google Drive
drive_service = create_drive_service()

if drive_service and os.path.exists(BACKUP_DIR):
    for backup_file in os.listdir(BACKUP_DIR):
        full_path = os.path.join(BACKUP_DIR, backup_file)

        if os.path.isdir(full_path):
            logging.info(f"Compactando diretório: {full_path}")
            zip_file = compress_directory(full_path)

            if verify_file_exists(zip_file) and upload_file_to_drive(drive_service, zip_file, FOLDER_ID):
                os.remove(zip_file)
                shutil.rmtree(full_path)  # Exclui o diretório após o upload
            else:
                logging.error(f"Erro ao processar o diretório: {full_path}")

        elif os.path.isfile(full_path) and upload_file_to_drive(drive_service, full_path, FOLDER_ID):
            os.remove(full_path)  # Remove após o upload
else:
    logging.error("Erro: Serviço do Google Drive não foi inicializado ou diretório de backups não existe.")
