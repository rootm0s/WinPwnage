from ctypes.wintypes import *
from ctypes import *
import enum

# Constants 
LPWSTR 	= c_wchar_p
LPVOID 	= c_void_p	
DWORD 	= c_uint32
SIZE_T  = c_size_t
PVOID   = c_void_p
LPTSTR  = c_void_p
LPBYTE  = c_char_p
LPCTSTR = c_char_p
LPDWORD = POINTER(DWORD)
PULONG  = POINTER(ULONG)
PHANDLE = POINTER(HANDLE)
PDWORD  = POINTER(DWORD)
SW_HIDE = 0
SW_SHOW = 5
MAX_PATH = 260
SEE_MASK_NOCLOSEPROCESS = 0x00000040

# Process constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = (0x0080 | 0x0002 | 0x0040 | 0x0400 | 0x1000 | 0x0200 | 0x0100 | 0x0800 | 0x0001 | 0x0008 | 0x0010 | 0x0020 | 0x00100000L)

# Token constants
TOKEN_ALL_ACCESS = (0x000F0000 | 0x0001| 0x0002| 0x0004| 0x00000008| 0x0010| 0x00000020| 0x0040| 0x0080 | 0x0100)
TOKEN_PRIVS = (0x00000008 | (0x00020000 | 0x00000008) | 0x0004  | 0x0010 | 0x0002 | 0x0001 | (131072L | 4))

class c_enum(enum.IntEnum):
    @classmethod
    def from_param(cls, obj):
        return c_int(cls(obj))

class LUID(Structure):
     _fields_ = [('LowPart', DWORD),
				('HighPart', LONG)]

class LUID_AND_ATTRIBUTES(Structure):
     _fields_ = [('Luid', LUID),
				('Attributes',DWORD)]
                                                
class TOKEN_PRIVILEGES(Structure):
	#Used by elevate_handle_inheritance module
     _fields_ = [('PrivilegeCount', DWORD),
				('Privileges', LUID_AND_ATTRIBUTES * 512)]

class TOKEN_PRIVILEGES2(Structure):
	#Used by elevate_token_impersonation module
   _fields_ = [('PrivilegeCount', DWORD),
				('Privileges', DWORD * 3)]	 

class TOKEN_INFORMATION_CLASS(c_enum):
     TokenUser = 1
     TokenElevation = 20
     TokenIntegrityLevel = 25

class PROC_THREAD_ATTRIBUTE_ENTRY(Structure):
    _fields_ = [("Attribute", DWORD),
				("cbSize", SIZE_T),
				("lpValue", PVOID)]

class PROC_THREAD_ATTRIBUTE_LIST(Structure):
    _fields_ = [("dwFlags", DWORD),
				("Size", ULONG),
				("Count", ULONG),
				("Reserved",ULONG),
				("Unknown", PULONG),
				("Entries", PROC_THREAD_ATTRIBUTE_ENTRY * 1)]

class STARTUPINFO(Structure):
    _fields_ = [
               ('cb', DWORD),
               ('lpReserved', LPTSTR),
               ('lpDesktop', LPTSTR),
               ('lpTitle', LPTSTR),
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
               ('lpReserved2', LPBYTE),
               ('hStdInput', HANDLE),
               ('hStdOutput', HANDLE),
               ('hStdError', HANDLE)
               ]

class STARTUPINFOEX(Structure):
    _fields_ = [('StartupInfo', STARTUPINFO),
				('lpAttributeList', LPVOID),]

class PROCESS_INFORMATION(Structure):                          
    _fields_ = [("hProcess", HANDLE),
				("hThread", HANDLE),
				("dwProcessId", DWORD),
				("dwThreadId", DWORD)]

class SID_AND_ATTRIBUTES(Structure):                           
    _fields_ = [('Sid', c_void_p),
				('Attributes', DWORD)]

class SECURITY_IMPERSONATION_LEVEL(c_int):
    SecurityAnonymous = 0
    SecurityIdentification = SecurityAnonymous + 1
    SecurityImpersonation = SecurityIdentification + 1
    SecurityDelegation = SecurityImpersonation + 1

class TOKEN_TYPE(c_enum):
	TokenPrimary = 1
	TokenImpersonation = 2

class TOKEN_USER(Structure):
    _fields_ = [('User', SID_AND_ATTRIBUTES),]

class TOKEN_MANDATORY_LABEL(Structure):
    _fields_ = [('Label', SID_AND_ATTRIBUTES),]	

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

