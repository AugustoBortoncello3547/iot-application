import paho.mqtt.publish as publish
import json
from decouple import config

def getDevice(deviceOption):
    devices = {
        "1": "temperatura",
        "2": "umidade",
        "3": "vibracao",
        "4": "luminosidade"
    }
    
    return devices[deviceOption]

def sendDataToTago(data, option):

    device = getDevice(option)

    broker = "mqtt.tago.io"
    port = 1883
    topic = "tago/data/post"

    data = [{
        "variable": device,
        "value": data,
        "metadata": {
                "mqtt_topic": device
            }
    }]

    usernameDevice = config(device.upper())
    passwordDevice = config(device.upper() + "-TOKEN")

    print(device, usernameDevice, passwordDevice)

    publish.single(topic, json.dumps(data), qos=1, retain=False, hostname=broker,
               port=port, client_id='', keepalive=60, auth={'username': str(usernameDevice) , 'password': str(passwordDevice) })
    
    print("Informação enviada com sucesso :) ")

def celsius_para_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def calcular_umidade_relativa(umidade_absoluta):
    # Vamos supor que a umidade máxima seja 25 g/m3
    return  (umidade_absoluta / 25) * 100

def hz_para_rpm(hz):
    return hz * 60

def converter_lumens_para_lux(lumens):
    area = 100; # Área de 100 m2
    iluminancia = lumens / area
    return iluminancia

def numeroEhValido(input_text):
    try:
        numero = float(input_text)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    while True:
        print("Escolha uma opção:")
        print("1. Registrar temperatura")
        print("2. Registrar umidade")
        print("3. Registrar vibração")
        print("4. Registrar luminosidade")
        print("5. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            temperatura = input("Digite a temperatura em Celsius: ")

            if not numeroEhValido(temperatura):
                print("Valor digitado é incorreto.")
                continue
           
            temperatura = celsius_para_fahrenheit(float(temperatura))
            print(f"Temperatura digitada em Fahrenheit: {temperatura}")
            sendDataToTago(temperatura, opcao)
        elif opcao == "2":
            umidade = input("Digite a umidade em g/m3: ")

            if not numeroEhValido(umidade):
                print("Valor digitado é incorreto.")
                continue
           
            umidade = calcular_umidade_relativa(float(umidade))
            print(f"Umidade de g/m3 em kg/m3: {umidade}")
            sendDataToTago(umidade, opcao)
        elif opcao == "3":
            vibracao = input("Digite a vibração em HZ: ")

            if not numeroEhValido(vibracao):
                print("Valor digitado é incorreto.")
                continue

            vibracao = hz_para_rpm(float(vibracao))
            print(f"Umidade de Hz em Rpm: {vibracao}")
            sendDataToTago(vibracao, opcao)
        elif opcao == "4":
            luminosidade = input("Digite a luminosidade em lumens: ")

            if not numeroEhValido(luminosidade):
                print("Valor digitado é incorreto.")
                continue

            luminosidade = converter_lumens_para_lux(float(luminosidade))
            print(f"Luminosidade lumens em lux numa área de 100 m2: {luminosidade}")
            sendDataToTago(luminosidade, opcao)
        elif opcao == "5":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")