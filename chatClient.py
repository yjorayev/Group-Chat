from socket import *
import sys
import threading
host = "127.0.0.1"
port = 9999

class listen(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client
		self.setDaemon(True)

	def run(self):
		while(True):
			data = self.client.recv(1024)
			if data.decode() == "exit":
				sys.exit(0)
			print(data.decode())




if __name__ == "__main__":
	try:
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((host, port))
		print("Welcome to chat!")
		print("Type your message and press 'Enter' to send.")
		print("Send '/name' command to change your username.")
		print("Send '/quit' command to quit.")
	except error as e:
			if clientSocket:
				clientSocket.close()
			print("Could not open a socket: "+ str(e))
			sys.exit(1)

	l = listen(clientSocket)
	l.start()
	message = input()
	while True:
		#sys.stdout.flush()
		clientSocket.send(message.encode())
		#data = self.clientSocket.recv(1024)
		#data = data.decode()
		#print("Recieved: "+str(data))
		message= input()
	clientSocket.close()
