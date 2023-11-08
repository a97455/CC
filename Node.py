import socket
import os
import json
import sys
import track_protocol_mensage as tpm

class Node:
    def __init__(self,folder_path,host,port):
        # Dicionario com os nomes dos ficheiros (chave) e uma lista dos blocos que tem desse ficheiro (valor)
        self.dict_files_inBlocks = {}
        # Dicionario com os nomes dos ficheiros (chave) e o numero de blocos que esse ficheiro tem (valor)
        self.dict_files_complete = {}
        
        # adiciona os ficheiro do folder_path ao dict_files
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                # Calculate the number of blocks of 1024 bytes
                file_size = os.path.getsize(item_path)
                num_blocks = (file_size + 1023) // 1024
                self.dict_files_complete[item] = num_blocks
            elif os.path.isdir(item_path):
                # Aqui você deve percorrer os arquivos na diretoria específica 'item_path'
                self.dict_files_inBlocks[item] = []
                for block in os.listdir(item_path):
                    block_path = os.path.join(item_path, block)
                    if os.path.isfile(block_path):
                        self.dict_files_inBlocks[item].append(block)

        
        # Cria o socket TCP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta ao servidor
        self.client_socket.connect((host, port))


    def startConnection(self):
        # Mensagens para o servidor
        tpm.startConnection(self.client_socket)

        # Recebe a resposta do servidor
        data = self.client_socket.recv(1024)
        print(data.decode())
    

    def sendDictsFiles(self):
        # Mensagens para o servidor
        tpm.sendDictsFiles(self.client_socket,self.dict_files_inBlocks,self.dict_files_complete)


    def getFile(self,filename):
        # Mensagens para o servidor
        tpm.getFile(self.client_socket,filename)
        
        while True:
            try:
                header = self.client_socket.recv(20).decode().split("|")

                data_length = int(header[1], 16)
                data = self.client_socket.recv(data_length)
                
                # message vai ser um dicionário
                message = json.loads(data.decode())

                if header[0] == "011":
                    dict_nodeAddress_listBlocks = message['dict_nodeAddress_listBlocks']

                    # funcao para transferir o ficheiro ou parte dele de um no(transfer_protocol) 

                    # reenvia o seu dict_files para o Tracker (já com o novo ficheiro transferido)
                    self.filesDictNode(self.client_socket,self.dict_files)
                    break

            except Exception:
                continue

    def endConnection(self):
        # Mensagens para o servidor
        tpm.endConnection(self.client_socket)

        print("\nConexão Terminada.")

        # Fecha a conexão com o servidor
        self.client_socket.close()


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
        print("Use: python3 Node.py folder_path host port")
        sys.exit(1)

    folder_path = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])

    node = Node(folder_path, host, port)
    node.startConnection()
    node.filesDictNode()

    try:
        interactive_mode(node)
    except KeyboardInterrupt:
        node.endConnection()