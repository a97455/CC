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
    
    with classLock:
        client_socketUDP.sendto(header.encode(),(provider_host,9090)) #envia o header
        client_socketUDP.sendto(message_json.encode(),(provider_host,9090)) #envia a camada de dados

def sendBlock(provider_socketUDP,client_host,blocoBinario,blockSize,block,filename,classLock):
    # Envia dados para o servidor
    message = {'block':block,'blockSize':blockSize,'filename':filename}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 18 bytes
    header = SEND_BLOCK +"|"+ messageSize_str

    with classLock:
        provider_socketUDP.sendto(header.encode(),(client_host,9090)) #envia o header
        provider_socketUDP.sendto(message_json.encode(),(client_host,9090)) #envia a camada de dados
        provider_socketUDP.sendto(blocoBinario,(client_host,9090)) #envia o bloco em binario