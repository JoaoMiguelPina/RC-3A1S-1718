#!/usr/bin/env python

import socket
import sys
import os
import signal
import select


numberOfWorkingServers = 0

IP = socket.gethostname()
CS_PORT = 58065


BUFFER_SIZE = 1024
CONTADOR = 0

def signal_handler(signal, frame):
    print 'pressionou CTRL-C\n'
    numberOfWorkingServers = 0
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def chunks(input, size):
    input_size = len(input)
    slice_size = input_size / size
    remain = input_size % size
    result = []
    iterator = iter(input)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(iterator.next())
        if remain:
            result[i].append(iterator.next())
            remain -= 1
    return result

FLAG_WCT = False
FLAG_UPP = False
FLAG_LOW = False
FLAG_FLW = False


nrArguments = len(sys.argv)

if nrArguments == 3:
    CS_PORT = int(sys.argv[2])

#----------------------------------------------------------
pid = os.fork()

if pid == 0:

    fptc = open('file_processing_tasks.txt', 'w')
    fptc.close()

    while True:



        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #conexao UDP para recebermos do WS
        sock.bind((IP, CS_PORT))
        data, addr = sock.recvfrom(1024)
        mensagemRecebida = data.split()
        if mensagemRecebida[0] == 'REG':
            if numberOfWorkingServers < 10:
                fptc = open('file_processing_tasks.txt', 'a')
                data = ''
                for i in range(1, len(mensagemRecebida)):
                    data = data + mensagemRecebida[i] + ' '
                data = data + '\n'
                fptc.write(data)
                fptc.close()

                sock.sendto('OK', (addr[0], int(addr[1])))
                numberOfWorkingServers = numberOfWorkingServers + 1
                sock.close()
            elif numberOfWorkingServers >= 10:
                sock.sendto('NOK', (addr[0], int(addr[1])))
                sock.close()
            else:
                sock.sendto('ERR', (addr[0], int(addr[1])))
                sock.close()



        elif mensagemRecebida[0] == 'UNR':

            fptc = open('file_processing_tasks.txt', 'r')
            linhas = fptc.readlines()
            fptc.close()
            fptc = open('file_processing_tasks.txt', 'w')
            for linha in linhas:
                lista = linha.split()
                if lista[-1] != mensagemRecebida[-1] or lista[-2] != mensagemRecebida[-2]:
                    fptc.write(linha)
            sock.sendto('OK', (addr[0], int(addr[1])))
            fptc.close()
            sock.close()
            numberOfWorkingServers = numberOfWorkingServers - 1





elif pid < 0:
    print 'Erro no Fork'

else:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conexao para receber informacao do USER
    s.bind((IP, CS_PORT))
    s.listen(1)


    while True:

        conn, addr = s.accept()

        if not os.path.exists("input_files"):
            os.makedirs("input_files")

        data = conn.recv(BUFFER_SIZE)


        lista_data_n = data.split('\n')
        lista_data = lista_data_n[0].split()
        if lista_data[0] == 'LST':

            newpid = os.fork()
            if newpid == 0:
                f1 = open('file_processing_tasks.txt', 'r')
                fileProcessingT = f1.readlines()
                f1.close()
                message_to_send = ''
                N_PTC = 0
                FLAG_WCT = False
                FLAG_UPP = False
                FLAG_LOW = False
                FLAG_FLW = False
                for line in fileProcessingT:
                    palavras = line.split()
                    for palavra in range(0, len(palavras)):
                        if palavras[palavra] == 'WCT' and FLAG_WCT == False:
                            message_to_send = message_to_send + ' WCT'
                            FLAG_WCT = True
                            N_PTC = N_PTC + 1
                        elif palavras[palavra] == 'UPP' and FLAG_UPP == False:
                            message_to_send = message_to_send + ' UPP'
                            FLAG_UPP = True
                            N_PTC = N_PTC + 1
                        elif palavras[palavra] == 'LOW' and FLAG_LOW == False:
                            message_to_send = message_to_send + ' LOW'
                            FLAG_LOW = True
                            N_PTC = N_PTC + 1
                        elif palavras[palavra] == 'FLW' and FLAG_FLW == False:
                            message_to_send = message_to_send + ' FLW'
                            FLAG_FLW = True
                            N_PTC = N_PTC + 1
                message_to_send = 'FPT ' + str(N_PTC) + message_to_send
                conn.send(message_to_send)
                conn.close()


            elif newpid < 0:
                print "Erro no fork"



        elif lista_data[0] == 'REQ':


            newpid = os.fork()
            texto_ficheiro = ''

            if newpid == 0:

                filename = str(CONTADOR)*5
                f = open(os.path.join('input_files', filename + ".txt"), 'w')

                texto_ficheiro = ''
                for i in range(3, len(lista_data)):
                    texto_ficheiro += lista_data[i] + ' '
                texto_ficheiro += '\n'
                for i in range(1, len(lista_data_n)):
                    texto_ficheiro += lista_data_n[i] + '\n'


                f.write(texto_ficheiro)
                f.close()

                f1 = open('file_processing_tasks.txt', 'r')
                fileProcessingT = f1.readlines()
                f1.close()

                NR_WCT = 0
                NR_FLW = 0
                NR_UPP = 0
                NR_LOW = 0

                for line in fileProcessingT:
                    palavras = line.split()
                    for palavra in range(0, len(palavras)):
                        if palavras[palavra] == 'WCT':
                            NR_WCT += 1
                        elif palavras[palavra] == 'UPP':
                            NR_UPP += 1
                        elif palavras[palavra] == 'LOW':
                            NR_LOW += 1
                        elif palavras[palavra] == 'FLW':
                            NR_FLW += 1

               	f_input = open(os.path.join('input_files', filename + ".txt"), "r")
               	texto_ficheiro = f_input.readlines()
               	f_input.close()
                numeroLinhas = len(texto_ficheiro)

               	i_wct = 0
                i_flw = 0
                i_upp = 0
                i_low = 0

                if lista_data[1] == 'WCT':

                    if NR_WCT == 0:
                        conn.send("REP EOF\n")

                    else:
                        lista_final = chunks(texto_ficheiro, NR_WCT)
                        lista_file_names = []

                        for i in range(0, NR_WCT):
                            filenameAux = filename + str(i)*3
                            f = open(os.path.join('input_files', filenameAux + ".txt"), 'w')
                            lista_file_names.append(filenameAux)
                            for j in range(0, len(lista_final[i])):
                                f.write(lista_final[i][j])
                        f.close()
                        conta_final = 0
                        for line in fileProcessingT:
                    	   palavras = line.split()
                           for palavra in range(0, len(palavras)):
                               if palavras[palavra] == 'WCT':
                                    sockWS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket para enviar para o WS o pedido do USER
                                    sockWS.connect((str(palavras[-2]), int(palavras[-1])))

                                    mensagem = 'WRQ WCT ' + str(lista_file_names[i_wct]) + ' ' + str(os.path.getsize(os.path.join('input_files', lista_file_names[i_wct] + '.txt'))) + ' '

                                    for x in range(0,len(lista_final[i_wct])):
                                        mensagem = mensagem + str(lista_final[i_wct][x])


                                    sockWS.send(mensagem)
                                    feedback = sockWS.recv(BUFFER_SIZE)
                                    splited_feedback = feedback.split()
                                    conta_final = conta_final + int(splited_feedback[3]) #conta final do WCT

                                    #sockWS.shutdown(socket.SHUT_RDWR)
                                    sockWS.close()
                                    os.remove(str(os.path.join('input_files', lista_file_names[i_wct] + '.txt')))
                                    i_wct += 1
                        mensagem_final = 'REP R ' + str(os.path.getsize(os.path.join('input_files', filename + '.txt'))) + ' ' + str(conta_final)


                        conn.send(mensagem_final)
                        conn.close()

                elif lista_data[1] == 'FLW':

                    if NR_FLW == 0:
                        conn.send("REP EOF")
                        conn.close()

                    else:
                        lista_final = chunks(texto_ficheiro, NR_FLW)
                        lista_file_names = []

                        for i in range(0, NR_FLW): #ciclo para criar todos os ficheiros fragmentais
                            filenameAux = filename + str(i)*3
                            f = open(os.path.join('input_files', filenameAux + ".txt"), 'w')
                            lista_file_names.append(filenameAux)
                            for j in range(0, len(lista_final[i])):
                                f.write(lista_final[i][j])
                            f.close()
                        palavra_final = ''
                        for line in fileProcessingT:
                            palavras = line.split()
                            for palavra in range(0, len(palavras)):
                                if palavras[palavra] == 'FLW':
                                    sockWS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket para enviar para o WS o pedido do USER
                                    sockWS.connect((str(palavras[-2]), int(palavras[-1])))
                                    mensagem = 'WRQ FLW ' + str(lista_file_names[i_flw]) + ' ' + str(os.path.getsize(os.path.join('input_files', lista_file_names[i_flw] + '.txt'))) + ' '

                                    for x in range(0,len(lista_final[i_flw])):
                                        mensagem = mensagem + str(lista_final[i_flw][x])
                                    sockWS.send(mensagem)
                                    feedback = sockWS.recv(BUFFER_SIZE)
                                    splited_feedback = feedback.split()
                                    if len( splited_feedback[3]) > len(palavra_final):
                                        palavra_final = splited_feedback[3]
                                    #sockWS.shutdown(socket.SHUT_RDWR)
                                    sockWS.close()
                                    os.remove(str(os.path.join('input_files', lista_file_names[i_flw] + '.txt')))
                                    i_flw += 1
                        mensagem_final = 'REP R ' + str(os.path.getsize(os.path.join('input_files', filename + '.txt'))) + ' ' + palavra_final
                        conn.send(mensagem_final)
                        conn.close()

                elif lista_data[1] == 'UPP':
                    if NR_UPP == 0:
                        conn.send("REP EOF")
                        conn.close()

                    else:
                        lista_final = chunks(texto_ficheiro, NR_UPP)
                        lista_file_names = []

                        for i in range(0, NR_UPP): #ciclo para criar todos os ficheiros fragmentais
                            filenameAux = filename + str(i)*3
                            f = open(os.path.join('input_files', filenameAux + ".txt"), 'w')
                            lista_file_names.append(filenameAux)
                            for j in range(0, len(lista_final[i])):
                                f.write(lista_final[i][j])
                            f.close()
                        string_final = ''
                        for line in fileProcessingT:
                            palavras = line.split()
                            for palavra in range(0, len(palavras)):
                                if palavras[palavra] == 'UPP':
                                    sockWS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket para enviar para o WS o pedido do USER
                                    sockWS.connect((str(palavras[-2]), int(palavras[-1])))
                                    mensagem = 'WRQ UPP ' + str(lista_file_names[i_upp]) + ' ' + str(os.path.getsize(os.path.join('input_files', lista_file_names[i_upp] + '.txt'))) + ' '

                                    for x in range(0,len(lista_final[i_upp])):
                                        mensagem = mensagem + str(lista_final[i_upp][x])

                                    sockWS.send(mensagem)

                                    feedback = sockWS.recv(BUFFER_SIZE)
                                    splited_feedback = feedback.split("\n")
                                    primeira_linha_feedback = splited_feedback[0].split()
                                    for i in range(3, len(primeira_linha_feedback)):
                                        string_final += primeira_linha_feedback[i] + ' '
                                    string_final += '\n'
                                    for i in range(1, len(splited_feedback)/2-1):
                                        string_final += splited_feedback[i] + '\n'
                                    #sockWS.shutdown(socket.SHUT_RDWR)
                                    sockWS.close()
                                    os.remove(str(os.path.join('input_files', lista_file_names[i_upp] + '.txt')))
                                    i_upp += 1
                        mensagem_final = 'REP F ' + str(os.path.getsize(os.path.join('input_files', filename + '.txt'))) + ' ' + string_final
                        conn.send(mensagem_final) #enviar mensagem para o USER
                        conn.close()

                elif lista_data[1] == 'LOW':
                    if NR_LOW == 0:
                        conn.send("REP EOF")
                        conn.close()

                    else:
                        lista_final = chunks(texto_ficheiro, NR_LOW)
                        lista_file_names = []

                        for i in range(0, NR_LOW): #ciclo para criar todos os ficheiros fragmentais
                            filenameAux = filename + str(i)*3
                            f = open(os.path.join('input_files', filenameAux + ".txt"), 'w')
                            lista_file_names.append(filenameAux)
                            for j in range(0, len(lista_final[i])):
                                f.write(lista_final[i][j])
                            f.close()
                        string_final = ''
                        for line in fileProcessingT:
                            palavras = line.split()
                            for palavra in range(0, len(palavras)):
                                if palavras[palavra] == 'LOW':
                                    sockWS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket para enviar para o WS o pedido do USER
                                    sockWS.connect((str(palavras[-2]), int(palavras[-1])))
                                    mensagem = 'WRQ LOW ' + str(lista_file_names[i_low]) + ' ' + str(os.path.getsize(os.path.join('input_files', lista_file_names[i_low] + '.txt'))) + ' '
                                    for x in range(0,len(lista_final[i_low])):
                                        mensagem = mensagem + str(lista_final[i_low][x])

                                    sockWS.send(mensagem)

                                    feedback = sockWS.recv(BUFFER_SIZE)
                                    splited_feedback = feedback.split("\n")
                                    primeira_linha_feedback = splited_feedback[0].split()
                                    for i in range(3, len(primeira_linha_feedback)):
                                        string_final += primeira_linha_feedback[i] + ' '
                                    string_final += '\n'
                                    for i in range(1, len(splited_feedback)):
                                        string_final += splited_feedback[i] + '\n'

                                    #sockWS.shutdown(socket.SHUT_RDWR)
                                    sockWS.close()
                                    os.remove(str(os.path.join('input_files', lista_file_names[i_low] + '.txt')))
                                    i_low += 1

                        mensagem_final = 'REP F ' + str(os.path.getsize(os.path.join('input_files', filename + '.txt'))) + ' ' + string_final

                        conn.send(mensagem_final)
                        conn.close()

                    f.close()
            elif newpid < 0:
                print "Erro no fork"


        CONTADOR+=1

        if CONTADOR == 10:
            CONTADOR = 0

    conn.close()
