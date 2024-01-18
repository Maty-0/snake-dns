import socket
import concurrent.futures
from request_handler import handler

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 53))

while True:
    message, address = server_socket.recvfrom(1024)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(handler(message, server_socket, address), 1)