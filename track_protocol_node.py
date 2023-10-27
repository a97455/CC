import socket
import time
from track_protocol_mensage import *

def Node(node_name):
    #dicionario das cenas que tem
    dict_files={'algo':'teste'}

    # Configuração do cliente
    host = '127.0.0.1'
    port = 12345

    # Cria o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((host, port))

    # Mensagens para o servidor
    #startConnection(client_socket,node_name)

    # Recebe a resposta do servidor
    #data = client_socket.recv(1024)
    #print("Servidor disse: " + data.decode())

    #Só para dar tempo entre a execução das 2 funções
    #time.sleep(5)

    # A funcionar direito se estiver recv(36) no tracker
    filesDictNode(client_socket,node_name,dict_files)

    data = client_socket.recv(1024)
    print("Servidor disse: " + data.decode())

    # Fecha a conexão com o servidor
    client_socket.close()
 
Node("node1")