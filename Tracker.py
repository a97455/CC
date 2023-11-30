import socket
import json
import threading
import DNS as dns
import track_protocol_mensage as tpm

class Tracker:
    node_count=1

    def __init__(self,host,port): 
        self.listNodes = []
        # Dicionario com os diversos ficheiros (filename) e o seu dicionario que relaciona os seus blocos (chave) com a lista de nodos onde eles existem (valor)
        self.dict_filename_dictBlockListNodes = {}
        # Dicionario com os diversos ficheiros (filename) e o seu respetivo numero de blocos
        self.dict_filename_numBlocks = {} 

        try:
            # Cria o socket TCP
            self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Liga o socket ao endereço e porta especificados
            self.tracker_socket.bind((host, port))
            # Escuta por conexões
            self.tracker_socket.listen(5)
            print(f"Servidor aguardando conexões em {host}:{port}...")

            while True:
                # Aceita uma conexão
                client_socket, client_adress = self.tracker_socket.accept()
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
                    if message['name'] not in self.listNodes:
                        self.listNodes.append(message['name'])

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
                            blockString=str(block)
                            if blockString in self.dict_filename_dictBlockListNodes[filename]: #chave é a string do numBloco
                                if client_address not in self.dict_filename_dictBlockListNodes[filename][blockString]:
                                    self.dict_filename_dictBlockListNodes[filename][blockString].append(client_address)
                            else:
                                self.dict_filename_dictBlockListNodes[filename][blockString] = [client_address]

                elif header[0] == "010": # getFile
                    if message['filename'] not in self.dict_filename_numBlocks:
                        error="Nenhum nó tem o ficheiro inteiro"
                        tpm.noFileComplete(client_socket,error)
                    else:
                        tpm.sendDictBlockListNodes(client_socket,self.dict_filename_dictBlockListNodes[message['filename']],self.dict_filename_numBlocks[message['filename']])
                
                elif header[0] == "110": #newBlockLocaly
                    self.dict_filename_dictBlockListNodes[message['filename']][message['block']].append(client_address)

                elif header[0] == '100': # endConnection
                    if message['name'] in self.listNodes:
                        self.listNodes.remove(message['name'])

                        for dictBlockListNodes in self.dict_filename_dictBlockListNodes.values():
                            for listNodes in dictBlockListNodes.values():
                                if client_address in listNodes:
                                    listNodes.remove(client_address)

            except IndexError:
                break

        client_socket.close()

    def stopTracker(self):
        # Fecha o socket do servidor
        self.tracker_socket.close()

        print("\nTracker terminado.")


if __name__ == '__main__':
    dns.start_named_server()
    Tracker('10.4.4.1',9090)