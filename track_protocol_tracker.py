import socket
import json

def cria_ligacao():
    #Guarda informação dos nodos
    list_nodes = {}

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
        data = client_socket.recv(1024)
        if not data:
            break

        mensage=data.decode().split("|")
        if (mensage[0]=="startConnection"):
            if mensage[1] not in list_nodes:
                list_nodes[mensage[1]]={}  
        elif (mensage[0]=="filesDictNode"):
            data2 = client_socket.recv(1024)
            list_nodes[mensage[1]]=json.loads(data2.decode())  

        # Envia uma resposta de volta para o cliente
        response = mensage[1]
        client_socket.send(response.encode())

        # Fecha a conexão com o cliente
        client_socket.close()

        # Fecha o socket do servidor
        server_socket.close()

cria_ligacao()









