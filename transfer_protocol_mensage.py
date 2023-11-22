import json

GET_BLOCK = "0"

def getBlock(client_socketUDP,client_host,provider_host,block,filename):
    # Envia dados para o servidor
    message = {'client_host':client_host,'block':block,'filename':filename}
    message_json = json.dumps(message)
    messageSize_in_bytes = len(message_json).to_bytes(8,'big')

    # messageSize_str ocupa 16 bytes
    messageSize_str = messageSize_in_bytes.hex().zfill(16) # Convert bytes to hexadecimal string

    # header ocupa 18 bytes
    header = GET_BLOCK +"|"+ messageSize_str
    client_socketUDP.sendto(header.encode(),(provider_host,9090)) #envia o header
    client_socketUDP.sendto(message_json.encode(),(provider_host,9090)) #envia a camada de dados