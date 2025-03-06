# a b c d e f g h i j k l m n o p q r s t u v w x y z
# import requests
import socket

# from http.server import BaseHTTPRequestHandler, HTTPServer


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(123)

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    print("Request:\n", request)
    request_line = request.split("\n")[0]
    method, path, _ = request_line.split()
    if method == "GET":
        response_method = "GET"
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"
    elif method == "POST":
        response_method = "POST"
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"
    else:
        response_method = "Error"
        response = f"HTTP/1.1 404 \r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"
    