# Videogame deals notifier
In this exercise, you are to create a videogame deals notification system using the MQTT protocol in Python, with the Paho module. The system will consist of two parts: a publisher that will send out information about videogame deals, and a subscriber that will receive such notifications according to the user's interests.

The publisher should send messages with the name of the videogame and the discount percentage (see `videogames.py`), one per second, to an MQTT broker according to the topic hierarchy:

```
videogames/deals/<type>/<developer>
```

The subscriber should subscribe to topics according to the user's interests, which will be specified via command line. For example, if the user is interested in action videogames from the developers Ubisoft and Rockstar:

```
subscriber.py -d ubisoft rockstar -t action-RPG
```

And if they are interested in any type of videogame from the developer Valve:

```
subscriber.py -d valve
```

For all messages of interest, a text will be published on the terminal, printing a special text in case the discount is greater than 70%.

### Requirements
Install the following Debian packages:
```bash
sudo apt install mosquitto
```

Ensure the Mosquitto broker is running:
```bash
sudo service mosquitto restart
netstat -tuln | grep 1883
```
