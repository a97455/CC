import json

START_CONNECTION = "000"
FILES_DICT_NODE = "001"
GET_FILE = "010"
FILES_LIST_TRACKER = "011" 
FILES_LIST_INSERT = "100"
FILES_LIST_DELETE = "101"
END_CONNECTION = "110"

def startConnection(client_socket,node_name):
    # Envia dados para o servidor
    message = node_name
    messageSize_in_bytes = len(message).to_bytes(8,'big')

    # header ocupa 39 bytes (ao transformar em str o messageSize_in_bytes ocupa 35 caracteres, ou seja, 35 bytes)
    header = START_CONNECTION +"|"+ str(messageSize_in_bytes) 
    final = header + message
    client_socket.send(final.encode())

def filesDictNode(client_socket,node_name,dict_files):
    message = node_name + "|" + json.dumps(dict_files)
    messageSize_in_bytes = len(message).to_bytes(8,'big')

    # header ocupa 39 bytes (ao transformar em str o messageSize_in_bytes ocupa 35 caracteres, ou seja, 35 bytes)
    header = FILES_DICT_NODE +"|"+ str(messageSize_in_bytes) 
    final = header + message
    client_socket.send(message.encode())