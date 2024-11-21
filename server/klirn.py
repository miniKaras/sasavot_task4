import socket


def start_client(host='127.0.0.1', port=55555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Подключение к серверу.\n Список комманд: \nset <ключ> <значение> \nget <ключ> \ndelete <ключ> \nexit")

    while True:

        command = input("> ")

        if command.lower() == "exit":
            print("Канец")
            break

        client.send(command.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        print(response)

    client.close()


if __name__ == "__main__":
    start_client()
