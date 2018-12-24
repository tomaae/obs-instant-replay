# Open Broadcaster Software - Instant Replay
![OBS Instant Replay Preview](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_preview.PNG)

OBS Instant Replay is a script for Open Broadcaster Software which can be used to display Instant replay as Picture-in-Picture.  
Optionally, you can let viewers trigger instant replay using a chat command (Script for *Streamlabs Chatbot* included).  

*obs-instant-replay is based on instant-replay.lua script developed by OBS*

# OBS Instant replay installation
1. Copy "instant-replay.lua" into OBS scripts directory (Usually "C:\Program Files (x86)\obs-studio\data\obs-plugins\frontend-tools\scripts\").  
You can rename the file is you want.

2. In OBS main menu, open "Tools">"Scripts"  
*Do not change any parameters yet*  
![Open scripts window](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_scripts_open.png)

3. Enable replay buffer in OBS  
In OBS Settings under "Output", select "Replay Buffer" tab.  
Check Enable Replay Buffer.  
Set "Maximum Replay Time" in seconds.  
![Enable Replay Buffer](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_replaybuffer.PNG)

4. (Optional) Set recording to overwrite  
*This step is optional and will force OBS to overwrite video file on each replay instead of creating new one.*  
In OBS Settings under "Advanced", "Recording" section:  
"Change Filename Formatting" to a specific name.  
Check "Overwrite if file exists.  
Enter "Replay", or any keyword of your choosing into "Replay Buffer Filename Prefix" to prevent filename conflict with recording. 
![Overwrite Replay Buffer](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_recording.PNG)

5. (Optional) Automatically start replay buffer when streaming  
In OBS Settings under "General", "Output" section:  
Check "Automatically start replay buffer when streaming".  
![Automatically start Replay Buffer](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_automaticreplaybuffer.PNG)

6. Set Hotkeys in OBS  
In OBS Settings under "Hotkeys":  
Set hotkey for "OBS Instant Replay" (Used to trigger the replay)  
Set hotkey for "Save Replay" under "Replay Buffer" section. (You will never use this hotkey, btu it is mandatory for Replay Buffer to work.)  
![Configure Hotkeys](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_settings_hotkeys.PNG)

7. Create Replay scene  
*Replay scene will be named "Replay" in this guide for simplicity. You may chose any name you want.*  
Add "Media Source" and fit it to screen. (Named "Replay Media Player" in this guide)  
(Optionally) Add loading image/video (Named "Overplay Replay Loading" in this guide)  
(Optionally) Add transparent overlaying image as indication that the element is a replay (Named "Overplay Replay" in this guide, showing "INSTANT REPLAY" in top left corner and "<< REW" in lower right corner)  
(Optionally) You may add any other elements to customize this scene  
![Create Replay Scene](https://raw.githubusercontent.com/tomaae/obs-instant-replay/github-resources/obs_scene_create.PNG)

8. Add Replay to your scenes  
Add Replay Scene as a Source to all scenes where you want replay to appear.  
Resize sources as needed.  

9. In OBS main menu, open "Tools">"Scripts" and configure obs-instant-replay.  
**Replay Source**: Set to replay scene  
**Media Source**: Set to media source within replay scene  
**Replay duration**: Should match maximum replay time as set for replay buffer  
*After applying settings, all sources in "Replay" scene will become invisible.*  

# Streamlabs Chatbot plugin installation and configuration

