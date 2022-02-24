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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/tty"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

imageR = "./imgs/image.png"
imageW = "./imgs/recebida.png"

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna

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
        x = len([bytes([0,255]),bytes([0]),bytes([15]),bytes([16*15]),bytes([255,0]),bytes([255])]*5)
        out =b''
        size=0
        while True:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer == b'\xee':
                print("Leitura Encerrada!")
                break
            elif rxBuffer == b'\xd0':
                size+=1
            else:
                out+=rxBuffer
            

        print("recebeu {}" .format(out))
        print(f"tamanho: {size}")

        print("------------")
        print("Enviando dados de volta")
        volta = size.to_bytes(1, byteorder='big')
        com1.sendData(np.asarray(volta))
        txSize = com1.tx.getStatus()
  
            
        fim_recep = time.time()  #fim do recepção
        tempo_recep = fim_recep - inicio_recep
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")

        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
