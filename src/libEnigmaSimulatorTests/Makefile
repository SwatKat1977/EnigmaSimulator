CPPFLAGS = -std=c++17 -Wall -g -I. -I /opt/homebrew/include -I ../libEnigmaSimulator
# CPPFLAGS += --coverage -ftest-coverage # -fprofile-arcs

LIB_DIRS = -L /opt/homebrew/lib
LIBRARIES = -lgtest
CXX = g++

OBJS = ../libEnigmaSimulator/Rotor.o \
	../libEnigmaSimulator/Plugboard.o \
	RotorTests.o

LIBTESTS = ./libEnigmaSimulatorTests

$(LIBTESTS): $(OBJS)
	g++ -o $(LIBTESTS) $(OBJS) $(LIB_DIRS) $(LIBRARIES)

all: $(LIBTESTS)

clean:
	$(RM) $(LIBTESTS) $(OBJS)
