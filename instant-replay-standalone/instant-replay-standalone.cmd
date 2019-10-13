@echo off
python.exe instant-replay.py
IF %ERRORLEVEL% NEQ 0 (
	pause
)