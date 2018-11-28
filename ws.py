#!/usr/bin/env python
import socket
import sys
import signal
import os
import string

BUFFER_SIZE = 1024

WS_PORT = 59000
CS_NAME = socket.gethostname()
CS_PORT = 58065

nrArguments = len(sys.argv)

MESSAGE = ''

def end():
	msg = 'UNR ' + str(CS_NAME) + ' ' + str(CS_PORT)

	sockSend.sendto(msg, (CS_NAME, int(CS_PORT)))
	conn = sockSend.recvfrom(1024)
	sockSend.close()
	print 'UAK' + ' ' + conn[0]


def signal_handler(signal, frame):
    print 'pressionou CTRL-C\n'
    end()
    sockWS.close()
    sockSend.close()
    conn.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)







for i in range (nrArguments):
    if sys.argv[i] == 'WCT':
        MESSAGE = MESSAGE + 'WCT '
    elif sys.argv[i] == 'FLW':
        MESSAGE = MESSAGE + 'FLW '
    elif sys.argv[i] == 'UPP':
        MESSAGE = MESSAGE + 'UPP '
    elif sys.argv[i] == 'LOW':
        MESSAGE = MESSAGE + 'LOW '


    if sys.argv[i] == '-p':
        i = i + 1
        WS_PORT = sys.argv[i]
    elif sys.argv[i] == '-n':
        i = i+ 1
        CS_NAME = socket.gethostbyname(str(sys.argv[i]))
    elif sys.argv[i] == '-e':
        i = i + 1
        CS_PORT = sys.argv[i]

sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = 'REG ' + MESSAGE + str(CS_NAME) + ' ' + str(WS_PORT)
sockSend.sendto(msg, (CS_NAME, int(CS_PORT)))
conn = sockSend.recvfrom(1024)
sockSend.close()
print 'RAK' + ' ' + conn[0]


sockWS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockWS.bind((CS_NAME, int(WS_PORT)))
sockWS.listen(1)


while True:

	conn, addr = sockWS.accept()

	pid = os.fork()

	strings = ''

	if pid == 0:
		data = conn.recv(1024)

		frase = data.split("\n")
		words = frase[0].split()
		words_aux = data.split()

		if words[1] == 'WCT':
			resposta = 'REP R ' + str(words[3]) + ' ' + str(len(words_aux) - 4)

			conn.send(resposta)

		elif words[1] == 'FLW':
			longest_word = ''
			for word in range(3, len(words_aux)):
				if len(words_aux[word]) > len(longest_word):
					longest_word = words_aux[word]
			resposta = 'REP R ' + str(words[3]) + ' ' + longest_word
			conn.send(resposta)

		elif words[1] == 'UPP':
			string_up = ''
			for word in range(4, len(words)):
				string_up += words[word] + ' '
			string_up += '\n'
			for word in range(1, len(frase)):
				string_up += frase[word] + '\n'
			strings += string_up.upper()
			f = open(os.path.join('input_files', str(words[2] + ".txt")), 'w')
			f.write(strings)
			f.close()
			resposta = 'REP F ' + str(os.path.getsize(os.path.join('input_files', str(words[2])+ ".txt"))) + ' ' + strings
			conn.send(resposta)

		elif words[1] == 'LOW':
			string_low = ''
			for word in range(4, len(words)):
				string_low += words[word] + ' '
			string_low += '\n'
			for word in range(1, len(frase)):
				string_low += frase[word] + '\n'
			strings += string_low.lower()
			f = open(os.path.join('input_files', str(words[2]+ ".txt")), 'w')
			f.write(strings)
			f.close()

	        resposta = 'REP F ' + str(os.path.getsize(os.path.join('input_files', str(words[2])+ ".txt"))) + ' ' + strings
	        conn.send(resposta)
	else:
		continue

conn.close()
