import json
import os
import random
import smtplib
import socket
import ssl
import threading
import time
from email.mime.text import MIMEText
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import cards

email_sender = 'SecureFaceBanking@gmail.com'
email_password = 'oukn kgzd jgul wnon'


def cardauth(data, acc):
    if (data["expiration_month"] == acc["expiration_month"] and
        data["expiration_year"] == acc["expiration_year"] and
        data["cvv"] == acc["cvv"] and
        data["cardholder_name"] == acc["cardholder_name"] and
        data["amount"] <= acc["balance"]):
        return True
    else:
        return False

global msg
msg = ""
def fauth_thread():
    global cauth
    cauth = cardauth(data, cards.acc1)
    if cauth:
        print("hi")
    else:
        print("crap")


def email_thread(data):
    email_reciever = cards.acc1["card_email"]
    global pin
    pin = random.randint(100000, 999999)
    print(pin)
    subject = 'Your pin is ' + str(pin) + "\n"
    body = ("Enter the pin or open the Secure Face app to verify by facial scan.\n"
            "Thank you for participating in Secure Face banking!\n\n"
            "Purchase info \n" +
            "Time: " + str(time.ctime()) + "\n" +
            "Purchase description: " + data["description"] + "\n"
             "Invoice amount: ${:.2f}".format(data["amount"])
            )
    msg = MIMEText(body)
    msg["Subject"] = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_reciever, msg.as_string())
    print("Email to " + email_reciever + " sent!")
    server.quit()


def socket_thread():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    server_address = (ip, 16801)
    serversocket.bind(server_address)

    serversocket.listen(1)
    print("Listening for a connection at", ip + "...")
    while True:
        clientsocket, address = serversocket.accept()
        print("Connected with " + address[0] + ":" + str(address[1]))

        message = clientsocket.recv(1024).decode()
        data = json.loads(message)
        print(data)
        email_thread(data)



socket_thread = threading.Thread(target=socket_thread)
socket_thread.start()


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        global PIN
        form = self.headers['Content-Type']
        if form == "application/x-www-form-urlencoded":
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length).decode("utf-8")
            PIN = data.split("=")[1]
            print(PIN)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(b'OK')


with TCPServer(("", 8000), Handler) as httpd:
    print("Server started at http://localhost:8000")
    httpd.handle_request()

if int(pin) == int(PIN):
    msg = "Payment Approved!"
    print(msg)
else:
    msg = "Payment Denied"
    print(msg)