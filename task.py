import os
import socket
import logging
import threading

STATIC_DIR = "static"
SERVER_RUNNING = True

logging.basicConfig(filename="server.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    encoding="utf-8")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8000))
server_socket.listen(1)
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


def GET_response(path):
    file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, "rb") as file:
                response_body = file.read()
                content_type = get_content_type(file_path)
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode() + response_body
                logging.info(f"Успешный GET-запрос к статике: {path} ({len(response_body)} байт)")
                return response
        except FileNotFoundError:
            return NOT_FOUND_response()
    else:
        response_body = "GET Response"
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"Content-Type: text/plain\r\n"
            f"Connection: close\r\n\r\n"
            f"{response_body}"
        ).encode()
        logging.info(f"Успешный GET-запрос: {path} ({len(response_body)} байт)")
        return response

def POST_response(path):
    response_body = "POST Response"
    response = (
        f"HTTP/1.1 200 OK\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Connection: close\r\n\r\n"
        f"{response_body}"
    ).encode()
    logging.info(f"Успешный POST-запрос: {path}")
    return response

def NOT_ALLOWED_response(method):
    response_body = f"405 Method {method} Not Allowed"
    response = (
        f"HTTP/1.1 405 Method Not Allowed\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Connection: close\r\n\r\n"
        f"{response_body}"
    ).encode()
    logging.error("{method} не поддерживается")
    return response

def NOT_FOUND_response():
    response_body = "404 Not Found"
    response = (
        f"HTTP/1.1 404 Not Found\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Connection: close\r\n\r\n"
        f"{response_body}"
    ).encode()
    logging.error("404")
    return response

def handle_client(client_socket, client_address):
        request = client_socket.recv(1024).decode()
        request_line = request.split("\n")[0]
        method, path, _ = request_line.split()
        logging.info(f"Запрос от {client_address}")
        if method == "GET":
            response = GET_response(path)
        elif method == "POST":
            response = POST_response(path)
        else:
            response = NOT_ALLOWED_response(method)
        client_socket.sendall(response)
        client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()