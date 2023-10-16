import json

def startConnection(client_socket,node_name):
    # Envia dados para o servidor
    message = "startConnection"+"|"+node_name
    client_socket.send(message.encode())

def filesDictNode(client_socket,node_name,dict_files):
    message = "filesDictNode"+"|"+node_name
    client_socket.send(message.encode())
    client_socket.send(json.dumps(dict_files).encode())