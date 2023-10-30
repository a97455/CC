import socket
import time
from track_protocol_mensage import *

def Node(node_name,host,port):
    # Dicionario com os blocos dos diversos ficheiros que lhe pertencem
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

    # Não está a executar
    filesDictNode(client_socket,node_name,dict_files)

    data = client_socket.recv(1024)
    print("Servidor disse: " + data.decode())

    # Fecha a conexão com o servidor
    client_socket.close()
 
Node("node1",'127.0.0.17',12345)