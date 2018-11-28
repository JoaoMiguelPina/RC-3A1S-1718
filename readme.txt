RC DISTRIBUTED PROCESSING

-Compile:
	make
-Clean:
	make clean
-Run User Application:
	./user [-n CSname] [-p CSport]
-Run Central Server:
	./cs [-p CSport]
-Run Working Server:
	./ws PTC(1) ... PTC(n) [-p WSport] [-n CSname] [-e CSport]
