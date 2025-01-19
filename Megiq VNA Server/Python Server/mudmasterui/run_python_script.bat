@echo off

:: Add a delay (in seconds) before running the second task
timeout /t 30 /nobreak

:: Set the path to your Python executable
set PYTHON_PATH="C:\Users\JoshuaPaterson\AppData\Local\Programs\Python\Python312\python.exe"

:: Set the path to your Python script
set SCRIPT_PATH="C:\Users\JoshuaPaterson\OneDrive - Phibion Pty Ltd\Documents\GitHub\Dielectric-Antenna-V2\Megiq VNA Server\Python Server\mudmasterui\runserver.py"

:: Run the Python script
%PYTHON_PATH% %SCRIPT_PATH%

pause