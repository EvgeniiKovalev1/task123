import os
import socket

STATIC_DIR = "static"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(123)

def get_content_type(name):
    if name.endswith(".html"):
        return "text/html"
    elif name.endswith(".css"):
        return "text/css"
    elif name.endswith(".json"):
        return "application/json"
    else:
        return "text/plain"

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    request_line = request.split("\n")[0]
    method, path, _ = request_line.split()
    if method == "GET":
        file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
        with open(file_path, "rb") as file:
            response_method = file.read()
            content_type = get_content_type(file_path)
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_method)}\r\nContent-Type: {content_type}\r\n\r\n{response_method}/r/nConnection: close"
    elif method == "POST":
        response_method = "POST"
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"
    else:
        response_method = "Error"
        response = f"HTTP/1.1 404 \r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"

    client_socket.sendall(response)
    client_socket.close()
