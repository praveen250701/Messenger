import socket
import cv2
import socket
import pickle
import os

HEADER = 64
PORT = 15011
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = 'localhost'

client = socket.socket()
client.connect((SERVER, PORT))


def send(m, user):
    msg = f'{user} sends => {m}'
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    if 'picture send' in m:
        recy()
    if 'video' in m:
        clientvidy()
    print(client.recv(2048).decode(FORMAT))


def connection():
    stay = True
    user = input('Your Name : ')
    user = user.upper()
    while stay:
        config = input(f'{user.upper()}  want to send message ? (y/n)\n>> ')
        if config == 'n':
            stay = False
            send(DISCONNECT_MESSAGE, user)
        else:
            m = input('Enter the message\n>> ')
            send(m, user)


def clientvidy():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
    serverip = 'localhost'
    ServerPort = 15011
    cap = cv2.VideoCapture(0)
    while True:
        conn, photo = cap.read()
        cv2.imshow('streaming', photo)
        conn, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)
        s.sendto(x_as_bytes, (serverip, ServerPort))
        if cv2.waitKey(10) == ord('p'):
            break
    cv2.destroyAllWindows()
    cap.release()


def recy():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1501))
    file = open('socketpic.jpg', 'rb')
    image_data = file.read(2048)
    while image_data:
        client.send(image_data)
        image_data = file.read(2048)
    file.close()
    client.close()


connection()
clientvidy()