class ShellExecuteInfoW(Structure):
	_fields_ = [
		('cbSize', DWORD),
		('fMask', c_ulong),
		('hwnd', HWND),
		('lpVerb', LPWSTR),
		('lpFile', LPWSTR),
		('lpParameters', LPWSTR),
		('lpDirectory', LPWSTR),
		('nShow', c_int),
		('hInstApp', HINSTANCE),
		('lpIDList', LPVOID),
		('lpClass', LPWSTR),
		('hKeyClass', HKEY),
		('dwHotKey', DWORD),
		('hIcon', HANDLE),
		('hProcess', HANDLE)
	]

PShellExecuteInfoW = POINTER(ShellExecuteInfoW)

# Load dlls
shell32 	= WinDLL('shell32', use_last_error=True)
kernel32 	= WinDLL('kernel32', use_last_error=True)
advapi32 	= WinDLL("advapi32", use_last_error=True)
psapi 		= WinDLL('psapi', use_last_error=True)
ntdll		= WinDLL("ntdll", use_last_error=True)

# Functions
ShellExecuteEx = shell32.ShellExecuteExW
ShellExecuteEx.argtypes = [PShellExecuteInfoW]
ShellExecuteEx.restype = BOOL

OpenProcess = kernel32.OpenProcess
OpenProcess.restype = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [LPVOID]
CloseHandle.restype = c_int

QueryFullProcessImageNameW = kernel32.QueryFullProcessImageNameW
QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, LPWSTR, POINTER(DWORD)]
QueryFullProcessImageNameW.restype = BOOL

GetLastError = windll.kernel32.GetLastError 
GetLastError.restype = DWORD 

TerminateProcess = kernel32.TerminateProcess
TerminateProcess.restype = BOOL
TerminateProcess.argtypes = [HANDLE, UINT]

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.restype = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]

NtOpenProcessToken = ntdll.NtOpenProcessToken
NtOpenProcessToken.restype = BOOL
NtOpenProcessToken.argtypes = [HANDLE, DWORD, PHANDLE]

NTSTATUS = c_ulong
STATUS_UNSUCCESSFUL = NTSTATUS(0xC0000001)
NtSetInformationToken = ntdll.NtSetInformationToken
NtSetInformationToken.restype = NTSTATUS
NtSetInformationToken.argtypes = [ HANDLE, TOKEN_INFORMATION_CLASS, c_void_p, ULONG]

RtlAllocateAndInitializeSid = ntdll.RtlAllocateAndInitializeSid
RtlAllocateAndInitializeSid.restype = BOOL
RtlAllocateAndInitializeSid.argtypes = [POINTER(SID_IDENTIFIER_AUTHORITY), BYTE, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPVOID]

NtFilterToken = ntdll.NtFilterToken
NtFilterToken.restype = NTSTATUS
NtFilterToken.argtypes = [HANDLE, ULONG, LPVOID, LPVOID, LPVOID, PHANDLE]

CreateProcessWithLogonW = advapi32.CreateProcessWithLogonW
CreateProcessWithLogonW.restype	= BOOL
CreateProcessWithLogonW.argtypes = [LPCWSTR, LPCWSTR, LPCWSTR, DWORD, LPCWSTR, LPWSTR, DWORD, LPVOID, LPCWSTR, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]  

GetCurrentProcess = kernel32.GetCurrentProcess 
GetCurrentProcess.restype = HANDLE

OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL
OpenProcessToken.argtypes = [HANDLE, DWORD, POINTER(HANDLE)]

GetCurrentProcessId = kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD

GetCurrentThread = kernel32.GetCurrentThread                                          
GetCurrentThread.restype = HANDLE

LookupPrivilegeValue = advapi32.LookupPrivilegeValueW   
LookupPrivilegeValue.restype = BOOL
LookupPrivilegeValue.argtypes = [LPWSTR, LPWSTR, POINTER(LUID)]

AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.restype = BOOL
AdjustTokenPrivileges.argtypes = [HANDLE, BOOL, c_void_p, DWORD, c_void_p, POINTER(DWORD)]	

EnumProcesses = psapi.EnumProcesses
EnumProcesses.argtypes = [LPVOID, DWORD, LPDWORD]
EnumProcesses.restype = BOOL

GetProcessImageFileName = psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = DWORD
GetProcessImageFileName.argtypes = [HANDLE, c_char_p, DWORD]

InitializeProcThreadAttributeList = kernel32.InitializeProcThreadAttributeList
InitializeProcThreadAttributeList.restype = BOOL
InitializeProcThreadAttributeList.argtypes = [POINTER(PROC_THREAD_ATTRIBUTE_LIST), DWORD, DWORD, POINTER(SIZE_T)]                                                       

