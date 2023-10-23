import json

START_CONNECTION = "000"
FILES_DICT_NODE = "001"
GET_FILE = "010"
FILES_LIST_TRACKER = "011" # List (???)
FILES_LIST_INSERT = "100"
FILES_LIST_DELETE = "101"
END_CONNECTION = "110"

def startConnection(client_socket,node_name):
    # Envia dados para o servidor
    message = node_name
    message_in_bytes = len(message).to_bytes(4,'big')
    header = START_CONNECTION +"|"+ str(message_in_bytes) # 8 bytes
    final = header + message
    client_socket.send(final.encode())

def filesDictNode(client_socket,node_name,dict_files):
    message = node_name + "|" + json.dumps(dict_files)
    header = "001" + message
    client_socket.send(message.encode())