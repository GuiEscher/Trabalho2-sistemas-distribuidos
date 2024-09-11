import paho.mqtt.client as mqtt # Biblioteca para comunicação via MQTT
import time

# Configurações do broker MQTT
BROKER = 'mqtt-broker'
PORT = 1883
FABRICA_ID = 'fabrica_1'
TOPIC_SUPPLY = f'{FABRICA_ID}/almoxarifado/reabastecimento' # topico para reabastecimento
TOPIC_REQUEST_BASE = f'{FABRICA_ID}/linha_producao'

# Dicionário que armazena o estoque de cada tipo de parte
estoque_partes = {
    'pv1': 100,
    'pv2': 100,
    'pv3': 100,
    'pv4': 100,
    'pv5': 100
}

# Função callback para tratar mensagens recebidas
def on_message(client, userdata, msg):
    global estoque_partes  # Acessa a variável global estoque_partes
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    
    # Verifica se a mensagem é de reabastecimento
    if TOPIC_SUPPLY in msg.topic:
        parte, quantidade = msg.payload.decode().split(',')
        quantidade = int(quantidade)
        estoque_partes[parte] += quantidade  # Atualiza o estoque da parte reabastecida
        print(f"Recebidas {quantidade} unidades de {parte}. Estoque atual de {parte}: {estoque_partes[parte]}")
        check_kanban()  # Verifica o status do estoque após o reabastecimento
    
    # Verifica se a mensagem é uma solicitação de partes da linha de produção
    elif TOPIC_REQUEST_BASE in msg.topic:
        parte, quantidade = msg.payload.decode().split(',')
        quantidade = int(quantidade)
        
        # Se há estoque suficiente, envia as partes solicitadas e atualiza o estoque
        if estoque_partes[parte] >= quantidade:
            estoque_partes[parte] -= quantidade
            client.publish(f"{msg.topic}/resposta", f"{quantidade} unidades de {parte}")
            print(f"Enviadas {quantidade} unidades de {parte} para {msg.topic}. Estoque atual de {parte}: {estoque_partes[parte]}")
        else:
            client.publish(f"{msg.topic}/resposta", "Estoque insuficiente")  # Informa que não há estoque suficiente
            print(f"Estoque insuficiente para atender a solicitação de {parte}.")
        
        check_kanban()  # Verifica o status do estoque após a solicitação

# Função que verifica o status do estoque e emite alertas
def check_kanban():
    for parte, quantidade in estoque_partes.items():
        # Define o status do estoque baseado na quantidade
        if quantidade > 50:
            status = "VERDE"  # Estoque saudável
        elif 20 < quantidade <= 50:
            status = "AMARELO"  # Estoque moderado, precisa de atenção
        else:
            status = "VERMELHO"  # Estoque crítico, ação necessária
            print(f"Estoque crítico de {parte}! Emitir ordem de compra.")
        
        print(f"Status do estoque de {parte}: {status}")

# Função principal que configura e inicia o cliente MQTT do almoxarifado
def almoxarifado():
    client = mqtt.Client()  # Cria um cliente MQTT
    client.on_message = on_message  # Define a função callback para tratar mensagens
    client.connect(BROKER, PORT, 60)  # Conecta ao broker MQTT
    client.subscribe(f"{FABRICA_ID}/almoxarifado/#")  # Inscreve-se nos tópicos de reabastecimento
    client.subscribe(f"{TOPIC_REQUEST_BASE}/+/solicitar_partes")  # Inscreve-se nos tópicos de solicitação de partes
    client.loop_start()  # Inicia o loop para manter a conexão MQTT ativa

    while True:
        time.sleep(1) 

if __name__ == "__main__":
    almoxarifado()  
