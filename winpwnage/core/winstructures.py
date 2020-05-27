from ctypes.wintypes import *
from ctypes import *
import ctypes
import enum

# Wintypes
INT = c_int
LPWSTR = c_wchar_p
LPVOID = c_void_p
LPCSTR =  c_char_p
DWORD = c_uint32
SIZE_T = c_size_t
PVOID = c_void_p
LPTSTR = c_void_p
LPBYTE = c_char_p
LPCTSTR = c_char_p
NTSTATUS = c_ulong
LPDWORD = POINTER(DWORD)
PULONG = POINTER(ULONG)
PHANDLE = POINTER(HANDLE)
PDWORD = POINTER(DWORD)

# Misc constants
SW_HIDE = 0
SW_SHOW = 5
MAX_PATH = 260
SEE_MASK_NOCLOSEPROCESS = 0x00000040
STATUS_UNSUCCESSFUL = ULONG(0xC0000001)

# Process constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = (0x0080 | 0x0002 | 0x0040 | 0x0400 | 0x1000 | 0x0200 | 0x0100 | 0x0800 | 0x0001 | 0x0008 | 0x0010 | 0x0020 | 0x00100000)

# Token constants
TOKEN_DUPLICATE = 0x0002
TOKEN_QUERY = 0x00000008
TOKEN_ADJUST_PRIVILEGES  = 0x00000020
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_ALL_ACCESS = (0x000F0000 | 0x0001 | 0x0002 | 0x0004 | 0x00000008 | 0x0010 | 0x00000020 | 0x0040 | 0x0080 | 0x0100)
TOKEN_PRIVS = (0x00000008 | (0x00020000 | 0x00000008) | 0x0004 | 0x0010 | 0x0002 | 0x0001 | (131072 | 4))
TOKEN_WRITE = (0x00020000 | 0x0020 | 0x0040 | 0x0080)

class c_enum(enum.IntEnum):
	@classmethod
	def from_param(cls, obj):
		return c_int(cls(obj))

class TOKEN_INFORMATION_CLASS(c_enum):
	""" https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class """
	TokenUser = 1
	TokenElevation = 20
	TokenIntegrityLevel = 25

class TOKEN_TYPE(c_enum):
	""" https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_type """
	TokenPrimary = 1
	TokenImpersonation = 2

class SECURITY_IMPERSONATION_LEVEL(INT):
	""" https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level """
	SecurityAnonymous = 0
	SecurityIdentification = SecurityAnonymous + 1
	SecurityImpersonation = SecurityIdentification + 1
	SecurityDelegation = SecurityImpersonation + 1

class IntegrityLevel(object):
	""" https://docs.microsoft.com/en-us/windows/win32/secauthz/well-known-sids """
	SECURITY_MANDATORY_UNTRUSTED_RID = 0x00000000
	SECURITY_MANDATORY_LOW_RID = 0x00001000
	SECURITY_MANDATORY_MEDIUM_RID = 0x00002000
	SECURITY_MANDATORY_MEDIUM_PLUS_RID = SECURITY_MANDATORY_MEDIUM_RID + 0x100
	SECURITY_MANDATORY_HIGH_RID = 0X00003000
	SECURITY_MANDATORY_SYSTEM_RID = 0x00004000
	SECURITY_MANDATORY_PROTECTED_PROCESS_RID = 0x00005000	

class GroupAttributes(object):
	""" https://msdn.microsoft.com/en-us/windows/desktop/aa379624"""
	SE_GROUP_ENABLED = 0x00000004
	SE_GROUP_ENABLED_BY_DEFAULT = 0x00000002 
	SE_GROUP_INTEGRITY = 0x00000020         
	SE_GROUP_INTEGRITY_ENABLED = 0x00000040
	SE_GROUP_LOGON_ID = 0xC0000000 
	SE_GROUP_MANDATORY = 0x00000001 
	SE_GROUP_OWNER = 0x00000008   
	SE_GROUP_RESOURCE = 0x20000000 
	SE_GROUP_USE_FOR_DENY_ONLY = 0x00000010 
	
class LUID(Structure):
	""" https://msdn.microsoft.com/en-us/windows/desktop/dd316552 """
	_fields_ = [
				("LowPart", DWORD),
				("HighPart", LONG)
				]

