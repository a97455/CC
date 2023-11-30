import socket
import time
import os
import json
import sys
import random
import threading
import DNS as dns
import Transfer as trs
import track_protocol_mensage as tpm
import transfer_protocol_mensage as trspm

class Node:  
    classLock=threading.Lock()

    def __init__(self,folder_path,trackerHost,trackerPort):
        # Dicionario com os filenames (chave) e uma lista dos blocos que tem desse ficheiro (valor)
        self.dict_files_inBlocks = {}
        # Dicionario com os filenames (chave) e o numero de blocos que esse ficheiro tem (valor)
        self.dict_files_complete = {}

        # caminho para a sua pasta de ficheiros locais
        self.folder_path=folder_path

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
        #Nome do Node
        self.name=socket.gethostname()
        # Conecta ao servidor
        self.socketTCP.connect((trackerHost, trackerPort))


    def startConnection(self):
        # Mensagens para o servidor
        tpm.startConnection(self.socketTCP,self.name)

        # Recebe a resposta do servidor 
        self.host=self.socketTCP.recv(1024).decode()

        # Criação do socket UDP
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Associa o socket ao endereço e à porta
        self.socketUDP.bind((self.host, 9090))


    def sendDictsFiles(self):
        # Mensagens para o servidor
        tpm.sendDictsFiles(self.socketTCP,self.dict_files_inBlocks,self.dict_files_complete)


    def getFile(self,filename):        
        if filename not in self.dict_files_complete:
            # Mensagens para o servidor
            tpm.getFile(self.socketTCP,filename)

            header = self.socketTCP.recv(20).decode().split("|")

            data_length = int(header[1], 16)
            data = self.socketTCP.recv(data_length)
            
            # message vai ser um dicionário
            message = json.loads(data.decode())

            if header[0] == "011":
                dict_Block_ListNodes = message['dict_Block_ListNodes']

                if filename not in self.dict_files_inBlocks:
                    self.dict_files_inBlocks[filename]= [] 
                    
                for block,listNodes in dict_Block_ListNodes.items():
                    if len(listNodes)==0:
                        print("Nenhum no tem o ficheiro completo")
                        break
                    if block not in self.dict_files_inBlocks[filename]:
                        # Cria uma nova thread para enviar cada pedido de bloco
                        transfer_thread = threading.Thread(target=self.getBlock, args=(listNodes,block,filename,message['numBlocks'],Node.classLock))
                        transfer_thread.daemon=True # termina as threads mal o processo principal morra
                        transfer_thread.start()

            elif header[0] == "101":
                print(message['error'])
        else:
            print("Já possui o ficheiro completo")


    def getBlock(self,listNodes,block,filename,numBlocks,classLock):
        node_selected = random.choice(listNodes)
        trspm.getBlock(self.socketUDP,node_selected[0],self.host,block,filename,numBlocks,classLock)

        BlockLocaly= False
        while not BlockLocaly:
            time.sleep(5) #espera pela chegada dos blocos

            if block in self.dict_files_inBlocks[filename]:
                BlockLocaly=True
            else:
                trspm.getBlock(self.socketUDP,node_selected[0],self.host,block,filename,numBlocks,classLock) #volta a pedir o bloco que se perdeu na rede


    def endConnection(self):
        # Mensagens para o servidor
        tpm.endConnection(self.socketTCP,self.name)

        # Fecha os seus sockets
        self.socketTCP.close()
        self.socketUDP.close()

        print("\nConexão Terminada.")

    
def interactive_mode(node):
    while True:
        print("\nChoose an option:")
        print("1. Get File")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter the filename: ")
            node.getFile(filename)
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
    trackerHost = dns.get_host_by_name(sys.argv[2])
    trackerPort = int(sys.argv[3])

    node = Node(folder_path, trackerHost, trackerPort)
    node.startConnection()
    node.sendDictsFiles()

    try:
        # Cria uma nova thread para cada esperar receber pedidos de blocos no seu socketUDP
        transfer_thread = threading.Thread(target=trs.Transfer, args=(node.folder_path,node.socketTCP,node.socketUDP,
                                                                      node.dict_files_complete,node.dict_files_inBlocks,
                                                                      Node.classLock))
        transfer_thread.daemon=True # termina as threads mal o processo principal morra
        transfer_thread.start()

        # Thread principal vai lidar com os pedidos de ficheiros no node
        interactive_mode(node)
        
    except KeyboardInterrupt:
        node.endConnection()
