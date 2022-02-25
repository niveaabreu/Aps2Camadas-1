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
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        caso = input("""Qual o caso deseja simular?
        1 - Caso de Sucesso de Transmissão
        2 - Caso de erro de transmissão
        3 - Caso de timeout\n """)
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("-------------------------")
        print("Esperando o recebimento de dados...")
        print("-------------------------")

        inicio_recep = time.time()  #inicio do recepção

        out =b''
        size=0

        while True:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer == b'\xc3':
                print("\n------------")
                print("Leitura Encerrada!")
                print("------------")
                break
            elif rxBuffer == b'\xd0' and int(caso)==1:
                print(f"\nComando {size+1}:")
                size+=1
            else:
                if int(caso)==1:
                    print(f"{rxBuffer}", end="")
                out+=rxBuffer
            # rxBuffer, nRx = com1.getData(size_to_read)
            # if rxBuffer[-1] == b'\xc3':
            #     print("\n------------")
            #     print("Leitura Encerrada!")
            #     print("------------")
            #     break
            # size+=int.from_bytes(rxBuffer, 'big')
            # size_to_read=int.from_bytes(rxBuffer, 'big') + 1
            # out+=rxBuffer
        #out = "".join(out.split(b'\xd0'))
        if int(caso)==1:
            print("\n------------")
            print("recebeu {}" .format(out))
            print(f"\nQuantidade de comandos recebidos: {size}")
            print("------------")

        print("\n------------")
        print("Enviando dados de volta para Client..")
        print("------------")
        volta = size.to_bytes(1, byteorder='big')
        if int(caso)==1:
            com1.sendData(np.asarray(volta))
        elif int(caso)==2:
            com1.sendData(np.asarray(int(3).to_bytes(1, byteorder='big')))
        else:
            print("\nCASO DE TIMEOUT")
            time.sleep(10)
        txSize = com1.tx.getStatus()
            
        fim_recep = time.time()  #fim do recepção
        tempo_recep = fim_recep - inicio_recep
        # Encerra comunicação
        print("\n-------------------------")
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
