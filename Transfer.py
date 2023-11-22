import threading
import json
import os
import track_protocol_mensage as tpm
import transfer_protocol_mensage as trspm

class Transfer:
    def __init__(self,folder_path,socketTCP,socketUDP,dict_files_complete,dict_files_inBlocks):
        self.folder_path=folder_path
        self.socketTCP=socketTCP
        self.socketUDP=socketUDP
        self.dict_files_complete=dict_files_complete
        self.dict_files_inBlocks=dict_files_inBlocks
        self.lock=threading.Lock()

        while True:
            with self.lock:
                # Recebe dados do cliente (header tem 18 bytes)
                data,_= self.socketUDP.recvfrom(18)
                header=data.decode().split('|')

                data_length = int(header[1], 16)
                data_message,_= self.socketUDP.recvfrom(data_length)

                # message vai ser um dicionário
                message = json.loads(data_message.decode())

                if header[0]== '0':
                    # Cria uma nova thread para cada pedido de bloco recebido
                    transfer_thread = threading.Thread(target=self.sendBlock, args=(message['filename'],message['block'],
                                                                                    message['client_host']))
                    transfer_thread.daemon=True # termina as threads mal o precesso principal morra
                    transfer_thread.start()

                elif header[0]== '1':        
                    blockReceived,_ = self.socketUDP.recvfrom(message['blockSize'])
                    # Cria uma nova thread para cada bloco recebido
                    transfer_thread = threading.Thread(target=self.saveBlock, args=(message['block'],message['filename'],
                                                                                    blockReceived))
                    transfer_thread.daemon=True # termina as threads mal o precesso principal morra
                    transfer_thread.start()


    def sendBlock(self,filename,block,client_host):
        if filename in self.dict_files_complete:
            file_path = os.path.join(self.folder_path, filename)
            blockRequested = getBlock_inFile(file_path,block)
            trspm.sendBlock(self.socketUDP,client_host,blockRequested,len(blockRequested),block,filename)
        elif filename in self.dict_files_inBlocks:
            fileFolder_path = os.path.join(self.folder_path, filename)
            block_path = os.path.join(fileFolder_path, block) #bloco esta numa pasta com o nome do ficheiro
            blockRequested = file_to_binary(block_path)
            trspm.sendBlock(self.socketUDP,client_host,blockRequested,len(blockRequested),block,filename)


    def saveBlock(self,block,filename,blockReceived):
        fileFolder_path=os.path.join(self.folder_path,filename)
        block_path=os.path.join(fileFolder_path,f'{block}') #bloco ficara guardado na pasta local do seu ficheiro
        binary_to_file(blockReceived,fileFolder_path,block_path)

        #adiciona o bloco transferido ao seu dicionario local
        if filename in self.dict_files_inBlocks:
            self.dict_files_inBlocks[filename].append(block)
        else: 
            self.dict_files_inBlocks[filename]=[block]


        print(self.dict_files_inBlocks)
        # reenvia os seus dicionarios para o Tracker (já com o novo ficheiro transferido)
        tpm.sendDictsFiles(self.socketTCP,self.dict_files_inBlocks,self.dict_files_complete)


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


def binary_to_file(binary_data,fileFolder_path,block_path): #guarda o bloco na sua pasta local
    # Ensure the directory exists
    os.makedirs(fileFolder_path, exist_ok=True)

    with open(block_path, 'wb') as file:
        # Write the binary data to the file
        file.write(binary_data)