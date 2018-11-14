from ctypes import (
	WinDLL, WinError, GetLastError, Structure, POINTER, 
	c_wchar_p, c_uint32, c_void_p, c_ulong, c_int, 
	sizeof, byref, create_unicode_buffer, 
)

from ctypes.wintypes import (
	BOOL, LPSTR, BYTE, HWND, HANDLE, HKEY, HINSTANCE
)

# Constants 
LPWSTR 	= c_wchar_p
LPVOID 	= c_void_p	
DWORD 	= c_uint32
LPDWORD = POINTER(DWORD)
SW_HIDE = 0
SW_SHOW = 5
MAX_PATH 	= 260
SEE_MASK_NOCLOSEPROCESS = 0x00000040
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010


class ShellExecuteInfoW(Structure):
	_fields_ = [
		('cbSize',          DWORD),
		('fMask',           c_ulong),
		('hwnd',            HWND),
		('lpVerb',          LPWSTR),
		('lpFile',          LPWSTR),
		('lpParameters',    LPWSTR),
		('lpDirectory',     LPWSTR),
		('nShow',           c_int),
		('hInstApp',        HINSTANCE),
		('lpIDList',        LPVOID),
		('lpClass',         LPWSTR),
		('hKeyClass',       HKEY),
		('dwHotKey',        DWORD),
		('hIcon',           HANDLE),
		('hProcess',        HANDLE)
	]
PShellExecuteInfoW = POINTER(ShellExecuteInfoW)

# Load dlls
shell32 	= WinDLL('shell32', use_last_error=True)
kernel32 	= WinDLL('kernel32', use_last_error=True)
psapi 		= WinDLL('psapi', use_last_error=True)

# Functions
ShellExecuteEx 			= shell32.ShellExecuteExW
ShellExecuteEx.argtypes = [PShellExecuteInfoW]
ShellExecuteEx.restype 	= BOOL

OpenProcess 			= kernel32.OpenProcess
OpenProcess.restype 	= HANDLE
OpenProcess.argtypes 	= [DWORD, BOOL, DWORD]

CloseHandle 			= kernel32.CloseHandle
CloseHandle.argtypes 	= [LPVOID]
CloseHandle.restype 	= c_int

EnumProcesses 			= psapi.EnumProcesses
EnumProcesses.argtypes 	= [LPVOID, DWORD, LPDWORD]
EnumProcesses.restype 	= BOOL

QueryFullProcessImageNameW 			= kernel32.QueryFullProcessImageNameW
QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, LPWSTR, POINTER(DWORD)]
QueryFullProcessImageNameW.restype  = BOOL


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
