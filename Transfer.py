import threading
import json
import os

class Transfer:
    def __init__(self,node,folder_path):
        self.lock=threading.Lock()
        while True:
            with self.lock:
                # Recebe dados do cliente (header tem 18 bytes)
                data,_= node.socketUDP.recvfrom(18)
                header=data.decode().split('|')

                data_length = int(header[1], 16)
                data_message,_= node.socketUDP.recvfrom(data_length)

                # message vai ser um dicionário
                message = json.loads(data_message.decode())

                if header[0]== '0':
                    # Cria uma nova thread para cada pedido de bloco recebido
                    transfer_thread = threading.Thread(target=self.getBlock, args=(node,message))
                    transfer_thread.daemon=True # termina as threads mal o precesso principal morra
                    transfer_thread.start()
                elif header[0]== '1':        
                    #espera pela resposta com o bloco pedido
                    blockReceived,_ = self.node.socketUDP.recvfrom(1024)
                    block_path=os.path.join(folder_path,f'{block}')
                    binary_to_file(blockReceived,block_path)
                    self.dict_files_inBlocks[filename]=block

                    # reenvia os seus dicionarios para o Tracker (já com o novo ficheiro transferido)
                    node.sendDictsFiles()

    def getBlock(node,message):
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