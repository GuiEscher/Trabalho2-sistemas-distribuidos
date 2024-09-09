import time
import paho.mqtt.client as mqtt

BROKER = 'mqtt-broker'
PORT = 1883
TOPIC_SUPPLY = 'almoxarifado/reabastecimento'

def fornecedor():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        partes = 10  # Quantidade fixa para testes
        client.publish(TOPIC_SUPPLY, partes)
        print(f"Enviadas {partes} partes ao almoxarifado.")
        time.sleep(20)  # Espera para simular o intervalo entre envios

if __name__ == "__main__":
    fornecedor()
