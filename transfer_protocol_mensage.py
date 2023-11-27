import json

GET_BLOCK = "0"
SEND_BLOCK = "1"

def getBlock(client_socketUDP,provider_host,client_host,block,filename,classLock):
    # Envia dados para o servidor
    message = {'client_host':client_host,'block':block,'filename':filename}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 18 bytes
    header = GET_BLOCK +"|"+ messageSize_str
    final = header + message_json
    
    with classLock:
        client_socketUDP.sendto(final.encode(),(provider_host,9090)) 

def sendBlock(provider_socketUDP,client_host,blocoBinario,blockSize,block,filename,classLock):
    # Envia dados para o servidor
    message = {'block':block,'blockSize':blockSize,'filename':filename}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 18 bytes
    header = SEND_BLOCK +"|"+ messageSize_str
    final = header.encode() + message_json.encode() + blocoBinario

    with classLock:
        provider_socketUDP.sendto(final,(client_host,9090))