import threading
import hashlib
import json
import os
import track_protocol_mensage as tpm
import transfer_protocol_mensage as trspm

class Transfer:
    def __init__(self,folder_path,socketTCP,socketUDP,dict_files_complete,dict_files_inBlocks,classLock):
        self.folder_path=folder_path
        self.socketTCP=socketTCP
        self.socketUDP=socketUDP
        self.dict_files_complete=dict_files_complete
        self.dict_files_inBlocks=dict_files_inBlocks
        self.saveBlockLock = threading.Lock()

        while True:
            buffer, _ = socketUDP.recvfrom(2048) 

            while buffer:
                data_header,buffer = divideData(buffer,18) #header size = 18 
                header=data_header.decode().split('|')
                data_length = int(header[1], 16)
                data_message, buffer = divideData(buffer,data_length)

                # message vai ser um dicionário
                message = json.loads(data_message.decode())

                if header[0]== '0':
                    # Cria uma nova thread para cada pedido de bloco recebido, enviando esse mesmo bloco
                    transfer_thread = threading.Thread(target=self.sendBlock, args=(message['filename'],message['block'],message['numBlocks'],
                                                                                    message['client_host'],classLock))
                    transfer_thread.daemon=True # termina as threads mal o precesso principal morra
                    transfer_thread.start()

                elif header[0]== '1':        
                    blockReceived,buffer = divideData(buffer,message['blockSize'])
                    if message['checksum'] == calculate_checksum(blockReceived):
                        # Cria uma nova thread para cada bloco recebido
                        transfer_thread = threading.Thread(target=self.saveBlock, args=(message['block'],message['filename'],message['numBlocks'],
                                                                                        blockReceived,self.saveBlockLock))
                        transfer_thread.daemon=True # termina as threads mal o precesso principal morra
                        transfer_thread.start()


    def sendBlock(self,filename,block,numBlocks,client_host,classLock):
        if filename in self.dict_files_inBlocks:
            fileFolder_path = os.path.join(self.folder_path, filename)
            blockFolder_path=os.path.join(fileFolder_path,"blocks") #path to the folder containing all the blocks from that file
            block_path = os.path.join(blockFolder_path, block) 
            blockRequested = file_to_binary(block_path) 
            trspm.sendBlock(self.socketUDP,client_host,blockRequested,len(blockRequested),block,filename,numBlocks,classLock)
        elif filename in self.dict_files_complete:
            file_path = os.path.join(self.folder_path, filename)
            blockRequested = getBlock_inFile(file_path,block)
            trspm.sendBlock(self.socketUDP,client_host,blockRequested,len(blockRequested),block,filename,numBlocks,classLock)


    def saveBlock(self,block,filename,numBlocks,blockReceived,lock):
        fileFolder_path=os.path.join(self.folder_path,filename) 
        blockFolder_path=os.path.join(fileFolder_path,"blocks") #path to the folder containing all the blocks from that file
        block_path=os.path.join(blockFolder_path,f'{block}')
        binary_to_file(blockReceived,fileFolder_path,blockFolder_path,block_path,lock)

        if block not in self.dict_files_inBlocks[filename]:
            self.dict_files_inBlocks[filename].append(block)

        if len(self.dict_files_inBlocks[filename])==numBlocks:
            create_combined_file(blockFolder_path,fileFolder_path)

        # reenvia os seus dicionarios para o Tracker (já com o novo ficheiro transferido)
        tpm.newBlockLocaly(self.socketTCP,block,filename)


def divideData(data,n): #retrives the first n bytes from the buffer
    header = data[:n]
    rest_of_data= data[n:]

    return header, rest_of_data


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


def binary_to_file(binary_data,fileFolder_path,blockFolder_path,block_path,lock):
    with lock:
        # Ensure the directories exists
        os.makedirs(fileFolder_path, exist_ok=True)
        os.makedirs(blockFolder_path, exist_ok=True)

    with open(block_path, 'wb') as file:
        # Write the binary data to the file
        file.write(binary_data)


def create_combined_file(blockFolder_path,fileFolder_path):
    # Get a list of all files in the blockFolder_path
    blocks = [block for block in os.listdir(blockFolder_path) if os.path.isfile(os.path.join(blockFolder_path, block))]
    
    # Sort the blocks based on their names (assuming names are numbers)
    blocks.sort(key=lambda x: int(x))

    # Create a new file with the folder name
    output_file_path = os.path.join(fileFolder_path, f"{os.path.basename(fileFolder_path)}")

    # Open the new file in binary write mode to handle bytes
    with open(output_file_path, 'wb') as output_file:
        # Iterate through each file, read its content, and write to the output file
        for block in blocks:
            block_path = os.path.join(blockFolder_path, block)
            with open(block_path, 'rb') as input_file:
                # Read the content as bytes
                content = input_file.read()
                # Write the content to the output file
                output_file.write(content)


def calculate_checksum(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()