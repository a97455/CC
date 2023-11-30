import json
import Transfer as trs

GET_BLOCK = "0"
SEND_BLOCK = "1"

def getBlock(client_socketUDP,provider_host,client_host,block,filename,numBlocks,classLock):
    # Envia dados para o servidor
    message = {'client_host':client_host,'block':block,'filename':filename,'numBlocks':numBlocks}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 18 bytes
    header = GET_BLOCK +"|"+ messageSize_str
    final = header + message_json
    
    with classLock:
        client_socketUDP.sendto(final.encode(),(provider_host,9090)) 

def sendBlock(provider_socketUDP,client_host,blockBinary,blockSize,block,filename,numBlocks,classLock):
    checksum = trs.calculate_checksum(blockBinary)

    # Envia dados para o servidor
    message = {'block':block,'blockSize':blockSize,'filename':filename,'numBlocks':numBlocks,'checksum':checksum}
    message_json = json.dumps(message)
    messageSize_str = len(message_json).to_bytes(8,'big').hex().zfill(16) # Convert to hexadecimal string (16 bytes)

    # header ocupa 18 bytes 
    header = SEND_BLOCK +"|"+ messageSize_str
    final = header.encode() + message_json.encode() + blockBinary

    with classLock:
        provider_socketUDP.sendto(final,(client_host,9090))