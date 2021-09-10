import socket
import threading
from time import sleep


def echo_server(host, port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        _live = True
        i = 0
        while _live:
            conn, addr = s.accept()

            with conn:
                data = conn.recv(1024)
                if not data:
                    break
                if data == bytes(alph[i], 'utf-8'):
                    i += 2
                    if i == len(alph):
                        conn.send(
                            bytes("Last letter - z. Good job. Take a pie from the shelf.", 'utf-8'))
                        _live = False
                    else:
                        conn.send(bytes(alph[i-1], 'utf-8'))
                else:
                    conn.send(
                        bytes(f'Wrong. Next letter must be {alph[i]}', 'utf-8'))
                    _live = False


def simple_client(host, port):

    _live = True
    while _live:
        with socket.socket() as s:
            s.connect((host, port))

            try:
                s.sendall(bytes(input(">>> "), 'utf-8'))
                data = s.recv(1024)
                print(f'server: {data.decode("utf-8")}')
                if data.decode('utf-8')[:5].lower() == 'wrong':
                    _live = False
                if data.decode('utf-8')[:4].lower() == 'last':
                    _live = False
            except ConnectionRefusedError:
                sleep(0.5)


HOST = '127.0.0.1'
PORT = 55555
alph = 'abcdefghijklmnopqrstuvwxyz'

print('I will check your knowledge alphabet. We will write one character one by one. You start.')
server = threading.Thread(target=echo_server, args=(HOST, PORT))

client = threading.Thread(target=simple_client, args=(HOST, PORT))
server.start()
client.start()
server.join()
client.join()

print('Done!')
