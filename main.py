from track_protocol_node import Node

def main():
    # Configuração do servidor
    host = '127.0.0.17'
    port = 12345

    Node("node1",host,port)
    Node("node2",host,port)

if __name__ == "__main__":
    main()
