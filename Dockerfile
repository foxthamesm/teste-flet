# Usa imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para dentro do contêiner
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flet (será substituída pela variável de ambiente PORT no Cloud Run)
EXPOSE 8080

# Define a variável de ambiente PORT para o Flet usar
ENV PORT 8080

# Comando para rodar o app
CMD ["python", "main.py"]
