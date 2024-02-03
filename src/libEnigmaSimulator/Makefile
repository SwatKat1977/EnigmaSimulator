CPPFLAGS = -std=c++17 -Wall -g -I.

OBJS = Plugboard.o \
       Rotor.o \
	   main.o

LIBENIGMASIMULATOR = ${ENIGMASIM_BIN_DIR}/libEnigmaSimulator

$(LIBENIGMASIMULATOR): $(OBJS)
	g++ -o $(LIBENIGMASIMULATOR) $(OBJS)

all: $(LIBENIGMASIMULATOR)

clean:
	$(RM) $(LIBENIGMASIMULATOR) $(OBJS)
