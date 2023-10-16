import socket
from track_protocol_mensage import *

def Node(name):
    #dicionario das cenas que tem
    dict_files={}

    # Configuração do cliente
    host = '127.0.0.1'
    port = 12345

    # Cria o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((host, port))

    # Mensagens para o servidor
    startConnection(client_socket,name)
    filesDictNode(client_socket,name,dict_files)

    # Recebe a resposta do servidor
    data = client_socket.recv(1024)
    print(f"Servidor diz: {data.decode()}")

    # Fecha a conexão com o servidor
    client_socket.close()

Node("node1")