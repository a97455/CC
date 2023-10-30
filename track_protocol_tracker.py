import socket
import json
import threading
from track_protocol_mensage import *

dict_nodes_files = {} #Dicionario com os diversos nós e o seu respetivo dict_files
dict_nodes_adress = {} #Dicionario com os diversos nós e os seus endereços

def Connections(client_socket,client_adress):
    while True:
        # Lê dados do cliente
        try:
            header = client_socket.recv(20).decode().split("|")

            data_length = int(header[1], 16)
            data = client_socket.recv(data_length)
            
            if not data:
                break
            
            # message vai ser um dicionário
            message = json.loads(data.decode())

            if header[0] == "000":
                if message['node_name'] not in dict_nodes_files:
                    dict_nodes_files[message['node_name']] = {}
                    dict_nodes_adress[message['node_name']] = client_adress
            elif header[0] == "001":
                if message['node_name'] in dict_nodes_files:
                    dict_nodes_files[message['node_name']] = message['dict_files']
            elif header[0] == "010":
                dict_nodeAdress_listBlocks = {} #Dicionario com o endereco do no (chave) e a lista dos blocos (valor) do ficheiro pedido
                
                for node_name,dict_files in dict_nodes_files.items():
                    for filename,list_blocks in dict_files.items():
                        if message['filename'] == filename:
                            dict_nodeAdress_listBlocks[dict_nodes_adress[node_name]] = list_blocks
                
                filesListTracker(client_socket,dict_nodeAdress_listBlocks)
                
            # Envia uma resposta de volta para o cliente
            response = message['node_name']
            client_socket.send(response.encode())

        except Exception:
            break

    # Fecha a conexão com o cliente
    client_socket.close()


def Tracker(host,port):
    # Cria o socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket ao endereço e porta especificados
    server_socket.bind((host, port))

    # Escuta por conexões
    server_socket.listen(5)
    print(f"Servidor aguardando conexões em {host}:{port}...")
    
    while True:
        # Aceita uma conexão
        client_socket, client_adress = server_socket.accept()
        print(f"Conexão de {client_adress[0]}:{client_adress[1]} estabelecida.")
        minha_thread = threading.Thread(target=Connections, args=(client_socket,client_adress))
        minha_thread.start()

    # Fecha o socket do servidor
    server_socket.close()

Tracker('127.0.0.17',12345)