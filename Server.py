#!/usr/bin/python
import socket
import os
import sys       
pathname = os.path.dirname(sys.argv[0])
Working_directory = os.path.abspath(pathname)



class Net_DB_Server(object):
	def __init__(self,directory):
		self.filename=directory+'/TD2'
		self.readDatabaseFile(self.filename)
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind(("192.168.1.150", 12345))
		self.serversocket.listen(5) # become a server socket, maximum 5 connections
		print socket.gethostname()
		pass

	def readDatabaseFile(self, databaseFilePath):
		print 'Reading database file'
		with open(databaseFilePath, 'r') as f:
			new_Text = f.read()
		self.database = {}

		for row in new_Text.split('\n')[0:]:
			rowSplit = row.split(',')
			if (len(rowSplit) != 4):
				print 'Skipping row. Length incorrect. {0}'.format(row)
				continue
			try:
			    ID = rowSplit[0].strip()
			    Mill_TL = rowSplit[1].strip()
			    Lathe_TL = rowSplit[2].strip()
			    FPS_Template = rowSplit[3].strip()
			except Exception as ex:
				print 'There was a problem parsing the database row: {0}. {1}'.format(row, str(ex))
				continue

			self.database[ID] = {'Mill_TL': Mill_TL, 'Lathe_TL': Lathe_TL,
			                   'FPS_Template': FPS_Template}

	def Server_Loop(self):
		while True:
			print "looping"
			c, address = self.serversocket.accept()
			buf = c.recv(1200)
			if len(buf) > 0:
				if buf == "ping":
					print "ping"
					c.send("pong")
					print "pong"
				else:
					data = buf.split(',')
					print "data"
					if data[0] == "Enroll User":
						print "Enrolling User"
						self.Update_User_Data(data[1],data[2],data[3],data[4])
					else:
						print "sending"	
						ID = data[0]
						print ID
						if ID in self.database:
							print 'Sending requested user data ID =' + ID
							UserProfile=self.database[ID]
							message = ID + ',' + UserProfile['Mill_TL'] + ',' + UserProfile['Lathe_TL'] + ','+ UserProfile['FPS_Template']
							c.send(message)

						else:
							print "ID not found"
							c.send("ID not found")

	def Update_User_Data(self,USERID,Mill_TL,Lathe_TL,FPS_Template):
			self.database[USERID] = {'Mill_TL': Mill_TL, 'Lathe_TL': Lathe_TL,'FPS_Template': FPS_Template}
			f=open(self.filename,'w')
			f.truncate()
			for ID in self.database:
				UserProfile=self.database[ID]
				line = ID + ',' + UserProfile['Mill_TL'] + ',' + UserProfile['Lathe_TL'] + ',' + UserProfile['FPS_Template']
				f.write(line + '\n')
			f.close()
			self.readDatabaseFile(self.filename)




try:
	A = Net_DB_Server(Working_directory)
	A.Server_Loop()
except Exception as e:
	print e
	A.serversocket.shutdown(socket.SHUT_RDWR)
	A.serversocket.close()
