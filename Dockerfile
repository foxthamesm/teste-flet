
# Use imagem oficial Python como base
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos requirements.txt e o código para dentro do container
COPY requirements.txt ./
COPY . .

# Atualiza pip e instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta padrão usada pelo Flet
EXPOSE 8080

# Comando para rodar sua aplicação
#>>>>>>> a78a355c162360b1ffa951b245841d0dbb05e1db
CMD ["python", "main.py"]
