import time
import paho.mqtt.client as mqtt # Biblioteca para comunicação via MQTT

# Configurações do broker MQTT
BROKER = 'mqtt-broker'
PORT = 1883
FABRICA_ID = 'fabrica_1'
TOPIC_SUPPLY = f'{FABRICA_ID}/almoxarifado/reabastecimento'

# Função principal que simula o fornecedor
def fornecedor():
    client = mqtt.Client()  # Cria um cliente MQTT
    client.connect(BROKER, PORT, 60)  # Conecta ao broker MQTT

    while True:
        # Simula o envio de diferentes tipos de partes ao almoxarifado
        for parte in ['pv1', 'pv2', 'pv3', 'pv4', 'pv5']:
            quantidade = 10  # Quantidade fixa para reabastecimento
            client.publish(TOPIC_SUPPLY, f"{parte},{quantidade}")  # Publica a mensagem de reabastecimento
            print(f"Enviadas {quantidade} unidades de {parte} ao almoxarifado.")
            time.sleep(2)  # Espera para simular o intervalo entre os envios

if __name__ == "__main__":
    fornecedor()  # Executa a função principal 
