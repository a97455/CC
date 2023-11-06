import json

START_CONNECTION = "000"
FILES_DICT_NODE = "001"
GET_FILE = "010"
FILES_LIST_TRACKER = "011" 
END_CONNECTION = "100"

#___________________________Node_Send________________________________________

def startConnection(client_socket,node_name):
    # Envia dados para o servidor
    message = {'node_name': node_name}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 20 bytes
    header = START_CONNECTION +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())

def filesDictNode(client_socket,node_name,dict_files):
    message = {'node_name' : node_name, 'dict_files' : dict_files}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16)  
    
    # header ocupa 20 bytes
    header = FILES_DICT_NODE +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())

def getFile(client_socket,filename):
    # Envia dados para o servidor
    message = {'filename': filename}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 20 bytes
    header = GET_FILE +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())

def endConnection(client_socket,node_name):
    # Envia dados para o servidor
    message = {'node_name': node_name}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 20 bytes
    header = END_CONNECTION +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())

#___________________________Tracker_Send________________________________________

def filesListTracker(client_socket,dict_nodeAddress_listBlocks):
    # Envia dados para o no
    message = {'dict_nodeAddress_listBlocks': dict_nodeAddress_listBlocks}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 20 bytes
    header = FILES_LIST_TRACKER +"|"+ messageSize_str
    final = header + message_json
    client_socket.send(final.encode())