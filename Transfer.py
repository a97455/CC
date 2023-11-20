import threading
import json
import os

class Transfer:
    def __init__(self,host,socketUDP,folder_path,dict_files_inBlocks,dict_files_complete):

        while True:
            # Recebe dados do cliente (header tem 18 bytes)
            header, client_socket = socketUDP.recvfrom(18)         
            # Cria uma nova thread para cada pedido de bloco recebido
            transfer_thread = threading.Thread(target=self.Transfers, args=(socketUDP,folder_path,
                                                                            dict_files_inBlocks,
                                                                            dict_files_complete,header,
                                                                            client_socket))
            transfer_thread.daemon=True # termina as threads mal o precesso principal morra
            transfer_thread.start()

    def Transfers(self,socketUDP,folder_path,dict_files_inBlocks,dict_files_complete,header,client_socket):
        while True:
            data_length = int(header[1], 16)
            data = client_socket.recv(data_length)
            
            if not data:
                break
            
            # message vai ser um dicionário
            message = json.loads(data.decode())

            if header[0] == "0":
                if message['filename'] in dict_files_complete:
                    file_path = os.path.join(folder_path, message['filename'])
                    blockRequested = getBlock_inFile(file_path,message['block'])
                    socketUDP.sendto(blockRequested, (message['client_socketUDP'], 9090))
                elif message['filename'] in dict_files_inBlocks:
                    block_path = os.path.join(folder_path, message['block'])
                    blockRequested = file_to_binary(block_path)
                    socketUDP.sendto(blockRequested, (message['client_socketUDP'], 9090))


def getBlock_inFile(input_file, block_requested):
        with open(input_file, 'rb') as f:
            for _ in range(block_requested):
                block = f.read(128)  # Tamanho dos blocos (default)
                if not block:
                    break
            return block
        
def file_to_binary(file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        return binary_data