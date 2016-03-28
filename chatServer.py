from socket import *
import select
import sys
import threading

QUIT = False

class Server:
	def __init__(self):
		self.host = "127.0.0.1"
		self.port = 9999
		self.threads = []
		self.backlog = 10 

	def run(self):
		all_good = False
		#while not all_good:
		try:
			#all_good = False
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			self.sock.bind((self.host, self.port))
			self.sock.listen(self.backlog)
			#all_good= True
			print("Server started at "+self.host+":"+str(self.port))
			#break
		except Exception as err:
			print('Socket connection error... ')
			self.sock.close()
		try:
			while not QUIT:
				try:
					client, addr = self.sock.accept()
				except socket.timeout:
					continue
				new_thread = Client(client)
				print("Connected by ", addr)
				msg = ("Connected by %s at %s" %(new_thread.name, addr)).encode()
				for each in self.threads:
					each.client.send(msg)

				self.threads.append(new_thread)
				new_thread.start()

				for thread in self.threads:
					if not thread.isAlive():
						self.threads.remove(thread)
						thread.join()
		except KeyboardInterrupt:
				print("Terminating by Ctrl+C")
		except Exception as err:
			print("Exception: %s\nClosing" %err)
		for thread in self.threads:
			thread.join()
		self.sock.close()


class Client(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client

	def run(self):
		global QUIT
		done = False
		
		while not done:
			try:
				cmd = self.client.recv(1024).decode()
				if cmd.startswith("/name"):
					self.client.send("Enter your username: ".encode())
					old_name = self.name
					self.name = self.client.recv(1024).decode()
					msg = "%s has changed his username to %s" %(old_name, self.name)
					for each in server.threads:
						if each != self and each.isAlive():
							each.client.send(msg.encode())
					self.client.send(("Your username has been changed to %s" %self.name).encode())
				elif cmd == "/quit":
					self.client.send("exit".encode())
					self.client.close()
					server.threads.remove(self)
					for each in server.threads:
							each.client.send(("%s Disconnected" %self.name).encode())
					QUIT = True
					done = True
				else:
					msg = "%s===>%s" %(self.name, cmd)
					for each in server.threads:
						if each != self:
							each.client.send(msg.encode())
			except Exception as e:
				print("Connection lost", e)
				self.client.close()
				done = True
				continue
			
		self.client.close()
		return


if __name__ == "__main__":
	server = Server()
	server.run()

	print("Terminated")
