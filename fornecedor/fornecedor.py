import time
import paho.mqtt.client as mqtt

BROKER = 'mqtt-broker'
PORT = 1883
FABRICA_ID = 'fabrica_1'
TOPIC_SUPPLY = f'{FABRICA_ID}/almoxarifado/reabastecimento'

def fornecedor():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        for parte in ['pv1', 'pv2', 'pv3', 'pv4', 'pv5']:
            quantidade = 10  # Quantidade fixa para testes
            client.publish(TOPIC_SUPPLY, f"{parte},{quantidade}")
            print(f"Enviadas {quantidade} unidades de {parte} ao almoxarifado.")
            time.sleep(2)  # Espera para simular o intervalo entre envios

if __name__ == "__main__":
    fornecedor()
