import socket
from tracker_protocol_mensage import *

def cria_ligacao(name):
    #dicionario das cenas que tem
    dic_files={"adshbsah":[1,2]}

    # Configuração do cliente
    host = '127.0.0.1'
    port = 12345

    # Cria o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((host, port))

    startConnection(client_socket,name)
    filesDictNode(client_socket,name,dic_files)

    # Recebe a resposta do servidor
    data = client_socket.recv(1024)
    print(f"Servidor diz: {data.decode()}")

    # Fecha a conexão com o servidor
    client_socket.close()

cria_ligacao("node1")
    