class LUID_AND_ATTRIBUTES(Structure):
	""" https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/content/wdm/ns-wdm-_luid_and_attributes """
	_fields_ = [
				("Luid", LUID),
				("Attributes", DWORD)
				]
                                                
class TOKEN_PRIVILEGES(Structure):
	"""
	https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_privileges
	Used by elevate_handle_inheritance module
	"""
	_fields_ = [
				("PrivilegeCount", DWORD),
				("Privileges", LUID_AND_ATTRIBUTES * 512)
				]

class TOKEN_PRIVILEGES2(Structure):
	"""
	https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_privileges
	Used by elevate_token_impersonation module
	"""
	_fields_ = [
				("PrivilegeCount", DWORD),
				("Privileges", DWORD * 3)
				]

class PROC_THREAD_ATTRIBUTE_ENTRY(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute """
	_fields_ = [
				("Attribute", DWORD),
				("cbSize", SIZE_T),
				("lpValue", PVOID)
				]

class PROC_THREAD_ATTRIBUTE_LIST(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute """
	_fields_ = [
				("dwFlags", DWORD),
				("Size", ULONG),
				("Count", ULONG),
				("Reserved", ULONG),
				("Unknown", PULONG),
				("Entries", PROC_THREAD_ATTRIBUTE_ENTRY * 1)
				]

class STARTUPINFO(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoa """
	_fields_ = [
				("cb", DWORD),
				("lpReserved", LPTSTR),
				("lpDesktop", LPTSTR),
				("lpTitle", LPTSTR),
				("dwX", DWORD),
				("dwY", DWORD),
				("dwXSize", DWORD),
				("dwYSize", DWORD),
				("dwXCountChars", DWORD),
				("dwYCountChars", DWORD),
				("dwFillAttribute", DWORD),
				("dwFlags", DWORD),
				("wShowWindow", WORD),
				("cbReserved2", WORD),
				("lpReserved2", LPBYTE),
				("hStdInput", HANDLE),
				("hStdOutput", HANDLE),
				("hStdError", HANDLE)
				]

class STARTUPINFOEX(Structure):
	""" https://msdn.microsoft.com/en-us/windows/desktop/ms686329 """
	_fields_ = [
				("StartupInfo", STARTUPINFO),
				("lpAttributeList", LPVOID)
				]

class PROCESS_INFORMATION(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information """
	_fields_ = [
				("hProcess", HANDLE),
				("hThread", HANDLE),
				("dwProcessId", DWORD),
				("dwThreadId", DWORD)
				]

class SID_AND_ATTRIBUTES(Structure):
	""" https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/content/ntifs/ns-ntifs-_sid_and_attributes """
	_fields_ = [
				("Sid", LPVOID),
				("Attributes", DWORD)
				]

class TOKEN_USER(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_user """
	_fields_ = [
				("User", SID_AND_ATTRIBUTES)
				]

class TOKEN_MANDATORY_LABEL(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_mandatory_label """
	_fields_ = [
				("Label", SID_AND_ATTRIBUTES)
				]

class SECURITY_ATTRIBUTES(Structure): 
	""" https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/aa379560(v=vs.85) """
	_fields_ = [
				("nLength", DWORD),
				("lpSecurityDescriptor", LPVOID),                
				("bInheritHandle", BOOL)
				]

class SID_IDENTIFIER_AUTHORITY(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-sid_identifier_authority """
	_fields_ = [
				("Value",
				BYTE * 6)
				]

class ShellExecuteInfoW(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-shellexecuteinfow """
	_fields_ = [
				("cbSize", DWORD),
				("fMask", ULONG),
				("hwnd", HWND),
				("lpVerb", LPWSTR),
				("lpFile", LPWSTR),
				("lpParameters", LPWSTR),
				("lpDirectory", LPWSTR),
				("nShow", INT),
				("hInstApp", HINSTANCE),
				("lpIDList", LPVOID),
				("lpClass", LPWSTR),
				("hKeyClass", HKEY),
				("dwHotKey", DWORD),
				("hIcon", HANDLE),
				("hProcess", HANDLE)
				]

#https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-shellexecuteexw
ShellExecuteEx = ctypes.windll.shell32.ShellExecuteExW
ShellExecuteEx.argtypes	= [POINTER(ShellExecuteInfoW)]
ShellExecuteEx.restype	= BOOL

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-openprocess
OpenProcess = ctypes.windll.kernel32.OpenProcess
OpenProcess.restype	 = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/handleapi/nf-handleapi-closehandle
CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = [LPVOID]
CloseHandle.restype	 = INT

#https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-queryfullprocessimagenamew
QueryFullProcessImageNameW = ctypes.windll.kernel32.QueryFullProcessImageNameW
QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, LPWSTR, POINTER(DWORD)]
QueryFullProcessImageNameW.restype 	= BOOL

#https://msdn.microsoft.com/en-us/library/windows/desktop/ms679360(v=vs.85).aspx
GetLastError = ctypes.windll.kernel32.GetLastError 
GetLastError.restype = DWORD 

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-terminateprocess
TerminateProcess = ctypes.windll.kernel32.TerminateProcess
TerminateProcess.restype  = BOOL
TerminateProcess.argtypes = [HANDLE, UINT]

#https://docs.microsoft.com/en-us/windows/desktop/api/synchapi/nf-synchapi-waitforsingleobject
WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
WaitForSingleObject.restype  = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]

#https://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FToken%2FNtOpenProcessToken.html
NtOpenProcessToken = ctypes.windll.ntdll.NtOpenProcessToken
NtOpenProcessToken.restype  = BOOL
NtOpenProcessToken.argtypes = [HANDLE, DWORD, PHANDLE]

#https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/content/ntifs/nf-ntifs-ntsetinformationtoken
NtSetInformationToken = ctypes.windll.ntdll.NtSetInformationToken
NtSetInformationToken.restype  = NTSTATUS
NtSetInformationToken.argtypes = [HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, ULONG]

#https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/content/ntifs/nf-ntifs-rtlallocateandinitializesid
RtlAllocateAndInitializeSid = ctypes.windll.ntdll.RtlAllocateAndInitializeSid
RtlAllocateAndInitializeSid.restype  = BOOL
RtlAllocateAndInitializeSid.argtypes = [POINTER(SID_IDENTIFIER_AUTHORITY), BYTE, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPVOID]

#http://www.codewarrior.cn/ntdoc/wrk/se/NtFilterToken.htm
NtFilterToken = ctypes.windll.ntdll.NtFilterToken
NtFilterToken.restype = NTSTATUS
NtFilterToken.argtypes = [HANDLE, ULONG, LPVOID, LPVOID, LPVOID, PHANDLE]

#https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-createprocesswithlogonw
CreateProcessWithLogonW = ctypes.windll.advapi32.CreateProcessWithLogonW
CreateProcessWithLogonW.restype = BOOL
CreateProcessWithLogonW.argtypes = [LPCWSTR, LPCWSTR, LPCWSTR, DWORD, LPCWSTR, LPWSTR, DWORD, LPVOID, LPCWSTR, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]  

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess
GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess 
GetCurrentProcess.restype = HANDLE

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
OpenProcessToken = ctypes.windll.advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL
OpenProcessToken.argtypes = [HANDLE, DWORD, POINTER(HANDLE)]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-getcurrentprocessid
GetCurrentProcessId = ctypes.windll.kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-getcurrentthread
GetCurrentThread = ctypes.windll.kernel32.GetCurrentThread
GetCurrentThread.restype = HANDLE

#https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-lookupprivilegevaluew
LookupPrivilegeValue = ctypes.windll.advapi32.LookupPrivilegeValueW 
LookupPrivilegeValue.restype = BOOL
LookupPrivilegeValue.argtypes = [LPWSTR, LPWSTR, POINTER(LUID)]

#https://docs.microsoft.com/en-us/windows/desktop/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges
AdjustTokenPrivileges = ctypes.windll.advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.restype = BOOL
AdjustTokenPrivileges.argtypes = [HANDLE, BOOL, LPVOID, DWORD, LPVOID, POINTER(DWORD)]	

#https://docs.microsoft.com/en-us/windows/desktop/api/psapi/nf-psapi-enumprocesses
EnumProcesses = ctypes.windll.psapi.EnumProcesses
EnumProcesses.restype = BOOL
EnumProcesses.argtypes = [LPVOID, DWORD, LPDWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/psapi/nf-psapi-getprocessimagefilenamea
GetProcessImageFileName = ctypes.windll.psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = DWORD
GetProcessImageFileName.argtypes = [HANDLE, LPBYTE, DWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-initializeprocthreadattributelist
InitializeProcThreadAttributeList = ctypes.windll.kernel32.InitializeProcThreadAttributeList     
InitializeProcThreadAttributeList.restype = BOOL
InitializeProcThreadAttributeList.argtypes = [POINTER(PROC_THREAD_ATTRIBUTE_LIST), DWORD, DWORD, POINTER(SIZE_T)]                                                       

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute
UpdateProcThreadAttribute = ctypes.windll.kernel32.UpdateProcThreadAttribute
UpdateProcThreadAttribute.restype = BOOL
UpdateProcThreadAttribute.argtypes = [POINTER(PROC_THREAD_ATTRIBUTE_LIST), DWORD, DWORD, PVOID, SIZE_T, PVOID, POINTER(SIZE_T)]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-createprocessw
CreateProcess = ctypes.windll.kernel32.CreateProcessW
CreateProcess.restype = BOOL 
CreateProcess.argtypes = [LPCWSTR, LPWSTR, LPVOID, LPVOID, BOOL, DWORD, LPVOID, LPCWSTR, POINTER(STARTUPINFOEX), POINTER(PROCESS_INFORMATION)]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-deleteprocthreadattributelist
DeleteProcThreadAttributeList = ctypes.windll.kernel32.DeleteProcThreadAttributeList             
DeleteProcThreadAttributeList.restype = None
DeleteProcThreadAttributeList.argtypes = [POINTER(PROC_THREAD_ATTRIBUTE_LIST)] 

#https://docs.microsoft.com/en-us/windows/desktop/api/securitybaseapi/nf-securitybaseapi-gettokeninformation
GetTokenInformation = ctypes.windll.advapi32.GetTokenInformation
GetTokenInformation.restype =  BOOL
GetTokenInformation.argtypes = [HANDLE, INT, LPVOID, DWORD, PDWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/sddl/nf-sddl-convertsidtostringsida
ConvertSidToStringSidA = ctypes.windll.advapi32.ConvertSidToStringSidA
ConvertSidToStringSidA.restype = BOOL
ConvertSidToStringSidA.argtypes = [LPVOID, LPVOID]

#https://docs.microsoft.com/en-us/windows/desktop/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex
DuplicateTokenEx = ctypes.windll.advapi32.DuplicateTokenEx
DuplicateTokenEx.restype = BOOL
DuplicateTokenEx.argtypes = [HANDLE, DWORD, LPVOID, SECURITY_IMPERSONATION_LEVEL, TOKEN_TYPE, PHANDLE]                                                                    

#https://docs.microsoft.com/en-us/windows/desktop/api/securitybaseapi/nf-securitybaseapi-impersonateloggedonuser
ImpersonateLoggedOnUser = ctypes.windll.advapi32.ImpersonateLoggedOnUser
ImpersonateLoggedOnUser.restype = BOOL
ImpersonateLoggedOnUser.argtypes = [HANDLE]

#https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-createprocesswithtokenw
CreateProcessWithToken = ctypes.windll.advapi32.CreateProcessWithTokenW                     
CreateProcessWithToken.restype = BOOL                                               
CreateProcessWithToken.argtypes = [HANDLE, DWORD, LPCWSTR, LPWSTR, DWORD, LPCWSTR, LPCWSTR, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]

#https://docs.microsoft.com/en-us/windows/desktop/api/winsvc/nf-winsvc-openscmanagera
OpenSCManager = ctypes.windll.advapi32.OpenSCManagerA
OpenSCManager.restype = SC_HANDLE
OpenSCManager.argtypes = [LPCSTR, LPCSTR, DWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/winsvc/nf-winsvc-createservicea	
CreateService = ctypes.windll.advapi32.CreateServiceA
CreateService.restype = SC_HANDLE
CreateService.argtypes = [SC_HANDLE, LPCTSTR, LPCTSTR, DWORD, DWORD, DWORD, DWORD, LPCTSTR, LPCTSTR, LPDWORD, LPCTSTR, LPCTSTR, LPCTSTR]

#https://docs.microsoft.com/en-us/windows/desktop/api/winsvc/nf-winsvc-openservicea
OpenService = ctypes.windll.advapi32.OpenServiceA
OpenService.restype = SC_HANDLE
OpenService.argtypes = [SC_HANDLE, LPCTSTR, DWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/winsvc/nf-winsvc-startservicea
StartService = ctypes.windll.advapi32.StartServiceA
StartService.restype = BOOL
StartService.argtypes = [SC_HANDLE, DWORD, LPCTSTR]

#https://docs.microsoft.com/en-us/windows/desktop/api/winsvc/nf-winsvc-deleteservice
DeleteService = ctypes.windll.advapi32.DeleteService
DeleteService.restype = BOOL
DeleteService.argtypes = [SC_HANDLE]

#https://docs.microsoft.com/en-us/windows/desktop/api/winsvc/nf-winsvc-closeservicehandle
CloseServiceHandle = ctypes.windll.advapi32.CloseServiceHandle
CloseServiceHandle.restype = SC_HANDLE
CloseServiceHandle.argtypes = [SC_HANDLE]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-createthread
CreateThread = ctypes.windll.kernel32.CreateThread
CreateThread.restype = HANDLE
CreateThread.argtypes = [LPVOID, SIZE_T, LPVOID, LPVOID, DWORD, LPDWORD]

#https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-createnamedpipea
CreateNamedPipe = ctypes.windll.kernel32.CreateNamedPipeA
CreateNamedPipe.restype = HANDLE
CreateNamedPipe.argtypes = [LPCSTR, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPVOID]

#https://msdn.microsoft.com/en-us/library/windows/desktop/aa365146(v=vs.85).aspx
ConnectNamedPipe = ctypes.windll.kernel32.ConnectNamedPipe
ConnectNamedPipe.restype = BOOL
ConnectNamedPipe.argtypes = [HANDLE, LPVOID]

#https://docs.microsoft.com/en-us/windows/desktop/api/fileapi/nf-fileapi-readfile
ReadFile = ctypes.windll.kernel32.ReadFile
ReadFile.restype = BOOL
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPVOID]

#https://msdn.microsoft.com/en-us/library/windows/desktop/aa378618(v=vs.85).aspx
ImpersonateNamedPipeClient = ctypes.windll.advapi32.ImpersonateNamedPipeClient
ImpersonateNamedPipeClient.restype = BOOL
ImpersonateNamedPipeClient.argtypes = [HANDLE]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-openthreadtoken
OpenThreadToken = ctypes.windll.advapi32.OpenThreadToken
OpenThreadToken.restype = BOOL
OpenThreadToken.argtypes = [HANDLE, DWORD, BOOL, PHANDLE]

#https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-createprocessasusera
CreateProcessAsUser = ctypes.windll.advapi32.CreateProcessAsUserA
CreateProcessAsUser.restype = BOOL
CreateProcessAsUser.argtypes = [HANDLE, LPCTSTR, LPTSTR, LPVOID, LPVOID, BOOL, DWORD, LPVOID, LPCTSTR, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]

def get_process_name(hProcess, dwFlags = 0):
	ERROR_INSUFFICIENT_BUFFER = 122
	dwSize = MAX_PATH
	while 1:
		lpdwSize = DWORD(dwSize)
		lpExeName = create_unicode_buffer('', lpdwSize.value + 1)
		success = QueryFullProcessImageNameW(hProcess, dwFlags, lpExeName, byref(lpdwSize))
		if success and 0 < lpdwSize.value < dwSize:
			break
		error = GetLastError()
		if error != ERROR_INSUFFICIENT_BUFFER:
			return False
		dwSize = dwSize + 256
		if dwSize > 0x1000:
			# this prevents an infinite loop in Windows 2008 when the path has spaces,
			# see http://msdn.microsoft.com/en-us/library/ms684919(VS.85).aspx#4
			return False
	return lpExeName.value
