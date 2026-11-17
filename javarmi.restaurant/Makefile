.PHONY: all run-registry run-server run-client clean

SERVER_HOST ?= localhost
ARGS ?= list

all: Restaurant.class Reservation.class ReservationException.class Server.class Client.class

%.class: %.java
	javac $<

run-registry:
	rmiregistry

run-server:
	java -classpath . -Djava.rmi.server.hostname=$(SERVER_HOST) Server

run-client:
	java -classpath . Client $(SERVER_HOST) $(ARGS)

clean:
	$(RM) *.class *~
