import socket
from request_handler import handler

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 53))

while True:
    message, address = server_socket.recvfrom(1024)
    response = handler(message)
    print(response)
    if response != None:
        server_socket.sendto(response, address)
        print("send")