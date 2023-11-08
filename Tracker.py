import socket
import json
import threading
import track_protocol_mensage as tpm

class Tracker:
    node_count=1

    def __init__(self,host,port): 
        #Dicionario com os diversos endereços de nós (host,port) e o seu respetivo nome
        self.dict_address_nodeName = {}
        #Dicionario com os diversos nós(nome) e o seu respetivo dict_file 
        self.dict_address_dictFiles = {}

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
                connections_thread.daemon=True #termina as threads mal o precesso principal termina
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

                if header[0] == "000":
                    if client_address not in self.dict_address_nodeName:
                        node_name="Node"+str(Tracker.node_count)
                        Tracker.node_count+=1
                        
                        self.dict_address_nodeName[client_address] = node_name
                        self.dict_address_dictFiles[client_address] = {}

                        # Envia uma resposta de volta para o cliente
                        response = "Conexão realizada: "+node_name
                        client_socket.send(response.encode())

                elif header[0] == "001":
                    if client_address in self.dict_address_nodeName:
                        self.dict_address_dictFiles[client_address] = message['dict_files']
                
                elif header[0] == "010":
                    dict_nodeAddress_listBlocks = {} # Dicionario com o endereco do nó (chave) e a lista dos blocos (valor) do ficheiro pedido
                    
                    for node_address,dict_files in self.dict_address_dictFiles.items():
                        for filename,list_blocks in dict_files.items():
                            if message['filename'] == filename:
                                dict_nodeAddress_listBlocks[node_address] = list_blocks
                    
                    tpm.filesListTracker(client_socket,dict_nodeAddress_listBlocks)
                
                elif header[0] == '100':
                    if client_address in self.dict_address_nodeName:
                        self.dict_address_dictFiles.pop(client_address)
                        self.dict_address_nodeName.pop(client_address)

            except IndexError:
                break

        client_socket.close()

    def stopTracker(self):
        print("\nTracker terminado.")

        # Fecha o socket do servidor
        self.server_socket.close()


if __name__ == '__main__':
    Tracker('127.0.0.17',12345)