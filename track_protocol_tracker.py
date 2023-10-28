import socket
import json
import sys

def Tracker():
    # Guarda informação dos nodos e seus respetivos ficheiros
    # Para testar a filesDictNode (o node tem de estar no dicionário)
    dict_nodes_files = {'node1':{}}

    # Configuração do servidor
    host = '127.0.0.17'
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
        # FIXME: Para a função filesDictNode funciona com recv(36), para o startConnection tem de ser recv(39), não sei exatamente porque é que o tamanho do header é diferente nos 2
        header=client_socket.recv(20).decode().split("|")

        data_length = int(header[1], 16)
        data = client_socket.recv(data_length)
        
        if not data:
            break
        
        # message vai ser um dicionário
        message=json.loads(data.decode())
        if (header[0]=="000"):
            if message['node_name'] not in dict_nodes_files:
                dict_nodes_files[message['node_name']]={}  
                print(dict_nodes_files) # test
        elif (header[0]=="001"):
            print("Entrei na 001")
            if message['node_name'] in dict_nodes_files:
                dict_nodes_files[message['node_name']] = message['filesDictNode']
                print(dict_nodes_files) # teste

                # Envia uma resposta de volta para o cliente
                response = message['node_name']
                client_socket.send(response.encode())
            

    # Fecha a conexão com o cliente
    client_socket.close()

    # Fecha o socket do servidor
    server_socket.close()

Tracker()