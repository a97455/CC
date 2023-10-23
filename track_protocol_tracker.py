import socket
import json
import sys

def Tracker():
    # Guarda informação dos nodos e seus respetivos ficheiros
    dict_nodes_files = {}

    # Configuração do servidor
    host = '127.0.0.1'
    port = 12345

    # Cria o socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket ao endereço e porta especificados
    server_socket.bind((host, port))

    # Escuta por conexões
    server_socket.listen(5)

    print(f"Servidor aguardando conexões em {host}:{port}...")

    while True:
        # Aceita uma conexão
        client_socket, addr = server_socket.accept()
        print(f"Conexão de {addr[0]}:{addr[1]} estabelecida.")

        # Lê dados do cliente
        header=client_socket.recv(39).decode().split("|")
        print(header)

        data_length = int.from_bytes(eval(header[1].encode()),byteorder='big')
        data = client_socket.recv(data_length)
        
        if not data:
            break

        message=data.decode().split("|")
        if (header[0]=="000"):
            if message[0] not in dict_nodes_files:
                dict_nodes_files[message[0]]={}  
                print(dict_nodes_files) # test
        elif (header[0]=="001"):
            if message[0] in dict_nodes_files:
                dict_nodes_files[message[0]]=json.loads(message[1])
                print(dict_nodes_files) # teste

        # Envia uma resposta de volta para o cliente
        response = message[0]
        client_socket.send(response.encode())

    # Fecha a conexão com o cliente
    client_socket.close()

    # Fecha o socket do servidor
    server_socket.close()

Tracker()