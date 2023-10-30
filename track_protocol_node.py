import socket
import time
from track_protocol_mensage import *

def Node(node_name,host,port):
    # Dicionario com os nomes dos ficheiros que tem como chaves e os valores uma lista dos blocos desse ficheiro
    dict_files={}

    # Cria o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((host, port))

    # Mensagens para o servidor
    startConnection(client_socket,node_name)

    # Recebe a resposta do servidor
    data = client_socket.recv(1024)
    print("Servidor disse: " + data.decode())

    # Mensagens para o servidor
    filesDictNode(client_socket,node_name,dict_files)

    data = client_socket.recv(1024)
    print("Servidor disse: " + data.decode())

    # Fecha a conexão com o servidor
    client_socket.close()
