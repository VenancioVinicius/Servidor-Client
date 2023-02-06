import socket

if __name__ == '__main__':
    HOST = input('Digite o endereco do servidor:') 
    PORT = input('Digite a porta do servidor:')
    BUFSIZ = 4096
    ADDR = (HOST,int(PORT))

    client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_sock.connect(ADDR)

    continua=True
    try:
        while continua:
            dados = input("Digite uma mensagem:")
            client_sock.send(dados.encode('utf-8'))
            if(dados == 'END'):
                continua=False
            else:
                resposta = client_sock.recv(BUFSIZ)
                resposta = resposta.decode('utf-8')
                print(resposta)
                continuar = input("Continuar[s/n]?")
                if(continuar.lower()=="n"):
                    client_sock.send(b"END")
                    continua=False

    except KeyboardInterrupt:
        print("Ok, saindo!!")

    client_sock.close()    
    