CPPFLAGS = -std=c++17 -Wall -g -I.

ifeq (1,$(LOG_DEBUG))
CPPFLAGS+=-DENIGMASIM_DEBUG
endif

OBJS = EnigmaMachine.o \
	Plugboard.o \
	Reflector.o \
	ReflectorFactory.o \
	Rotor.o \
	RotorFactory.o \
	main.o

LIBENIGMASIMULATOR = ${ENIGMASIM_BIN_DIR}/libEnigmaSimulator

$(LIBENIGMASIMULATOR): $(OBJS)
	g++ $(OPTIONS) -o $(LIBENIGMASIMULATOR) $(OBJS)

all: $(LIBENIGMASIMULATOR)

clean:
	$(RM) $(LIBENIGMASIMULATOR) $(OBJS)
