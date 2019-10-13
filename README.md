# Open Broadcaster Software - Instant Replay
![OBS Instant Replay Preview](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_preview.PNG)

OBS Instant Replay is a script for Open Broadcaster Software which allows you to display *Instant Replay* as customizable Picture-in-Picture.  
Optionally, you can let viewers trigger instant replay using a chat command (Standalone script and Script for *Streamlabs Chatbot* included).  

*OBS Instant Replay is based on instant-replay.lua script provided by OBS*

# OBS Instant replay installation
1. Copy file to OBS scripts directory  
(1) Copy "obs-instant-replay.lua" into OBS scripts directory (Usually "C:\Program Files (x86)\obs-studio\data\obs-plugins\frontend-tools\scripts\")  

2. Add script to OBS  
(1) In OBS main menu, open "Tools">"Scripts"  
![Open scripts window](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_scripts_open.png)  
(2) Click "+" button and add script "obs-instant-replay.lua"  
*Do not change any parameters yet.*  

3. Enable replay buffer in OBS  
(1) In OBS Settings under "Output", select "Replay Buffer" tab  
(2) Check Enable Replay Buffer  
(3) Set "Maximum Replay Time" in seconds (Ideal time for replay is should be between 15 - 30 seconds)  
![Enable Replay Buffer](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_replaybuffer.PNG)

4. (Optional) Set recording to overwrite  
*This step is optional and will force OBS to overwrite video file on each replay instead of creating new one. This also applies to recording and there is no option to separate recording from replay at the moment.*  
In OBS Settings under "Advanced", "Recording" section:  
(1) Change "Filename Formatting" to a specific name  
(2) Check "Overwrite if file exists  
(3) Enter "Replay", or any keyword of your choosing into "Replay Buffer Filename Prefix" to prevent possible filename conflict with regular recording session  
![Overwrite Replay Buffer](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_recording.PNG)

5. (Optional) Automatically start replay buffer when streaming  
In OBS Settings under "General", "Output" section:  
(1) Check "Automatically start replay buffer when streaming"  
![Automatically start Replay Buffer](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_automaticreplaybuffer.PNG)

6. Set Hotkeys in OBS  
In OBS Settings under "Hotkeys":  
(1) Set hotkey for "OBS Instant Replay" (Used to trigger the replay)  
(2) Set hotkey for "Save Replay" under "Replay Buffer" section. (You will never use this hotkey, but it is mandatory by OBS for Replay Buffer to work)  
![Configure Hotkeys](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_hotkeys.PNG)

7. Create Replay scene  
*Replay scene will be named "Replay" in this guide for simplicity. You may chose any name you want.*  
(1) Add "Media Source" and fit it to screen. (Named "Replay Media Player" in this guide)  
(2) (Optionally) Add loading image/video (Named "Overplay Replay Loading" in this guide)  
(3) (Optionally) Add transparent overlaying image as indication that the element is a replay (Named "Overplay Replay" in this guide, showing "INSTANT REPLAY" in top left corner and "<< REW" in lower right corner)  
(4) (Optionally) You may add any other elements to customize this scene  
![Create Replay Scene](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_scene_create.PNG)

8. Add Replay to your scenes  
(1) Add Replay Scene as a Source to all scenes where you want replay to appear  
(2) Resize sources as needed.  

9. Configure OBS Instant Replay
(1) In OBS main menu, open "Tools">"Scripts" and configure obs-instant-replay  
**Enable**: Check to enable  
**Replay Scene**: Set to replay scene (Named "Replay" in this guide)  
**Media Source**: Set to media source within replay scene (Named "Replay Media Player" in this guide)  
**Replay duration**: Should match maximum replay time as set for replay buffer (As configured on step 3.3. in this guide)  
*After applying settings, all sources in "Replay" scene will become invisible.*  
![Configure script](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_scripts_config.png)

# Instant Replay Standalone Triggering configuration
*Instant Replay Standalone Triggering script is used only to let viewers/moderators trigger replay. If you do not require this functionality, you will not need this.*
1. Prepare standalone triggering  
(1) Download and install Python 3.7  
(2) Navigate into "instant-replay-standalone" directory  
(3) Rename file "settings.json.template" to "settings.json"  

2. Configure standalone triggering  
(1) Edit "settings.json"

```
{
    "Command": "!replay",
    "Permission": "",
    "Cooldown": 30.0,
    "TwitchChannel": "",
    "TwitchOAUTH": ""
}
```
- **Command** Command to trigger a replay (default: !replay)
- **Permission** Configure who can trigger a replay
  - **"broadcaster"** - Broadcaster only
  - **"moderator"** - Moderators and Broadcaster
  - **"subscriber"** - Subscribers, Moderators and Broadcaster
  - **""** - Everyone
- **Cooldown** Command cooldown in seconds (default: 30)
- **TwitchChannel** Channel name.
- **TwitchOAUTH** How to obtain a Twitch OAUTH: <a href="https://www.twitchapps.com/tmi/" target="_blank">www.twitchapps.com/tmi/</a>.


3. Set Hotkey in OBS  
In OBS Settings under "Hotkeys":  
(1) Press "+" sign next to "OBS Instant Replay" to create new entry  
(2) Click into new empty box created right under "OBS Instant Replay" and start "instant-replay-setup.exe"  
![OBS Hotkey for Chatbot](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_slcb_hotkey.PNG)

4. Run "instant-replay-standalone.cmd"  

# Streamlabs Chatbot script installation
*Streamlabs Chatbot script is used only to let viewers/moderators trigger replay. If you do not require this functionality, you will not need this.*  
1. Copy files Streamlabs Chatbot scripts directory  
(1) Copy directory "obs-instant-replay-streamlabs-chatbot" into Streamlabs Chatbot scripts directory "%APPDATA%\Streamlabs\Streamlabs Chatbot\Services\Scripts\"  

2. Enable and configure OBS Instant Replay script  
(1) Change settings as needed.  
![Enable Script](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/slcb_scripts.PNG)

3. Configuring Streamlabs Chatbot to use scripts  
*This step is only needed for first time script setup. If you used scripts withing Chatbot before, it will be already set up.*  
(1) Download and install Python 2.7
(2) Within settings, browse to Python\Lib directory  
(3) If your API Key is not generated yet, generate it  
![Chatbot Settings](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/slcb_settings.PNG)

4. Set Hotkey in OBS  
In OBS Settings under "Hotkeys":  
(1) Press "+" sign next to "OBS Instant Replay" to create new entry  
(2) Click into new empty box created right under "OBS Instant Replay" and start "instant-replay-setup.exe"  
![OBS Hotkey for Chatbot](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_slcb_hotkey.PNG)
