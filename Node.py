import socket
import os
import json
import sys
import track_protocol_mensage as tpm

class Node:
    def __init__(self,folder_path,host,port):
        # Dicionario com os nomes dos ficheiros (chave) e uma lista dos blocos que tem desse ficheiro (valor)
        self.dict_files = {}
        
        # adiciona os ficheiro do folder_path ao dict_files
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                self.dict_files[file] = file #falta meter a lista de blocos ao inves do nome do ficheiro
        
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
    

    def filesDictNode(self):
        # Mensagens para o servidor
        tpm.filesDictNode(self.client_socket,self.dict_files)

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