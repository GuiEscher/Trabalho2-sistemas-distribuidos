# Usando uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o script Python para dentro do container
COPY almoxarifado.py /app

# Instala as dependências necessárias
RUN pip install paho-mqtt

# Comando para executar o script
CMD ["python", "almoxarifado.py"]
