# Distributed_Project
2D racing game with chat
**Description**

Video link : https://drive.google.com/drive/folders/1hX_06eVIQZfs62jHt230rsp9-J4_poE9?usp=sharing

This repository contains several files that are part of a networked car simulation application. The files included are:

**car.py**: Simulates a car object and provides functionalities such as starting, stopping, accelerating, braking, and retrieving the current speed.

**server.py**: Sets up a server to handle network communication.

**network.py**: Provides network-related functionalities, including establishing connections, sending data, and receiving data.

**client.py**: Acts as a client to connect and interact with the server.

**File Descriptions**


# **car.py**


This file contains a Python script that simulates a car object. It provides methods to control the car's behavior, such as starting the engine, stopping the engine, accelerating, braking, and retrieving the current speed of the car.

# **server.py**


This file contains a Python script that sets up a server to handle network communication. It listens for incoming client connections and responds to requests. The server is responsible for coordinating communication between clients and providing the necessary data and functionality.

# **network.py**


This file contains a Python script that provides network-related functionalities. It includes methods for establishing network connections, sending data over the network, and receiving data from network connections. It serves as a utility module used by both the server and client scripts.

# **client.py**


This file contains a Python script that acts as a client to connect and interact with the server. It establishes a connection to the server and utilizes the provided functionalities to send requests and receive responses.

# **Usage**


To use the files in this repository, follow the steps below:

Clone the repository to your local machine using the following steps:

Copy code
python car.py
python server.py
python client.py
python network.py
Ensure that you have Python installed on your machine.

run the server then run the client
