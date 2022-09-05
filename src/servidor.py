import socket

#Socket é a combinação de um IP com um número de porta
HOST = '192.168.43.52'
PORT = 9090

def handle_request(request):
    """Trata da requisição"""

    cabecalho = request.split(' ')
        
    try:
        if cabecalho[1] == '/':
            filename = 'index.html'  
        elif cabecalho[1] == '/index.css':
            filename = 'index.css'
        elif cabecalho[1] == '/index.js':
            filename = 'index.js'
        elif cabecalho[1] == '/favicon.ico':
            filename = 'favicon.ico'
    except IndexError:
        print('Posição inválida!')
    
    try:
        fin = open(filename)
        content = fin.read(-1)
        fin.close()

        resposta = 'HTTP/1.1 200 OK\n\n' + content

    except FileNotFoundError:
        resposta = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'

    return resposta




try:
    #Os parâmetros para o método abaixo são: (Família de protocolo, Tipo de protocolo)
    #AF_INET => IP ; SOCK_STREAM => TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Para iniciar o socket no endereço e porta declarados => .bind((endereço, porta))
    s.bind((HOST, PORT))
    
    #Deixa o socket em modo de escuta, à procura de conexões (limitado a 3 conexões)
    s.listen(3)

    print('Esperando a conexão de um cliente...')

    while True:
            #Quando um cliente se conectar, ele deve retornar seu endereço e um socket para comunicação
            (communication_socket, address) = s.accept()

            print(f'Conectado em {address}')

            message = communication_socket.recv(3000).decode()
            print(message)

            response = handle_request(message)
            communication_socket.sendall(response.encode())
            communication_socket.close()

            
except KeyboardInterrupt:
        print('Servidor fechado!')
        s.close()