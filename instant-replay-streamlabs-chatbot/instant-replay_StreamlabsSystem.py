
#---------------------------
#   Import Libraries
#---------------------------
import os
import codecs
import sys
import re
import json

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "OBS Instant Replay"
Description = "Streamlabs Chatbot addon for OBS instant-replay"
Creator = "Tomaae"
Website = ""
Version = "1.0.0.0"

#---------------------------
#   Settings Handling
#---------------------------
class Settings:
	def __init__(self):
		self.settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")
		try:
			with codecs.open(self.settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.Command = "!replay"
			self.Cooldown = 30
			self.Permission = "moderator"
			self.Info = ""
			
		return

	def Reload(self, jsondata):
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self):
		try:
			with codecs.open(self.settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8")
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")
		return

#---------------------------
#   Define Global Variables
#---------------------------
global ScriptSettings
ScriptSettings = Settings()


#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
	# Load settings
	global ScriptSettings
	ScriptSettings = Settings()

	return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
	if data.IsChatMessage():
		rawMessage = data.RawData

		if data.GetParam(0).lower() != ScriptSettings.Command.lower():
			return
		
		if Parent.IsOnCooldown(ScriptName, ScriptSettings.Command):
			return
			
		if not Parent.HasPermission(data.User, ScriptSettings.Permission, ScriptSettings.Info):
			return

		os.system("\"" + os.path.join(os.path.dirname(os.path.realpath(__file__)), "instant-replay.exe") + "\"")

		Parent.AddCooldown(ScriptName, ScriptSettings.Command, ScriptSettings.Cooldown)  # Put the command on cooldown

	return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
	return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
	return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
	ScriptSettings.Reload(jsonData)
	ScriptSettings.Save()
	return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
	return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
	return

def UpatedUi():
	ui = {}
	UiFilePath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
	try:
		with codecs.open(UiFilePath, encoding="utf-8-sig", mode="r") as f:
			ui = json.load(f, encoding="utf-8")
	except Exception as err:
		Parent.Log(ScriptName, "{0}".format(err))

	# update ui with loaded settings
	ui['Command']['value'] = ScriptSettings.Command
	ui['Cooldown']['value'] = ScriptSettings.Cooldown
	ui['Permission']['value'] = ScriptSettings.Permission
	ui['Info']['value'] = ScriptSettings.Info

	try:
		with codecs.open(UiFilePath, encoding="utf-8-sig", mode="w+") as f:
			json.dump(ui, f, encoding="utf-8", indent=4, sort_keys=True)
	except Exception as err:
		Parent.Log(ScriptName, "{0}".format(err))
