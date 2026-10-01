## Garage door protocol
We have a two-leaf swing garage door that will be operated by a wireless remote. The control unit only offers 3 operations: open, close, and check status. The controller will return an error when requesting to open or close if the door is already in that state.
The open command has 2 modes: vehicle and pedestrian (in which only one of the leaves opens). The remote can indicate the time the door remains open, otherwise, it will remain open indefinitely.
The control unit will always respond to each command with an OK or error code. The possible errors are:

- The door is already open
- The door is already closed
- An obstacle was found
- The motor does not respond

Design the protocol. Then, implement this application in Python with sockets and Protocol Buffers.
