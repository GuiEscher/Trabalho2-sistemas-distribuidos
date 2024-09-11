import paho.mqtt.client as mqtt
import time

BROKER = 'mqtt-broker'
PORT = 1883
FABRICA_ID = 'fabrica_1'
TOPIC_SUPPLY = f'{FABRICA_ID}/almoxarifado/reabastecimento'
TOPIC_REQUEST_BASE = f'{FABRICA_ID}/linha_producao'

estoque_partes = {
    'pv1': 100,
    'pv2': 100,
    'pv3': 100,
    'pv4': 100,
    'pv5': 100
}

def on_message(client, userdata, msg):
    global estoque_partes
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    if TOPIC_SUPPLY in msg.topic:
        parte, quantidade = msg.payload.decode().split(',')
        quantidade = int(quantidade)
        estoque_partes[parte] += quantidade
        print(f"Recebidas {quantidade} unidades de {parte}. Estoque atual de {parte}: {estoque_partes[parte]}")
        check_kanban()
    elif TOPIC_REQUEST_BASE in msg.topic:
        parte, quantidade = msg.payload.decode().split(',')
        quantidade = int(quantidade)
        if estoque_partes[parte] >= quantidade:
            estoque_partes[parte] -= quantidade
            client.publish(f"{msg.topic}/resposta", f"{quantidade} unidades de {parte}")
            print(f"Enviadas {quantidade} unidades de {parte} para {msg.topic}. Estoque atual de {parte}: {estoque_partes[parte]}")
        else:
            client.publish(f"{msg.topic}/resposta", "Estoque insuficiente")
            print(f"Estoque insuficiente para atender a solicitação de {parte}.")
        check_kanban()

def check_kanban():
    for parte, quantidade in estoque_partes.items():
        if quantidade > 50:
            status = "VERDE"
        elif 20 < quantidade <= 50:
            status = "AMARELO"
        else:
            status = "VERMELHO"
            print(f"Estoque crítico de {parte}! Emitir ordem de compra.")
        print(f"Status do estoque de {parte}: {status}")

def almoxarifado():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(f"{FABRICA_ID}/almoxarifado/#")
    client.subscribe(f"{TOPIC_REQUEST_BASE}/+/solicitar_partes")
    client.loop_start()

    while True:
        time.sleep(1)  # Manter o loop ativo para receber mensagens

if __name__ == "__main__":
    almoxarifado()
