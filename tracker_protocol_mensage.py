import json

def startConnection(client_socket,name):
    # Envia dados para o servidor
    message = "startConnection"+"|"+name
    client_socket.send(message.encode())

def filesDictNode(client_socket,name,dicionario):
    message = "filesDictNode"+"|"+name
    client_socket.send(message.encode())
    client_socket.send(json.dumps(dicionario).encode())