# WinPwn

#### admin_to_system.py
> schtasks to elevate our process and gain persistence on the system with the /SC ONLOGON switch. The /RU SYSTEM command will run the process invisible since we're not SYSTEM. The process will spawn and work as we want to, just that we can't see it.

#### fax_dll_hijack.py
> This is a simple DLL hijacking attack that we have successfully tested against Windows XP,Vista and 7. A DLL named fxsst.dll normally resides in \Windows\System32 and is loaded by explorer.exe. Placing a new DLL with this name in \Windows results in this being loaded into explorer instead of the original DLL. On Windows Vista and above, the DLL's reference count must be increased by calling LoadLibrary on itself to avoid being unloaded. This achieves persistence, stealth and in some cases PSP avoidance.
