import socket
import json
import threading
import track_protocol_mensage as tpm

class Tracker:
    node_count=1

    def __init__(self,host,port): 
        # Dicionario com os diversos endereços de nós (host,port) e o seu respetivo nome
        self.dict_address_nodeName = {}
        # Dicionario com os diversos ficheiros (filename) e o seu dicionario que relaciona os seus blocos (chave) com a lista de nodos onde eles existem (valor)
        self.dict_filename_dictBlockListNodes = {}
        # Dicionario com os diversos ficheiros (filename) e o seu respetivo numero de blocos
        self.dict_filename_numBlocks = {} 

        try:
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

                # Cria uma nova thread para cada nova conexão estabelecida
                connections_thread = threading.Thread(target=self.Connections, args=(client_socket,client_adress))
                connections_thread.daemon = True # termina as threads mal o precesso principal morra
                connections_thread.start()


        except KeyboardInterrupt:
            self.stopTracker()

    def Connections(self,client_socket,client_address):
        while True:
            try:
                # Lê dados do cliente
                header = client_socket.recv(20).decode().split("|")

                data_length = int(header[1], 16)
                data = client_socket.recv(data_length)
                
                if not data:
                    break
                
                # message vai ser um dicionário
                message = json.loads(data.decode())

                if header[0] == "000": # startConnection
                    if client_address not in self.dict_address_nodeName:
                        node_name = "Node" + str(Tracker.node_count)
                        Tracker.node_count += 1
                        
                        self.dict_address_nodeName[client_address] = node_name

                        # Envia uma resposta de volta para o cliente (nodeHost)
                        response = client_address[0]
                        client_socket.send(response.encode())

                elif header[0] == "001": # sendDictsFiles
                    for filename,list_blocks in message['dict_files_inBlocks'].items():
                        if filename not in self.dict_filename_dictBlockListNodes:
                            self.dict_filename_dictBlockListNodes[filename] = {}
                        for block in list_blocks:
                            if block in self.dict_filename_dictBlockListNodes[filename]:
                                if client_address not in self.dict_filename_dictBlockListNodes[filename][block]:
                                    self.dict_filename_dictBlockListNodes[filename][block].append(client_address)
                            else:
                                self.dict_filename_dictBlockListNodes[filename][block] = [client_address]

                    for filename,numBlocks in message['dict_files_complete'].items():
                        self.dict_filename_numBlocks[filename] = numBlocks

                        if filename not in self.dict_filename_dictBlockListNodes:
                            self.dict_filename_dictBlockListNodes[filename] = {}

                        for block in range(1,numBlocks+1):
                            if block in self.dict_filename_dictBlockListNodes[filename]:
                                if client_address not in self.dict_filename_dictBlockListNodes[filename][block]:
                                    self.dict_filename_dictBlockListNodes[filename][block].append(client_address)
                            else:
                                self.dict_filename_dictBlockListNodes[filename][block] = [client_address]

                elif header[0] == "010": # getFile
                    if message['filename'] not in self.dict_filename_numBlocks:
                        print("Nenhum nó do servidor tem o ficheiro inteiro")
                    else:
                        tpm.sendDictBlockListNodes(client_socket,self.dict_filename_dictBlockListNodes[filename],self.dict_filename_numBlocks[filename])
                
                elif header[0] == '100': # endConnection
                    if client_address in self.dict_address_nodeName:
                        self.dict_address_nodeName.pop(client_address)
                        for dictBlockListNodes in self.dict_filename_dictBlockListNodes.values():
                            for listNodes in dictBlockListNodes.values():
                                if client_address in listNodes:
                                    listNodes.remove(client_address)
            except IndexError:
                break

        client_socket.close()

    def stopTracker(self):
        print("\nTracker terminado.")

        # Fecha o socket do servidor
        self.server_socket.close()


if __name__ == '__main__':
    Tracker('127.0.0.17',12345)