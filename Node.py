import socket
import os
import json
import track_protocol_mensage as tpm

class Node:
    name_count=1

    def __init__(self,folder_path,host,port):
        # Dicionario com os nomes dos ficheiros (chave) e uma lista dos blocos que tem desse ficheiro (valor)
        self.dict_files = {}
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                self.dict_files[file] = None
        
        # Nome do nodo
        self.node_name = "Node"+str(name_count)
        name_count += 1
        
        # Cria o socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta ao servidor
        client_socket.connect((host, port))
        
    def startConnection(self,client_socket,node_name):
        # Mensagens para o servidor
        tpm.startConnection(client_socket,node_name)
        # Recebe a resposta do servidor
        data = client_socket.recv(1024)
        print("Conexão realizada: " + data.decode())
    
    def filesDictNode(self,client_socket,node_name,dict_files):
        # Mensagens para o servidor
        tpm.filesDictNode(client_socket,node_name,dict_files)
        data = client_socket.recv(1024)
        print("Ficheiros locais recebidos: " + data.decode())


    def getFile(self,client_socket,filename):
        # Mensagens para o servidor
        tpm.getFile(client_socket,filename)
        
        while True:
            try:
                header = client_socket.recv(20).decode().split("|")

                data_length = int(header[1], 16)
                data = client_socket.recv(data_length)
                
                # message vai ser um dicionário
                message = json.loads(data.decode())

                if header[0] == "011":
                    dict_nodeAddress_listBlocks = message['dict_nodeAddress_listBlocks']

                    # funcao para transferir o ficheiro ou parte dele de um no(transfer_protocol) 
                    self.filesDictNode(client_socket,self.node_name,self.dict_files)
                    break

            except Exception:
                continue

    def endConnection(client_socket,node_name):
        # Mensagens para o servidor
        tpm.endConnection(client_socket,node_name)

        data = client_socket.recv(1024)
        print("Conexão Terminada: " + data.decode())

        # Fecha a conexão com o servidor
        client_socket.close()