import socket
import threading
from _thread import start_new_thread
from car import Car
import pickle
from pymongo import MongoClient
import pymongo.errors
import sys
import time
import random


#Mongo Db Connection string , Db and collections
connection_string = "mongodb+srv://ammarsaad11223:mhQotivdnA5FZqAz@cluster0.qsveoyz.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(connection_string,tlsAllowInvalidCertificates=True) # for server
client = MongoClient(connection_string)# for local
databaseMain = client["Car_game_DB"]
collection = databaseMain["Car_game"]
databaseReplica = client["Car_game_DB_Replica"]
collection1 = databaseReplica["Car_game"]
databases = [collection, collection1]


# Server settings and configurations
server = "192.168.202.28"
port = 8001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Server up and running...")



# Function to connect to the database
def checkDatabaseConnection():
    global database
    global databases
    try:
        if databaseMain.command('ping')['ok'] == 1:
            print("Successfully connected to MongoDB Main database!")
            database = databaseMain
            databases = [databaseMain]
        elif databaseReplica.command('ping')['ok'] == 1:
            print("Successfully connected to MongoDB Replica database!")
            database = databaseReplica
            databases = [databaseReplica]
        else:
            print("Failed to connect to MongoDB both Main and Replica databases!")
        if databaseMain.command('ping')['ok'] == 1 and databaseReplica.command('ping')['ok'] == 1:
            databases = [databaseMain, databaseReplica]
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB databases:", e)
        sys.exit()


#Intialize 4 fields in the DB
forallfields = {}
activePlayersStart = {"$set": {"activePlayers": 0, "playerscore": 0, "name": None, "messages": []}}
checkDatabaseConnection()
for d in databases:
    d.Car_game.update_many(forallfields, activePlayersStart)


# Retrieve player information from the database
def get_players_info(collection):
    players_info = []
    for x in collection.find({}, {"_id": 0}):
        players_info.append(tuple(x.values()))
    return players_info


#Generate Random coordinates for obstacles to pop
def generate_obstacles():
    obsL_x = [random.randrange(73, 188), random.randrange(188, 303), random.randrange(73, 188),
              random.randrange(188, 303), random.randrange(73, 188), random.randrange(188, 303),
              random.randrange(73, 188)]
    obsR_x = [random.randrange(330, 475), random.randrange(475, 620), random.randrange(330, 475),
              random.randrange(475, 620), random.randrange(330, 475), random.randrange(475, 620),
              random.randrange(330, 475)]
    obsL_img = [0, 1, 2, 3, 1, 0, 2]
    obsR_img = [1, 2, 3, 0, 3, 1, 0]
    return obsL_x, obsR_x, obsL_img, obsR_img


# Get updated player information from the database
def get_updated_info():
    global infoFromDb
    global info
    infoFromDb = get_players_info(collection)


# Generate obstacle positions and images
obsL_x, obsR_x, obsL_img, obsR_img = generate_obstacles()

# Get initial player information from the database
infoFromDb = get_players_info(collection)
print("info retrieved from DB:", infoFromDb)

info = []
for i in range(min(5, len(infoFromDb))):
    car = infoFromDb[i]
    info.append(
        Car(car[0], car[1], 355, 400, obsL_x, obsR_x, obsL_img, obsR_img))

# If the number of elements in infoFromDb is less than 5, add additional Car objects as needed
while len(info) < 5:
    info.append(Car(200, 200, 355, 400, obsL_x, obsR_x, obsL_img, obsR_img))

info = [Car(infoFromDb[0][0], infoFromDb[0][1], 355, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[1][0], infoFromDb[1][1], 490, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[2][0], infoFromDb[2][1], 215, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[3][0], infoFromDb[3][1], 600, 400, obsL_x, obsR_x, obsL_img, obsR_img),
        Car(infoFromDb[4][0], infoFromDb[4][1], 100, 400, obsL_x, obsR_x, obsL_img, obsR_img)]

# Player Unique ID initialization
currentPlayer = 0
activePlayers = 0
disconnectedPlayer = 5
start_time = time.time()


#Write player data to DB
def write_player_data(player, data):
    Player_data = data
    field = {"playerID": player}
    newInfo = {"$set": {"xPosition": Player_data.x, "yPosition": Player_data.y, "playerscore": Player_data.score,
                        "name": Player_data.nickname, "activePlayers": Player_data.activePlayers,
                        "messages": Player_data.messages}}
    for db in databases:
        db.Car_game.update_many(field, newInfo)

    # Save the messages list in all players at both databases so that when a disconnected player reconnects, they can view the current messages
    for db in databases:
        for document in db.player.find():
            db.Car_game.update_one({"_id": document["_id"]}, {"$set": {"messages": Player_data.messages}})

# Thread function to continuously write player data to the database
def write_to_database_thread(player, data):
    while True:
        time.sleep(1)
        write_player_data(player, data)


# Threaded client function to handle client requests
def handle_client_thread(conn, player):
    conn.send(pickle.dumps(info[player]))
    global activePlayers
    global disconnectedPlayer

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            info[player] = data

            write_thread = threading.Thread(target=write_to_database_thread, args=(player, data))
            write_thread.start()

            for x in range(len(info)):
                info[x].activePlayers = activePlayers

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = info[0], info[2], info[3], info[4]
                elif player == 2:
                    reply = info[0], info[1], info[3], info[4]
                elif player == 3:
                    reply = info[0], info[1], info[2], info[4]
                elif player == 4:
                    reply = info[0], info[1], info[2], info[3]
                else:
                    reply = info[1], info[2], info[3], info[4]

                print("Obtained Data:", data)
                print("Sending Data:", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Player", player + 1, "Disconnected")
    info[player].active = 0
    disconnectedPlayer = player
    print(info[player].active, "now I am disconnected")
    activePlayers -= 1

    Updated_info = {
        "$set": {"playerID": info[player].playerId, "CarId": info[player].imgID, "xPosition": info[player].x,
                 "yPosition": info[player].y, "playerscore": info[player].score, "name": info[player].nickname,
                 "activePlayers": info[player].activePlayers, "messages": info[player].messages}}

    write_to_database_thread(player,Updated_info)
    conn.close()


#Main server loop
while True:
    conn, addr = s.accept()
    print("Connected to This address:", addr)

    start_new_thread(handle_client_thread, (conn, currentPlayer))
    info[currentPlayer].active = 1
    print(info[currentPlayer].active, "now I am connected")
    currentPlayer += 1
    activePlayers += 1
