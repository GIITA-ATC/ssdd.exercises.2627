## Adding two numbers using a UDP socket connection
In this exercise we will create a simple client-server application that adds two numbers. The client will send two numbers (4-bytes integers) to the server, and the server will return the sum (4-bytes integer) of the two numbers. The client will then print the result. The server must run forever, listening for incoming messages.

Exec client and server programs in the following manner and order, in different terminal windows:
```bash
$ python3 server.py
```
```bash
$ python3 client.py <server_host:port> <number_1> <number_2>
```

### Sequence diagram

```
              +-----------------+        +-----------------+
              |                 |        |                 |
              |      Client     |        |      Server     |
              |                 |        |                 |
              +-----------------+        +-----------------+
                       |                          |
                   +---|                          |---+
msg = pack(n1, n2) |   |                          |   |
                   +-->|                          |   |  msg = recv()
                       |         send(msg)        |   |
                       |------------------------->|<--+
                   +---|                          |
                   |   |                          |---+
        r = recv() |   |                          |   |  n1, n2 = unpack(msg)
                   |   |                          |   |  r = n1 + n2
                   |   |        send(r)           |<--+
                   +-->|<-------------------------|
                       |                          |---+
                   +---|                          |   |
result = unpack(r) |   |                          |   |  msg = recv()
     print(result) |   |                          |   |
                   +-->|                          |   |
                       |                          |   |
                       #                          |   |
                    finished                      ...   (loop forever)
```
