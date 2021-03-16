CC = gcc # C compiler
BIN = bin

install:
	$(CC) -fpic -shared -o libsolver.so \
		-I/usr/include/python3.8 -lpython3.8 \
		src/Solver.c
	[ -d $(BIN) ] || mkdir $(BIN)/libsolver.so
	mv -f libsolver.so $(BIN)/libsolver.so	