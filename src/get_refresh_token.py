from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

# Definir o caminho do arquivo de credenciais na pasta 'credentials'
CLIENT_SECRET_FILE = os.path.join('credentials', 'client_secret_387147842037-vhj9u42el7op4rem3ocjo5k260gr3qk2.apps.googleusercontent.com.json')

# Definir os escopos de acesso
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_tokens():
    # Criar o fluxo de autenticação com o arquivo de credenciais especificado
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    
    # Executar o servidor local para obter as credenciais
    creds = flow.run_local_server(port=0)
    
    # Criar um dicionário para armazenar os tokens de acesso
    tokens = {
        "refresh_token": creds.refresh_token,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret
    }

    # Salvar os tokens em um arquivo 'tokens.json'
    with open("tokens.json", "w") as token_file:
        json.dump(tokens, token_file, indent=4)
    
    print("Refresh Token salvo com sucesso!")

# Chamar a função para obter e salvar os tokens
get_tokens()
