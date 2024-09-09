import paho.mqtt.client as mqtt
import time

BROKER = 'mqtt-broker'
PORT = 1883
TOPIC_REQUEST = 'linha_producao/solicitar_partes'

def linha_producao():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    while True:
        client.publish(TOPIC_REQUEST, "10")
        print("Solicitado 10 partes ao almoxarifado.")
        time.sleep(15)  # Espera para simular intervalo entre solicitações

if __name__ == "__main__":
    linha_producao()
