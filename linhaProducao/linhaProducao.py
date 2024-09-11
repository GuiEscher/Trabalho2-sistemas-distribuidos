import os
import paho.mqtt.client as mqtt # Biblioteca para comunicação via MQTT
import time
import random

# Configuração das variáveis de ambiente
BROKER = os.getenv('BROKER', 'mqtt-broker')  # Broker MQTT
PORT = int(os.getenv('PORT', 1883))  # Porta do broker MQTT
FABRICA_ID = os.getenv('FABRICA_ID', 'fabrica_1')  # Identificador da fábrica
LINHA_ID = os.getenv('LINHA_ID', 'linha_1')  # Identificador da linha de produção

# Tópicos de MQTT para comunicação com o almoxarifado
TOPIC_REQUEST = f'{FABRICA_ID}/linha_producao/{LINHA_ID}/solicitar_partes'
TOPIC_RESPONSE = f'{FABRICA_ID}/linha_producao/{LINHA_ID}/solicitar_partes/resposta'

# Função callback para tratar mensagens recebidas
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")  # Exibe a resposta do almoxarifado

# Função principal que simula a linha de produção
def linha_producao():
    client = mqtt.Client()  # Cria um cliente MQTT
    client.on_message = on_message  # Define a função callback para tratar mensagens
    client.connect(BROKER, PORT, 60)  # Conecta ao broker MQTT
    client.subscribe(TOPIC_RESPONSE)  # Inscreve-se no tópico para receber respostas do almoxarifado
    client.loop_start()  # Inicia o loop para manter a conexão MQTT ativa

    while True:
        # Simula a solicitação de diferentes partes ao almoxarifado
        parte = random.choice(['pv1', 'pv2', 'pv3', 'pv4', 'pv5'])
        quantidade = random.randint(1, 20) + 20  # Quantidade variável para a solicitação
        client.publish(TOPIC_REQUEST, f"{parte},{quantidade}")  # Envia a solicitação ao almoxarifado
        print(f"Solicitado {quantidade} unidades de {parte} ao almoxarifado para {LINHA_ID}.")
        time.sleep(10)  # Espera para simular o intervalo entre solicitações

if __name__ == "__main__":
    linha_producao()  # Executa a função principal 
