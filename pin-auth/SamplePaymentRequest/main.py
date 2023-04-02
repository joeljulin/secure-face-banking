import json
import socket

data = {
    "amount": 50.00,
    "currency": "USD",
    "description": "Online Purchase",
    "card_number": 4321265464573164,
    "expiration_month": 12,
    "expiration_year": 2028,
    "cvv": 123,
    "cardholder_name": "John Smith",
}

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.21.160.1', 16801)
clientsocket.connect(server_address)
print("sent")

message = json.dumps(data)
clientsocket.send(message.encode())


clientsocket.close()