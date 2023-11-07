import socket
import json
import threading
import track_protocol_mensage as tpm

dict_address_nodeName = {} #Dicionario com os diversos endereços de nós (host,port) e o seu respetivo nome
dict_nodeName_dictFiles = {} #Dicionario com os diversos nós(nome) e o seu respetivo dict_files

def Connections(client_socket,client_address,node_count):
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
                if client_address not in dict_address_nodeName:
                    node_name="Node"+str(node_count)
                    node_count+=1
                    
                    dict_address_nodeName[client_address] = node_name
                    dict_nodeName_dictFiles[node_name] = {}
            elif header[0] == "001":
                if dict_address_nodeName[client_address] in dict_nodeName_dictFiles:
                    dict_nodeName_dictFiles[dict_address_nodeName[client_address]] = message['dict_files']
            elif header[0] == "010":
                dict_nodeAddress_listBlocks = {} # Dicionario com o endereco do nó (chave) e a lista dos blocos (valor) do ficheiro pedido
                
                for node_name,dict_files in dict_nodeName_dictFiles.items():
                    for filename,list_blocks in dict_files.items():
                        if message['filename'] == filename:
                            dict_nodeAddress_listBlocks[dict_address_nodeName[node_name]] = list_blocks
                
                tpm.filesListTracker(client_socket,dict_nodeAddress_listBlocks)
            elif header[0] == '100':
                if dict_address_nodeName[client_address] in dict_nodeName_dictFiles:
                    dict_nodeName_dictFiles.pop(dict_address_nodeName[client_address])
                    dict_address_nodeName.pop(dict_address_nodeName[client_address])
                
            # Envia uma resposta de volta para o cliente
            response = dict_address_nodeName[client_address]
            client_socket.send(response.encode())

        except Exception:
            break

    # Fecha a conexão com o cliente
    client_socket.close()


class Tracker():
    node_count=1

    def __init__(self,host,port): 
        # Cria o socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Liga o socket ao endereço e porta especificados
        self.server_socket.bind((host, port))

        # Escuta por conexões
        self.server_socket.listen(5)
        print(f"Servidor aguardando conexões em {host}:{port}...")
    
        while True:
            # Aceita uma conexão
            client_socket, client_adress = self.server_socket.accept()
            print(f"Conexão de {client_adress[0]}:{client_adress[1]} estabelecida.")
            my_thread = threading.Thread(target=Connections, args=(client_socket,client_adress,Tracker.node_count))
            my_thread.start()

    def closeTracker(self):
        # Fecha o socket do servidor
        self.server_socket.close()

Tracker('127.0.0.17',12345) #no core seria host,port (10.4.4.1:9090)