UpdateProcThreadAttribute = kernel32.UpdateProcThreadAttribute
UpdateProcThreadAttribute.restype = BOOL
UpdateProcThreadAttribute.argtypes = [POINTER(PROC_THREAD_ATTRIBUTE_LIST),DWORD, DWORD, PVOID, SIZE_T, PVOID, POINTER(SIZE_T)]

CreateProcess = kernel32.CreateProcessW
CreateProcess.restype = BOOL 
CreateProcess.argtypes = [LPCWSTR, LPWSTR, LPVOID, LPVOID, BOOL, DWORD, LPVOID, LPCWSTR, POINTER(STARTUPINFOEX), POINTER(PROCESS_INFORMATION)]

DeleteProcThreadAttributeList = kernel32.DeleteProcThreadAttributeList              
DeleteProcThreadAttributeList.restype = None
DeleteProcThreadAttributeList.argtypes = [POINTER(PROC_THREAD_ATTRIBUTE_LIST)] 

GetTokenInformation = advapi32.GetTokenInformation
GetTokenInformation.restype =  BOOL
GetTokenInformation.argtypes = [HANDLE, c_int, c_void_p, DWORD, PDWORD]

ConvertSidToStringSidA = advapi32.ConvertSidToStringSidA
ConvertSidToStringSidA.restype = BOOL
ConvertSidToStringSidA.argtypes = [c_void_p, c_void_p]

DuplicateTokenEx = advapi32.DuplicateTokenEx
DuplicateTokenEx.restype  = BOOL
DuplicateTokenEx.argtypes = [HANDLE, DWORD, c_void_p, SECURITY_IMPERSONATION_LEVEL, TOKEN_TYPE, PHANDLE]                                                                    

ImpersonateLoggedOnUser = advapi32.ImpersonateLoggedOnUser
ImpersonateLoggedOnUser.restype = BOOL
ImpersonateLoggedOnUser.argtypes = [HANDLE]

CreateProcessWithToken = advapi32.CreateProcessWithTokenW                           
CreateProcessWithToken.restype = BOOL                                               
CreateProcessWithToken.argtypes = [HANDLE, DWORD, LPCWSTR, LPWSTR, DWORD, LPCWSTR, LPCWSTR, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]

OpenSCManager = advapi32.OpenSCManagerA
OpenSCManager.restype = SC_HANDLE
OpenSCManager.argtypes = [LPCTSTR, LPCTSTR, DWORD]
		
CreateService = advapi32.CreateServiceA
CreateService.restype = SC_HANDLE
CreateService.argtypes = [SC_HANDLE, LPCTSTR, LPCTSTR, DWORD, DWORD, DWORD, DWORD, LPCTSTR, LPCTSTR, LPDWORD, LPCTSTR, LPCTSTR, LPCTSTR]

OpenService = advapi32.OpenServiceA
OpenService.restype = SC_HANDLE
OpenService.argtypes = [SC_HANDLE, LPCTSTR, DWORD]

StartService = advapi32.StartServiceA
StartService.restype = bool
StartService.argtypes = [SC_HANDLE, DWORD, LPCTSTR]

DeleteService = advapi32.DeleteService
DeleteService.restype = bool
DeleteService.argtypes = [SC_HANDLE]

CloseServiceHandle = advapi32.CloseServiceHandle
CloseServiceHandle.restype = SC_HANDLE
CloseServiceHandle.argtypes = [SC_HANDLE]

CreateThread = kernel32.CreateThread                                           
CreateThread.restype = HANDLE                                                      
CreateThread.argtypes = [LPVOID, SIZE_T, LPVOID, LPVOID, DWORD, LPDWORD]

CreateNamedPipe = kernel32.CreateNamedPipeA
CreateNamedPipe.restype = HANDLE
CreateNamedPipe.argtypes = [LPCTSTR, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPVOID]

ConnectNamedPipe = kernel32.ConnectNamedPipe
ConnectNamedPipe.restype = bool
ConnectNamedPipe.argtypes = [HANDLE, LPVOID]

ReadFile = kernel32.ReadFile
ReadFile.restype = bool
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPVOID]

ImpersonateNamedPipeClient = advapi32.ImpersonateNamedPipeClient
ImpersonateNamedPipeClient.restype = bool
ImpersonateNamedPipeClient.argtypes = [HANDLE]

OpenThreadToken = advapi32.OpenThreadToken
OpenThreadToken.restype = bool
OpenThreadToken.argtypes = [HANDLE, DWORD, BOOL, PHANDLE]

CreateProcessAsUser = advapi32.CreateProcessAsUserA                                  
CreateProcessAsUser.restype = bool                                                 
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
