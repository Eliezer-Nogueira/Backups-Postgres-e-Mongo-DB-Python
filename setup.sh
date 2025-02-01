#!/bin/bash

# Atualiza os repositórios
apt-get update

# Instala o cliente do PostgreSQL, que inclui o pg_dump
apt-get install -y postgresql-client

# Instala o mongodump (MongoDB Database Tools)
apt-get install -y mongodb-database-tools

# Instala as dependências do Python
pip install -r requirements.txt

# Exibe a mensagem de conclusão
echo "Instalação concluída. Dependências do PostgreSQL (pg_dump) e MongoDB (mongodump) estão instaladas."
