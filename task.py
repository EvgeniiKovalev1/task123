import os
import socket
import logging
import threading
import keyboard

STATIC_DIR = "static"
server = True

logging.basicConfig(filename="server.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    encoding="utf-8")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8000))
server_socket.listen(1)
logging.info("Сервер запущен")


def get_content_type(name):
    """Функция определяющая расширение файла для работы со статкой"""

    if name.endswith(".html"):
        return "text/html"
    elif name.endswith(".css"):
        return "text/css"
    elif name.endswith(".json"):
        return "application/json"
    else:
        return "text/plain"


def make_response(method, path, content_type, response_body, response_code=200):
    """Функция отвечающая за логгирование запросов и их генерацию"""


    response = (
        f"HTTP/1.1 {response_code} OK\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Connection: close\r\n\r\n"
    ).encode() + response_body
    if response_code == 200:
        logging.info(f"Успешный {method}-запрос: {path} ({len(response_body)} байт)")
    elif response_code == 404:
        logging.error(f"404 Не надейно: {path}")
    elif response_code == 405:
        logging.error(f"405 {method} не поддерживается")

    return response


def GET_response(path):
    file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try: ## блок для работы со статикой
            with open(file_path, "rb") as file:
                response_body = file.read()
                content_type = get_content_type(file_path)
                return make_response("GET", path, content_type, response_body, 200)
        except FileNotFoundError:
            return NOT_FOUND_response(path)
    else:
        response_body = b"GET Response" 
        return make_response("GET", path, "text/plain", response_body, 200)


def POST_response(path):
    response_body = b"POST Response"
    return make_response("POST", path, "text/plain", response_body, 200)


def NOT_ALLOWED_response(method, path):
    response_body = f"405 Method {method} Not Allowed".encode()
    return make_response(method, path, "text/plain", response_body, 405)


def NOT_FOUND_response(path):
    response_body = b"404 Not Found"
    return make_response("GET", path, "text/plain", response_body, 404)


def handle_client(client_socket, client_address):
    """Функция разбирающая запросы"""


    request = client_socket.recv(1024).decode()
    request_line = request.split("\n")[0]
    method, path, _ = request_line.split()
    logging.info(f"Запрос от {client_address}: {method} {path}")
    if method == "GET":
        response = GET_response(path)
    elif method == "POST":
        response = POST_response(path)
    else:
        response = NOT_ALLOWED_response(method, path)
    client_socket.sendall(response)
    client_socket.close()


def stop_server():
    server = False
    logging.info("Сервер остановлен пользователем")
    server_socket.close()


keyboard.add_hotkey("q", stop_server)

while server:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
