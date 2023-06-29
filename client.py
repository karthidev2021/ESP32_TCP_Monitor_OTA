import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("192.168.1.6",2002))

while True:
    a=input()
    client.send(a.encode("utf-8"))