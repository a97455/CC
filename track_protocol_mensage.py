import json

START_CONNECTION = "000"
SEND_DICTS_FILES = "001"
GET_FILE = "010"
SEND_DICT_BLOCK_LISTNODES = "011" 
END_CONNECTION = "100"
NO_FILE_COMPLETE = "101"
NEW_BLOCK_LOCALY = "110"

#___________________________Node_Send________________________________________

def startConnection(client_socket,name):
    # Envia dados para o servidor
    message = {'name':name}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 20 bytes
    header = START_CONNECTION +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())


def sendDictsFiles(client_socket,dict_files_inBlocks,dict_files_complete):
    message = {'dict_files_inBlocks' : dict_files_inBlocks, 'dict_files_complete':dict_files_complete}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)
    
    # header ocupa 20 bytes
    header = SEND_DICTS_FILES +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())


def getFile(client_socket,filename):
    # Envia dados para o servidor
    message = {'filename': filename}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 20 bytes
    header = GET_FILE +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())


def newBlockLocaly(client_socket,block,filename):
    # Envia dados para o servidor
    message = {'block':block,'filename':filename}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 20 bytes
    header = NEW_BLOCK_LOCALY +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())


def endConnection(client_socket,name):
    # Envia dados para o servidor
    message = {'name':name}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 20 bytes
    header = END_CONNECTION +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())
    

#___________________________Tracker_Send________________________________________

def sendDictBlockListNodes(client_socket,dict_Block_ListNodes,numBlocks):
    # Envia dados para o no
    message = {'dict_Block_ListNodes': dict_Block_ListNodes,'numBlocks':numBlocks}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 20 bytes
    header = SEND_DICT_BLOCK_LISTNODES +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())


def noFileComplete(client_socket,error):
    # Envia dados para o no
    message = {'error': error}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 20 bytes
    header = NO_FILE_COMPLETE +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())