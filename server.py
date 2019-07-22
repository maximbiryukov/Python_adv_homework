import socket
import json
import time

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')

args = parser.parse_args()

config = {'host': 'localhost', 'port': 8000, 'buffersize': 1024}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file)
        config.update(file_config)

host, port = config.get('host'), config.get('port')


try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    print("server started with {}:{} at {}".format(host, port, time.ctime()))

    while True:
        client, address = sock.accept()
        print('Client was detected {}:{} at {} '.format(address[0], address[1], time.ctime()))

        b_request = client.recv(config.get('buffersize')) # принимаем сообщение клиента

        message = json.loads(b_request.decode())

        print('Client was idenified as \'{}\''.format(message['user']['account_name']))

        response = { # формируем ответ клиенту
            "response": 200,
            "time": time.ctime(),
            "alert": "You've succesfully connected to the server at {} as {}".format(message['time'],message['user']['account_name'])}

        client.send(json.dumps(response).encode()) # посылаем ответ клиенту

        b_message = client.recv(config.get('buffersize')).decode() # принимаем сообщение для ЭХО

        client.send(b_message.encode()) # посылаем сообщение обратно

        client.close()

except KeyboardInterrupt:
    print()
    print('Server was shut down')