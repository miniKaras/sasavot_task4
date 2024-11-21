import socket
import threading
import random


class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipListNode(None, None, self.max_level)

    def random_level(self):
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def set(self, key, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            current.value = value
        else:
            new_level = self.random_level()
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level
            new_node = SkipListNode(key, value, new_level)

            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def get(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return "Нету такого"

    def delete(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            return True
        return "Нету такого"


skip_list = SkipList()


def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        if not command:
            break
        parts = command.split()
        if len(parts) == 0:
            response = "Неверная команда"
        else:
            cmd = parts[0].lower()

            if cmd == "set" and len(parts) == 3:
                key, value = parts[1], parts[2]
                skip_list.set(key, value)
                response = f"Добавлен ключ: {key} со значением: {value}"

            elif cmd == "get" and len(parts) == 2:
                key = parts[1]
                value = skip_list.get(key)
                response = value

            elif cmd == "delete" and len(parts) == 2:
                key = parts[1]
                skip_list.delete(key)

            else:
                response = "Неверная команда"

        client_socket.send(response.encode('utf-8'))

    client_socket.close()


def start_server(host='127.0.0.1', port=55555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Сервер Е {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
