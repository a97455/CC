import socket

# Configuração do servidor
UDP_IP = "127.0.0.1"  # IP do servidor
UDP_PORT = 5005  # Porta que o servidor está ouvindo

# Criação do soquete UDP
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # Internet/UDP
sock.bind((UDP_IP, UDP_PORT))

# Aguarda por mensagens
while True:
    data, addr = sock.recvfrom(1024)  # buffer size é 1024 bytes
    print("Mensagem recebida:", data)
