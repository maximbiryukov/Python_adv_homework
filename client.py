import json
import socket
import time

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')

args = parser.parse_args()

config = {'host':'127.0.0.2', 'port':8000, 'buffersize':1024}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file)
        config.update(file_config)

host, port, buffersize = config.get('host'), config.get('port'), config.get('buffersize')



try:
    sock = socket.socket()
    sock.connect((host, port))

    print('Как представимся серверу?')
    name = input()

    presence = { # формируем presence сообщение
        "action": "presence",
        "time": time.ctime(),
        "type": "status",
        "user": {
                "account_name":  name,
                "password":      None
        }
}

    sock.send(json.dumps(presence).encode()) # посылаем presence сообщение
    b_response = sock.recv(buffersize)
    response = json.loads(b_response.decode())

    print('{} {}'.format(response['response'],response['alert'])) # Выводим ответ сервера
    print()
    print('Введите сообщение: ')
    echo_message = input() # принмаем сообщение для эхо

    sock.send(echo_message.encode()) # посылаем сообщение для эхо

    print('А вот и ваше сообщение: {}'.format(sock.recv(buffersize).decode())) # выводим эхо ответ


except KeyboardInterrupt:
    print()
    print('Client shut down')
