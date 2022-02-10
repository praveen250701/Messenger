import socket
from threading import Thread
import cv2
import socket
import numpy
import pickle

hi = 0
SERVER = 'localhost'  # localhost
PORT = 15011
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")


server.listen(1)
conn, addr = server.accept()
print(f"[NEW CONNECTION] {conn} : {addr} connected.")


class Send(Thread):
    def run(self):
        while True:
            msg = input("Enter Message to Send\n>>")
            msg = msg.encode()
            conn.send(msg)
            print(f"Msg Sent to {addr}")


class Receive(Thread):
    def run(self):
        while True:
            r_msg = conn.recv(1024)
            r_msg = r_msg.decode()
            print("[RECEIVED MESSAGE] : " + r_msg)


def sendvidy():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = 'localhost'
    port = 15011
    s.bind((ip, port))
    while True:
        x = s.recvfrom(1000000)
        clientip = x[1][0]
        data = x[0]
        print(data)
        data = pickle.loads(data)
        print(type(data))
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('server', data)  # to open image
        if cv2.waitKey(10) == ord('p'):
            break
    cv2.destroyAllWindows()


def sendy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1501))
    server.listen(10)
    client_socket, client_address = server.accept()
    file = open('scenery1.jpg', 'wb')
    image_chunk = client_socket.recv(2048)
    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)
    file.close()
    client_socket.close()


t1 = Send()
t2 = Receive()
t1.start()
t2.start()
sendy()
sendvidy()
