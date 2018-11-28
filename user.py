#!/usr/bin/env python

import socket
import sys
import getopt
import os
import signal

BUFFER_SIZE = 1024

CS_NAME = socket.gethostname()
CS_PORT = 58065

nrArguments = len(sys.argv)

def signal_handler(signal, frame):
    print 'pressionou CTRL-C\n'
    s.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


if nrArguments == 3:
    if sys.argv[1] == '-n':
        CS_NAME = str(sys.argv[2])
    elif sys.argv[1] == '-p':
        CS_PORT = int(sys.argv[2])
elif nrArguments == 5:
    CS_NAME = str(sys.argv[2])
    CS_PORT = int(sys.argv[4])

#---------------------------------------------------------------------------------------
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CS_NAME, CS_PORT))

    MESSAGE = raw_input('>')
    lista = MESSAGE.split()
    if MESSAGE == 'exit':
        break
    elif MESSAGE == 'list':
        MESSAGE = 'LST\n'
    elif lista[0] == 'request':
        f = open(str(lista[2]) , 'r')
        TEXTO = f.read()
        f.close()

        size = os.path.getsize(lista[2])
        MESSAGE = 'REQ ' + lista[1]+ ' ' + str(size) + ' ' + TEXTO + '\n'

    else:
        print "Comando desconhecido"

    s.send(MESSAGE) #Envio da mensagem para o CS
    data = s.recv(BUFFER_SIZE) #resposta do CS

    dados = MESSAGE.split()
    aux = data.split("\n")
    aux_espacos = data.split()

    if data != '' and aux[0] != 'REP EOF':
        if MESSAGE == 'LST\n':

            aux = data.split()
            if len(aux) - int(aux[1]) == 1:
                answer = s.recv(BUFFER_SIZE)
                data += answer
            aux = data.split()

            for i in range(0, int(aux[1])):
                c = i + 2
                if aux[c] == 'WCT':
                    print str(i + 1) + '- ' + aux[c] + ' - word count\n'
                elif aux[c] == 'FLW':
                    print str(i + 1) + '- ' + aux[c] + ' - find longest word\n'
                elif aux[c] == 'UPP':
                    print str(i + 1) + '- ' + aux[c] + ' - convert to upper case\n'
                elif aux[c] == 'LOW':
                    print str(i + 1) + '- ' + aux[c] + ' - convert to lower case\n'

        elif dados[0] == 'REQ':
            aux = data.split("\n")
            aux_first = aux[0].split()
            if len(aux_espacos) <= 3:
                answer = s.recv(BUFFER_SIZE)
                data += answer
            aux = data.split("\n")
            aux_first = aux[0].split()

            if dados[1] == 'WCT':
                print 'Number of Words: ' + str(aux_first[3])

            elif dados[1] == 'FLW':
                print 'Longest Word: ' + str(aux_first[3])

            elif dados[1] == 'UPP':
                print str(os.path.getsize(lista[2])) + ' Bytes to transmit'
                texto = ''
                for i in range(3, len(aux_first)):
                    texto += aux_first[i] + ' '
                texto += '\n'
                for i in range(1, len(aux) - 2):
                    if i == len(aux)-3:
                        texto += aux[i]
                    else:
                        texto += aux[i] + '\n'

                f = open(str(lista[2]) , 'w')
                f.write(texto)
                f.close()
                print 'received file ' + str(lista[2])
                print str(aux_first[2]) + ' Bytes'

            elif dados[1] == 'LOW':

                print str(os.path.getsize(lista[2])) + ' Bytes to transmit'
                texto = ''
                for i in range(3, len(aux_first)):
                    texto += aux_first[i] + ' '
                texto += '\n'
                for i in range(1, len(aux) - 2):
                    if i == len(aux)-3:
                        texto += aux[i]
                    else:
                        texto += aux[i] + '\n'
                f = open(str(lista[2]) , 'w')
                f.write(texto)
                f.close()

                print 'received file ' + str(lista[2])
                print str(aux_first[2]) + ' Bytes'
    else:
        print "REP EOF\n"

s.close()
