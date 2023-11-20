import json

GET_BLOCK = "0"

def getBlock(client_socketUDP,sender_host,block,filename):
    # Envia dados para o servidor
    message = {'client_socketUDP':client_socketUDP,'block':block,'filename':filename}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 18 bytes
    header = GET_BLOCK +"|"+ messageSize_str
    final = header + message_json
    client_socketUDP.sendto(final.encode()) #porta default para sockets udp no nosso protocolo