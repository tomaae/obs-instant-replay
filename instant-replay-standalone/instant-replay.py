import socket
import threading
import json
import re
import os
import codecs


#---------------------------
#   Settings Handling
#---------------------------
class Settings:
	def __init__(self, pathRoot=None):
		self.pathRoot     = pathRoot + '\\'
		if not os.path.isdir(self.pathRoot):
			print("Working directory not detected.")
			exit(1)
		if not os.path.exists(self.pathRoot + "settings.json"):
			print("Configuration file \"settings.json\" is missing.")
			exit(1)
			
		self.Reload()
		return
		
	def Reload(self):
		print("Loading settings...")
		self.TwitchChannel  = ""
		self.TwitchOAUTH    = ""
		self.Command        = ""
		self.Permission     = ""
		self.Cooldown       = ""
		
		try:
			with codecs.open(self.pathRoot + "settings.json", encoding="utf-8-sig", mode="r") as f:
				data = json.load(f, encoding="utf-8")
				for key, value in data.items():
						self.__dict__[key] = value 
		except Exception as err:
			print("Unable to load settings.json. {0}".format(err))
			exit(1)
		finally:
			#
			# CONVERT
			#
			self.TwitchChannel = self.TwitchChannel.lower()

#---------------------------
#   Twitch API
#---------------------------
class Twitch:
	def __init__(self, settings):
		self.settings = settings
		self.host     = "irc.twitch.tv"                           # Hostname of the IRC-Server in this case twitch's
		self.port     = 6667                                      # Default IRC-Port
		self.chrset   = 'UTF-8'
		self.con      = socket.socket()
		return
		
	#---------------------------
	#   Connect
	#---------------------------
	def Connect(self):
		threading.Thread(target=self.Connection).start()
		return
		
	#---------------------------
	#   Connection
	#---------------------------
	def Connection(self):
		print("Connecting to Twitch...")
		try:
			self.con = socket.socket()
			self.con.connect((self.host, self.port))
			self.con.send(bytes('PASS %s\r\n'  % self.settings.TwitchOAUTH,       self.chrset)) # www.twitchapps.com/tmi/ will help to retrieve the required authkey
			self.con.send(bytes('NICK %s\r\n'  % self.settings.TwitchChannel,     self.chrset))
			self.con.send(bytes('JOIN #%s\r\n' % self.settings.TwitchChannel,     self.chrset))
			self.con.send(bytes('CAP REQ :twitch.tv/tags twitch.tv/commands\r\n', self.chrset))
		except:
			print("Unable to connect to Twitch...")
			return 1
		print("Connected to Twitch...")
		
		data = ""
		while True:
			try:
				data = data+self.con.recv(1024).decode(self.chrset)
				data_split = re.split(r"[~\r\n]+", data)
				data = data_split.pop()
				
				threading.Thread(target=self.ProcessData, args=(data_split,)).start()
				
			except socket.error:
				print("Twitch socket error")
			
			except socket.timeout:
				print("Twitch socket timeout")
		return
		
	#---------------------------
	#   ProcessData
	#---------------------------
	def ProcessData(self, data):
		for line in data:
			line = line.strip()
			line = line.split(" ")
			#print(line)
								
			if len(line) >= 1:
				if line[0] == 'PING':
					self.con.send(bytes('PONG %s\r\n' % line[1], self.chrset))
					continue

				jsonData = self.fill_tags()
				#
				# CHAT
				#
				if len(line) >= 3 and line[2] == 'PRIVMSG':
					jsonData = self.parse_tags(jsonData, line[0])
					jsonData['message'] = self.get_message(line)
					
					# COMMAND
					if jsonData['message'].find(settings.Command) == 0:
						if settings.Permission == "subscriber" and (jsonData['subscriber'] or jsonData['moderator']) == "1":
							print("Replay triggered")
							os.system("\"" + os.path.join(os.path.dirname(os.path.realpath(__file__)), "instant-replay.exe") + "\"")
							continue
						if settings.Permission == "moderator" and jsonData['moderator'] == "1":
							print("Replay triggered")
							os.system("\"" + os.path.join(os.path.dirname(os.path.realpath(__file__)), "instant-replay.exe") + "\"")
							continue
						if settings.Permission == "broadcaster" and jsonData['broadcaster'] == "1":
							print("Replay triggered")
							os.system("\"" + os.path.join(os.path.dirname(os.path.realpath(__file__)), "instant-replay.exe") + "\"")
							continue
						
					continue
		return

	#---------------------------
	#   fill_tags
	#---------------------------
	def fill_tags(self):
		result = {
			"moderator": "0",
			"subscriber": "0",
			"broadcaster": "0",
			"bits_total": "0",
			"bits": "0",
			"display-name": "",
			"msg-id": "", # Valid values: sub, resub, subgift, anonsubgift, raid, ritual.
			"msg-param-viewerCount": "", # (Sent only on raid) The number of viewers watching the source channel raiding this channel.
			"msg-param-recipient-display-name": "", # (Sent only on subgift, anonsubgift) The display name of the subscription gift recipient.
			"msg-param-sub-plan": "", #(Sent only on sub, resub, subgift, anonsubgift) The type of subscription plan being used. Valid values: Prime, 1000, 2000, 3000. 1000, 2000, and 3000 refer to the first, second, and third levels of paid subscriptions, respectively (currently $4.99, $9.99, and $24.99).
			"msg-param-months": "", # (Sent only on sub, resub, subgift, anonsubgift) The number of consecutive months the user has subscribed for, in a resub notice.
			"msg-param-ritual-name": "", # (Sent only on ritual) The name of the ritual this notice is for. Valid value: new_chatter.
			"login": "",
			"emotes": "", # <emote ID>:<first index>-<last index>,<another first index>-<another last index>/<another emote ID>:<first index>-<last index>...
			"command": "",
			"command_parameter": "",
			"sender": "",
			"message": ""
		}
		return result

	#---------------------------
	#   parse_tags
	#---------------------------
	def parse_tags(self, jsonData, msg):
		tags = msg.split(";")
		for tag in tags:
			tag = tag.split("=")
			#"@badges": "", # Comma-separated list of chat badges and the version of each badge (each in the format <badge>/<version>. Valid badge values: admin, bits, broadcaster, global_mod, moderator, subscriber, staff, turbo.
			if tag[0] == 'badges':
				badges = tag[1].split(",")
				for badge in badges:
					badge = badge.split("/")
					if badge[0] == 'broadcaster' or badge[0] == 'moderator' or badge[0] == 'subscriber':
						if badge[0] in jsonData:
							jsonData[badge[0]] = badge[1]
							if badge[0] == 'broadcaster':
								jsonData["moderator"] = "1"
								jsonData["broadcaster"] = "1"
					if badge[0] == 'bits':
						jsonData["bits_total"] = badge[1]
			else:
				if tag[0] in jsonData:
					jsonData[tag[0]] = tag[1]
		return jsonData
		
	#---------------------------
	#   get_message
	#---------------------------
	def get_message(self, msg):
		result = ""
		i = 4
		length = len(msg)
		while i < length:
			result += msg[i] + " "
			i += 1
		result = result.lstrip(':')
		result = result.strip()
		return result

#---------------------------
#   Main
#---------------------------
pathRoot = os.path.dirname(os.path.realpath(__file__))
# Initialize settings
settings = Settings(pathRoot=pathRoot)

# Initialize twitch
twitch = Twitch(settings=settings)
twitch.Connect()

print("Started...")
while True:
	input("")

exit(0)