# Indirect RPC
In this exercise, you have to simulate an RPC (Remote Procedure Call) with RabbitMQ. For this, you need to create two programs, one that acts as a client and another as a server. The server only carries out one task, which is to calculate the factorial of a number. The client, on the other hand, sends a number to the server and waits for it to return the result of the factorial calculation.

To implement this application, you will have to create two message queues, one for handling requests and another for handling responses. The client will send a message to the request queue and wait for the server to send a message to the response queue. The server, in turn, will be listening on the request queue and will send the result to the response queue.

Keep in mind that the client can specify, when posting a message, which is the response message queue to which the server should send the result. In addition, it will be necessary to link each request with its corresponding response. To do this, you can use the message correlation identifier provided by RabbitMQ:

```python
properties = pika.BasicProperties(
    reply_to = results_queue,
    correlation_id = correlation_id
)
```
