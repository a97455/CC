import json

START_CONNECTION = "000".strip()
FILES_DICT_NODE = "001".strip()
GET_FILE = "010"
FILES_LIST_TRACKER = "011" 
FILES_LIST_INSERT = "100"
FILES_LIST_DELETE = "101"
END_CONNECTION = "110"

def startConnection(client_socket,node_name):
    # Envia dados para o servidor
    message = {'node_name': node_name}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # header ocupa 39 bytes (ao transformar em str o messageSize_in_bytes ocupa 35 caracteres, ou seja, 35 bytes)
    # TODO: Acho que é o facto de ter START_CONNECTION e não "000", é a única coisa diferente nos 2
    messageSize_str = str(messageSize_in_bytes)
    messageSize_same = messageSize_str.zfill(8)
    print(len(messageSize_same))
    header = START_CONNECTION +"|"+ str(messageSize_in_bytes)
    print(len(header))
    final = header + message_json
    client_socket.send(final.encode())

def filesDictNode(client_socket,node_name,dict_files):
    # Mudei a message para um dicionário para não termos de tratar tudo em strings e splits do outro lado
    # Quando recebemos a message já sabemos que tipo de message é então acedemos diretamente aos campos que queremos pelo nome
    # Ex: linha 48/49 tracker
    message = {'node_name' : node_name, 'filesDictNode' : json.dumps(dict_files)}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')


    # header ocupa 36 bytes, não sei porque é que o tamanho é diferente
    # TODO: Acho que é o facto de ter FILES_DICT_NODE e não "001", é a única coisa diferente nos 2
    messageSize_str = messageSize_in_bytes.hex()  # Convert bytes to hexadecimal string
    messageSize_str = messageSize_str.zfill(16)
    print(len(messageSize_str))
    header = FILES_DICT_NODE +"|"+ messageSize_str
    print(len(header))
    final = header + message_json
    client_socket.send(final.encode())