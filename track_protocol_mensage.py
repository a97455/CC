import json

def startConnection(client_socket,node_name):
    # Envia dados para o servidor

    message = "startConnection"+"|"+node_name+"\n"
    client_socket.send(str(len(message)).encode())
    client_socket.send(message.encode())

def filesDictNode(client_socket,node_name,dict_files):
    message = "filesDictNode"+"|"+node_name+json.dumps(dict_files)+"\n"
    client_socket.send(message.encode()) 