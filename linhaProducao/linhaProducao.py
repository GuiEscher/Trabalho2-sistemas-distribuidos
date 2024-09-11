import os
import paho.mqtt.client as mqtt
import time
import random

# Configuração das variáveis de ambiente
BROKER = os.getenv('BROKER', 'mqtt-broker')
PORT = int(os.getenv('PORT', 1883))
FABRICA_ID = os.getenv('FABRICA_ID', 'fabrica_1')
LINHA_ID = os.getenv('LINHA_ID', 'linha_1')

# Tópicos de MQTT
TOPIC_REQUEST = f'{FABRICA_ID}/linha_producao/{LINHA_ID}/solicitar_partes'
TOPIC_RESPONSE = f'{FABRICA_ID}/linha_producao/{LINHA_ID}/solicitar_partes/resposta'

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

def linha_producao():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC_RESPONSE)
    client.loop_start()

    while True:
        parte = random.choice(['pv1', 'pv2', 'pv3', 'pv4', 'pv5'])
        quantidade = random.randint(1, 20) + 20  # Quantidade variável
        client.publish(TOPIC_REQUEST, f"{parte},{quantidade}")
        print(f"Solicitado {quantidade} unidades de {parte} ao almoxarifado para {LINHA_ID}.")
        time.sleep(10)  # Espera para simular intervalo entre solicitações

if __name__ == "__main__":
    linha_producao()
