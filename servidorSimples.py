import os
import socket

HOST ='localhost'
PORT = 12346
BUFSIZ = 1024
ADDR = (HOST, PORT)


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    server_socket.setsockopt( socket.SOL_SOCKET,socket.SO_REUSEADDR, 1 )
    while True:
        print('Server waiting for connection...')
        client_sock, addr = server_socket.accept()
        print('Client connected from: ', addr)
        while True:
            data = client_sock.recv(BUFSIZ)
            data = data.decode("utf-8")
            print(type(data))
            if not data or data == 'END':
                break
            # if data.startswith("SOMA"): #SOMA 1 2
            #     partes = data.split(" ")
            #     op1 = float(partes[1])
            #     op2 = float(partes[2])
            #     res = str(op1 + op2)
            #     client_sock.send(res.encode('utf-8'))
            if data.startswith("LISTAR"):
                path = 'textos'
                lista = str(os.listdir(path))
                print(lista)
                lista = "\n" + lista + "\n"
                client_sock.send(lista.encode('utf-8'))
                # for word in lista:
                #     result = word.encode('utf-8')
                #     print(result)
                #     client_sock.send(result)
                    
            if data.startswith("CONTEM"):
                partes = data.split(" ")
                palavra = str(partes[1])
                arquivo = str(partes[2])
                path = 'textos'
                print(palavra + ", " + arquivo)
                
                os.chdir(path)
                try:
                    arq = open(arquivo)
                    linhas = arq.read().splitlines()
                    validacao = 0
                    for linha in linhas:
                        print(linha)
                        if (linha == palavra):
                            contem = ("\nO arquivo " + arquivo + " contem a palavra " + palavra + ".\n")
                            validacao = 1
                    
                    if(validacao == 0):
                        contem = "\n__ERRO__\n"
                    os.chdir("..")
                    client_sock.send(contem.encode('utf-8'))
                except:
                    erroMensagem = "ERR_NAO_EXISTE"
                    os.chdir("..")
                    client_sock.send(erroMensagem.encode('utf-8'))
                
            if data.startswith("CONTAR"):
                partes = data.split(" ")
                palavra = str(partes[1])
                arquivo = str(partes[2])
                path = 'textos'
                print(palavra + ", " + arquivo)
                
                os.chdir(path)
                
                try:
                    arq = open(arquivo)
                    linhas = arq.read().splitlines()
                    validacao = 0
                    for linha in linhas:
                        print(linha)
                        if (linha == palavra):
                            validacao = 1 + validacao
                    
                    if(validacao == 0):
                        contem = "\n__ERRO__\n"
                        
                    validacao = str(validacao)
                    contem = ("\nO arquivo " + arquivo + " contem a palavra " + palavra + " " + validacao +" vezes.\n")
                    os.chdir("..")
                    client_sock.send(contem.encode('utf-8'))
                except:
                    erroMensagem = "ERR_NAO_EXISTE"
                    os.chdir("..")
                    client_sock.send(erroMensagem.encode('utf-8'))

        client_sock.close()
    server_socket.close()