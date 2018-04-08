# 💻 WinPwn

For educational use only!

#### Modules used:
    os,requests,psutil,_winreg

##### admin_to_system.py
> schtasks to elevate our process and gain persistence on the system with the /SC ONLOGON switch. The /RU SYSTEM command will run the process invisible since we're not SYSTEM. The process will spawn and work as we want to, just that we can't see it.

##### fax_dll_hijack.py
> This is a simple DLL hijacking attack that we have successfully tested against Windows XP,Vista and 7. A DLL named fxsst.dll normally resides in \Windows\System32 and is loaded by explorer.exe. Placing a new DLL with this name in \Windows results in this being loaded into explorer instead of the original DLL. On Windows Vista and above, the DLL's reference count must be increased by calling LoadLibrary on itself to avoid being unloaded. This achieves persistence, stealth and in some cases PSP avoidance.

##### fodhelper_dll_hijack.py
> This script is a proof of concept to bypass the User Access Control (UAC) via fodhelper.exe. Fodhelper.exe was introduced in Windows 10 to manage optional features like region-specific keyboard settings. Its location is: C:\Windows\System32\fodhelper.exe and it is signed by Microsoft, we use it to elevate from user to admin.

##### image_file_execution.py
> Registry key that was designed to assist with debugging and allows the user to specifiy an executable that should be run instead of the specified application.

##### oci_dll_hijack.py
> Windows contains a service called "Distributed Transaction Coordinator" that is configured to "Manual" start by default. This service causes a DLL called "C:\Windows\System32\wbem\oci.dll" to load into the "Network Services" group. By placing our own DLL in this location and configuring the service to start automatially, we have a persistence mechanism with system privileges. The service runs under the "Network Service" account, which is a restricted account that has privileges to access the network.

##### slui_file_hijack.py
> slui.exe is an auto-elevated binary that is vulnerable to file handler hijacking Read access to HKCU\Software\Classes\exefile\shell\open is performed upon execution. Due to the registry key being accessible from user mode, an arbitrary executable file can be provided.

#### Read:
* https://wikileaks.org/ciav7p1/cms/page_2621770.html
* https://wikileaks.org/ciav7p1/cms/page_2621767.html
* https://wikileaks.org/ciav7p1/cms/page_2621760.html
* https://msdn.microsoft.com/en-us/library/windows/desktop/bb736357(v=vs.85).aspx
* https://winscripting.blog/2017/05/12/first-entry-welcome-and-uac-bypass/
* https://github.com/winscripting/UAC-bypass/
