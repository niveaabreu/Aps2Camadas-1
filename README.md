# Projeto 2 de Camada Física da Computação 
## PROJETO CLIENT-SERVER EM TEMPO REAL 
Implemetação de ações que obedecem uma ordenação temporal real.
Nesse projeto foi construído um código em Python para transmissão (client) e recepção (server) serial com uma resposta do server para o client.


Foram testatos três tipos de casos: O PRIMEIRO sendo o caso de SUCESSO DE TRANSMISSÃO em que ao enviar uma série de comandos para o server ele retorna o tamanho daqueles bytes. Para o SEGUNDO ERRO DE TRANSMISSÃO acontece quando um número é diferente dos comandos enviados. Para o TERCEIRO o Caso de TIME em que mostra a duração de comunicação entre os dois arduinos.


Para utilização (seja com dois computadores ou em um único, neste último caso certifique-se de visualizar as portas), abra em um terminal na pasta server, e digite o abaixo para simular a operação desejadar

```console
 borg@borg:~ python aplicacao_server.py
 Qual caso deseja simular?
        1 - Caso de Sucesso
        2 - Caso de erro de transmissão 
        3 - Caso de timeout

```





Dessa forma, será gerado uma imagem cópia dentro do diretório após o envio da imagem (convertida em bytes) por meio do arduino e salva uma exata cópia na mesma raiz.