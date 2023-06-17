# Distributed_Project
2D racing game with chat
**Description**
This repository contains several files that are part of a networked car simulation application. The files included are:

**carfile.py**: Simulates a car object and provides functionalities such as starting, stopping, accelerating, braking, and retrieving the current speed.

**serverfile.py**: Sets up a server to handle network communication.

**networkfile.py**: Provides network-related functionalities, including establishing connections, sending data, and receiving data.

**clientfile.py**: Acts as a client to connect and interact with the server.

**File Descriptions**


**carfile.py**


This file contains a Python script that simulates a car object. It provides methods to control the car's behavior, such as starting the engine, stopping the engine, accelerating, braking, and retrieving the current speed of the car.

**serverfile.py**


This file contains a Python script that sets up a server to handle network communication. It listens for incoming client connections and responds to requests. The server is responsible for coordinating communication between clients and providing the necessary data and functionality.

**networkfile.py**


This file contains a Python script that provides network-related functionalities. It includes methods for establishing network connections, sending data over the network, and receiving data from network connections. It serves as a utility module used by both the server and client scripts.

**clientfile.py**


This file contains a Python script that acts as a client to connect and interact with the server. It establishes a connection to the server and utilizes the provided functionalities to send requests and receive responses.

**Usage**


To use the files in this repository, follow the steps below:

Clone the repository to your local machine using the following steps:

Copy code
python carfle.py
python serverfile.py
python clientfile.py
python networkfile.py
Ensure that you have Python installed on your machine.

run the server then run the client
