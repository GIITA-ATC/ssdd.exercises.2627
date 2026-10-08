## Restaurant Reservation System
A very prestigious restaurant, which only offers one service during dinner time per day, wishes to commission the development of a reservation management system. The services that this system should provide are:

- Request a reservation, indicating time (date+hour), number of diners, client's name, and contact phone number. In response, the client will receive: if the reservation is possible, the reservation generated; if the reservation is not possible, an error and the reason for the denial.
- Check a reservation, indicating the reservation identifier. In response, the client will receive: if the reservation exists, the details of the reservation; if the reservation doesn't exist, an error and the reason for the denial.
- Cancel a reservation, indicating the reservation identifier. In response, the client will receive: if the reservation exists, confirmation of the cancellation; if the reservation doesn't exist, an error and the reason for the denial.
- List the reservations. In response, the client will receive a list of reservations, even empty.

Implement this reservation application in Python, using Protocol Buffers to define the messages and services, and gRPC to implement the server and client applications.
