import socket  
import time    
import sys

class Server:

 def __init__(self, port = 5018):
     self.host = '' #Pega IP
     self.port = port 
     self.www_dir = 'Files' # Diretório
    
 def ativando_servidor(self):
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     self.socket.bind((self.host, self.port)) 
     self._aguardando_conexoes()
          
 def _headers(self,  cod):
     header = ''
     if (cod == 200):
        header = 'HTTP/1.1 200 OK\n'
     elif(cod == 404):
        header = 'HTTP/1.1 404 Not Found\n'
     data_atual = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) 
     header += 'Data: ' + data_atual +'\n'
     header += 'Servidor: HTTP-Server\n'
     header += 'Conexao: close\n\n'
     return header

 def _aguardando_conexoes(self):
     while True:
         print ("Aguardando nova conexão")
         self.socket.listen(3)
         
         conn, addr = self.socket.accept()
         # conn - socket to client
         # addr - clients address
    
         dados = conn.recv(1024) #Recebe dados
         nome_arquivo = bytes.decode(dados) 
         
         metodo = nome_arquivo.split(' ')[0]
         
         if (metodo == 'GET') | (metodo == 'HEAD'):
             requisicao = nome_arquivo.split(' ')
             requisicao = requisicao[1]
             requisicao = requisicao.split('?')[0]  
             
             requisicao = self.www_dir + requisicao
 
             try:
                 arquivo = open(requisicao,'rb')
                 if (metodo == 'GET'):
                     resposta = arquivo.read()                        
                 arquivo.close()
                 
                 headers = self._headers( 200)          
                 
             except Exception as e: 
                 headers = self._headers( 404)
             
                 if (metodo == 'GET'):
                    resposta = b"<html><body><p>Error 404: File not found</p><p>Servidor HTTP</p></body></html>"  
                 
             resposta_servidor =  headers.encode() 
             if (metodo == 'GET'):
                 resposta_servidor +=  resposta

             conn.send(resposta_servidor)
             print ("Fechando conexão com o cliente")
             conn.close()

print ("Iniciando servidor")
s = Server(5018)  
s.ativando_servidor() 
s.socket.shutdown(socket.SHUT_RDWR)    

