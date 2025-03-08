import os
import socket
import logging

STATIC_DIR = "static"

logging.basicConfig(filename="server.log",
level=logging.INFO,
format="%(asctime)s - %(levelname)s - %(message)s")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(123)
logging.info("Сервер запущен")

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
    logging.info(f"Запрос от {client_address}")
    if method == "GET":
        file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
        try:
            with open(file_path, "rb") as file:
                response_method = file.read()
                content_type = get_content_type(file_path)
                response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_method)}\r\nContent-Type: {content_type}\r\n\r\n{response_method}/r/nConnection: close"
                logging.info(f"Успешный GET-запрос: {path} {len(response_method)} байт")
        except Error:
            response = f"HTTP/1.1 404 Not Found"
            logging.error(f"{file_path} не найден")
    elif method == "POST":
        response_method = "POST"
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"
        logging.info(f"Успешный POST-запрос: {path}")
    else:
        response_method = "Not allowed"
        response = f"HTTP/1.1 405 \r\nContent-Length: {len(response_method)}\r\nContent-Type: text/plain\r\n\r\n{response_method}/r/nConnection: close"
        logging.error(f"{method}-Не поддерживается")

    client_socket.sendall(response)
    client_socket.close()
