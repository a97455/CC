import json

START_CONNECTION = "000"
FILES_DICT_NODE = "001"
GET_FILE = "010"
FILES_LIST_TRACKER = "011" 
FILES_LIST_INSERT = "100"
FILES_LIST_DELETE = "101"
END_CONNECTION = "110"

#___________________________Node________________________________________

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
    message = {'node_name' : node_name, 'filesDictNode' : dict_files}
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

#___________________________Tracker________________________________________

def filesListTracker(server_socket,node_name,list_blocks):
    # Envia dados para o no
    message = {'node_name': node_name,'list_blocks': list_blocks}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 20 bytes
    header = FILES_LIST_TRACKER +"|"+ messageSize_str
    final = header + message_json
    server_socket.send(final.encode())