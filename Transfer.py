import threading
import json
import os

class Transfer:
    def __init__(self,host,socketUDP,folder_path,dict_files_inBlocks,dict_files_complete):
        while True:
            # Recebe dados do cliente (header tem 18 bytes)
            data,_= socketUDP.recvfrom(18)
            header=data.decode().split('|')
            print(header)

            # le a segunda vez, os dados do pacote
            data_length = int(header[1], 16)
            data,_= socketUDP.recvfrom(data_length)

            # message vai ser um dicionário
            message = json.loads(data.decode())

            # Cria uma nova thread para cada pedido de bloco recebido
            transfer_thread = threading.Thread(target=self.Transfers, args=(socketUDP,folder_path,
                                                                            dict_files_inBlocks,
                                                                            dict_files_complete,header,
                                                                            message))
            transfer_thread.daemon=True # termina as threads mal o precesso principal morra
            transfer_thread.start()

    def Transfers(self,socketUDP,folder_path,dict_files_inBlocks,dict_files_complete,header,message):
        if header[0] == "0":
            if message['filename'] in dict_files_complete:
                file_path = os.path.join(folder_path, message['filename'])
                blockRequested = getBlock_inFile(file_path,message['block'])
                socketUDP.sendto(blockRequested, (message['client_host'],9090))
            elif message['filename'] in dict_files_inBlocks:
                block_path = os.path.join(folder_path, message['block'])
                blockRequested = file_to_binary(block_path)
                socketUDP.sendto(blockRequested, (message['client_host'],9090))


def getBlock_inFile(input_file, block_requested): 
        with open(input_file, 'rb') as f:
            for _ in range(int(block_requested)):
                block = f.read(128)  # Tamanho dos blocos (default)
                if not block:
                    break
            return block
        
def file_to_binary(file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        return binary_data