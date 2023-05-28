from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)

serverHost = '192.168.56.1'
serverPort = 8080

clientSocket.connect((serverHost, serverPort))
print(f"[CONNECTED] Client connected to server at {serverHost}:{serverPort}")

filename = input("Masukkan nama file: ")
request = "GET /" + filename + " HTTP/1.1\r\nHost: " + serverHost + "\r\n\r\n"
clientSocket.send(request.encode())
response = clientSocket.recv(9999).decode()
print(response)

clientSocket.close()