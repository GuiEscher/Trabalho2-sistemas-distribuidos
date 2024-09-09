import paho.mqtt.client as mqtt
import time

BROKER = 'mqtt-broker'
PORT = 1883
TOPIC_SUPPLY = 'almoxarifado/reabastecimento'
TOPIC_REQUEST = 'linha_producao/solicitar_partes'
estoque_partes = 100

def on_message(client, userdata, msg):
    global estoque_partes
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    if msg.topic == TOPIC_SUPPLY:
        partes = int(msg.payload.decode())
        estoque_partes += partes
        print(f"Recebidas {partes} partes. Estoque atual: {estoque_partes}")
        check_kanban()

def check_kanban():
    global estoque_partes
    if estoque_partes > 50:
        status = "VERDE"
    elif 20 < estoque_partes <= 50:
        status = "AMARELO"
    else:
        status = "VERMELHO"
        print("Estoque crítico! Emitir ordem de compra.")
    print(f"Status do estoque: {status}")

def almoxarifado():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC_SUPPLY)
    client.loop_start()
    
    while True:
        partes_solicitadas = 10  # Quantidade fixa para testes
        global estoque_partes
        if estoque_partes >= partes_solicitadas:
            estoque_partes -= partes_solicitadas
            print(f"Enviadas {partes_solicitadas} partes para linha de produção.")
        else:
            print("Estoque insuficiente para atender a solicitação.")
        check_kanban()
        time.sleep(10)  # Espera para simular intervalo entre solicitações

if __name__ == "__main__":
    almoxarifado()
