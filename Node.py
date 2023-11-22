import socket
import os
import json
import sys
import random
import threading
import Transfer as trs
import track_protocol_mensage as tpm
import transfer_protocol_mensage as trspm

class Node:
    def __init__(self,folder_path,serverHost,serverPort):
        # Dicionario com os filenames (chave) e uma lista dos blocos que tem desse ficheiro (valor)
        self.dict_files_inBlocks = {}
        # Dicionario com os filenames (chave) e o numero de blocos que esse ficheiro tem (valor)
        self.dict_files_complete = {}
        
        # adiciona os ficheiro do folder_path ao dict_files
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                # Calculate the number of blocks of 128 bytes
                file_size = os.path.getsize(item_path)
                num_blocks = (file_size + 127) // 128
                self.dict_files_complete[item] = num_blocks
            elif os.path.isdir(item_path):
                self.dict_files_inBlocks[item] = []
                for block in os.listdir(item_path):
                    block_path = os.path.join(item_path, block)
                    if os.path.isfile(block_path):
                        self.dict_files_inBlocks[item].append(block)

        
        # Criação do socket TCP
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta ao servidor
        self.socketTCP.connect((serverHost, serverPort))


    def startConnection(self):
        # Mensagens para o servidor
        tpm.startConnection(self.socketTCP)

        # Recebe a resposta do servidor 
        self.host=self.socketTCP.recv(1024).decode()

        # Criação do socket UDP
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Associa o socket ao endereço e à porta
        self.socketUDP.bind((self.host, 9090))


    def sendDictsFiles(self):
        # Mensagens para o servidor
        tpm.sendDictsFiles(self.socketTCP,self.dict_files_inBlocks,self.dict_files_complete)


    def getFile(self,filename,folder_path):
        if filename not in self.dict_files_complete:
            # Mensagens para o servidor
            tpm.getFile(self.socketTCP,filename)
            
            while True:
                try:
                    header = self.socketTCP.recv(20).decode().split("|")

                    data_length = int(header[1], 16)
                    data = self.socketTCP.recv(data_length)
                    
                    # message vai ser um dicionário
                    message = json.loads(data.decode())

                    if header[0] == "011":
                        dict_Block_ListNodes = message['dict_Block_ListNodes']

                        for block,listNodes in dict_Block_ListNodes.items():
                            if len(listNodes)==0:
                                print("Nenhum no tem o ficheiro completo")
                                break
                            if block not in self.dict_files_inBlocks:
                                node_selected = random.choice(listNodes)
                                trspm.getBlock(self.socketUDP,self.host,node_selected[0],block,filename)

                                #espera pela resposta com o bloco pedido
                                blockReceived,_ = self.socketUDP.recvfrom(1024)
                                block_path=os.path.join(folder_path,f'{block}')
                                binary_to_file(blockReceived,block_path)

                        # reenvia os seus dicionarios para o Tracker (já com o novo ficheiro transferido)
                        self.sendDictsFiles()
                    elif header[0] == "101":
                        print(message['error'])
                    break
                except Exception:
                    continue
        else:
            print("Já possui o ficheiro completo")

    def endConnection(self):
        # Mensagens para o servidor
        tpm.endConnection(self.socketTCP)

        print("\nConexão Terminada.")

        # Fecha a conexão com o servidor
        self.socketTCP.close()

    
def binary_to_file(binary_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        file.write(binary_data)


def interactive_mode(node,folder_path):
    while True:
        print("\nChoose an option:")
        print("1. Get File")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter the filename: ")
            node.getFile(filename,folder_path)
        elif choice == "2":
            node.endConnection()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Use: python3 Node.py folder_path trackerHost trackerPort")
        sys.exit(1)

    folder_path = sys.argv[1]
    trackerHost = sys.argv[2]
    trackerPort = int(sys.argv[3])

    node = Node(folder_path, trackerHost, trackerPort)
    node.startConnection()
    node.sendDictsFiles()

    try:
        # Cria uma nova thread para cada esperar receber pedidos de blocos no seu socketUDP
        transfer_thread = threading.Thread(target=trs.Transfer, args=(node.host,node.socketUDP,folder_path,
                                                                      node.dict_files_inBlocks,
                                                                      node.dict_files_complete))
        transfer_thread.daemon=True # termina as threads mal o precesso principal morra
        transfer_thread.start()

        # Thread principal vai lidar com os pedidos de ficheiros no node
        interactive_mode(node,folder_path)
        
    except KeyboardInterrupt:
        node.endConnection()
