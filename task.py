# a b c d e f g h i j k l m n o p q r s t u v w x y z
# import requests
import socket

# from http.server import BaseHTTPRequestHandler, HTTPServer

from task123.constants import HOST, PORT

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(123)

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    print("Request:\n", request)
    request_line = request.split("\n")[0]
    method, path, _ = request_line.split()
    if method == "GET":
        response_method = "GET"
    elif method == "POST":
        response_method = ""
    else:
        response_method = "Error"
    response = f"200, {response_method}"
