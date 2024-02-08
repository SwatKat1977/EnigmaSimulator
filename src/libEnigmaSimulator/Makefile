CPPFLAGS = -std=c++17 -Wall -g -I.

ifeq (1,$(LOG_DEBUG))
CPPFLAGS+=-DENIGMASIM_DEBUG
endif

OBJS = Plugboard.o \
       Rotor.o \
	   Reflector.o \
	   main.o

LIBENIGMASIMULATOR = ${ENIGMASIM_BIN_DIR}/libEnigmaSimulator

$(LIBENIGMASIMULATOR): $(OBJS)
	g++ $(OPTIONS) -o $(LIBENIGMASIMULATOR) $(OBJS)

all: $(LIBENIGMASIMULATOR)

clean:
	$(RM) $(LIBENIGMASIMULATOR) $(OBJS)
