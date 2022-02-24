#!/usr/bin/env python3
#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import sys
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/tty"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

imageR = "./imgs/image.png"
imageW = "./imgs/recebida.png"


def random_bytes():
    random.seed(time.time())
    lista = [bytes([0,255,0,255]),bytes([0,255,255,0]),bytes([255]),bytes([0]),bytes([255,0]),bytes([0,255])]*5
    x = random.randint(10,30)
    random.shuffle(lista)
    lista=lista[:x]
    out = []
    for byte in lista:
        out.append(byte)
        out.append(bytes([13*16]))

    #start = [0xAA.to_bytes(1, byteorder='big')]
    final=[0xEE.to_bytes(1, byteorder='big')]
    lista = lista+final
    l =b''.join(lista) # Mensagem a ser enviada
    
    return l, x


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        bytes_to_send, size = random_bytes()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("-------------------------")
        print("Comunicação aberta!")
        print("-------------------------")
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        #print(f" - {imageR}")

        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        inicio_envio = time.time()  #inicio do envio
        print(f"Enviando: \n {bytes_to_send} do tipo {type(bytes_to_send)}")
        print(f"Tamanho enviado:{size}")
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
          
        
        print("-------------------------")
        print("Iniciando Transmissão de dados")
        print("-------------------------")
        com1.sendData(np.asarray(bytes_to_send))
       
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus() # retorna o que foi escrito na transmissao, caso o buffer seja enviado, assume status 0, caso nao recebe a quantidade de bytes enviados no processo
        fim_envio = time.time()  #fim do envio
        tempo_envio = fim_envio - inicio_envio
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        print("-------------------------")
        print("Iniciando a recepção")
        print("-------------------------")
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
        inicio_recep = time.time()  #inicio do recepção
        #acesso aos bytes recebidos
        rxBuffer, nRx = com1.getData(1)

        if int.from_bytes(rxBuffer, 'big') == size:
            print("Dados enviados adequadamente")
        else:
            print(f"Algum erro: \n Tamanho enviado:{size}\nRecebido:{int.from_bytes(rxBuffer, 'big')}")
    
        print("recebeu {}" .format(rxBuffer))

            
        fim_recep = time.time()  #fim do recepção
        tempo_recep = fim_recep - inicio_recep
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")

        print(f"Tempo decorrido durante envio: {tempo_envio:.2f} s")
        print(f"Tempo decorrido durante recepção: {tempo_recep:.2f} s")
        print(f"Tempo total decorrido: {tempo_recep+tempo_envio:.2f} s")
        print("-------------------------")
        print(f"Baudrate de referência: {com1.fisica.baudrate}")

        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
