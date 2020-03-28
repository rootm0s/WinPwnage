# WinPwnage

[![xd](https://travis-ci.com/rootm0s/WinPwnage.svg?branch=master)](https://travis-ci.com/rootm0s/WinPwnage)
![xd](https://img.shields.io/badge/Python-2-blue.svg "Python 2")
![xd](https://img.shields.io/badge/Python-3-blue.svg "Python 3")

The goal of this repo is to study the Windows penetration techniques. Techniques are found online, on different blogs and repos here on GitHub. I do not take credit for any of the findings, thanks to all the researchers.

## UAC bypass techniques:
* UAC bypass using runas
    * Id: 1
    * Method: Windows API, this only works if UAC is set to never notify
    * Syntax: `winpwnage.py --use uac --id 1 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in:	n/a
* UAC bypass using fodhelper.exe
    * Id: 2
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 2 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: n/a
* UAC bypass using slui.exe
    * Id: 3
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 3 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 9600
	* Fixed in: n/a
* UAC bypass using silentcleanup scheduled task
    * Id: 4
    * Method: Registry key (Environment) manipulation, this bypasses UAC's Always Notify.
    * Syntax: `winpwnage.py --use uac --id 4 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 9600
	* Fixed in: n/a
* UAC bypass using sdclt.exe (isolatedcommand)
    * Id: 5
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 5 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: 17025
* UAC bypass using sdclt.exe (App Paths)
    * Id: 6
    * Method: Registry key (App Paths) manipulation
    * Syntax: `winpwnage.py --use uac --id 6 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: 16215
* UAC bypass using perfmon.exe
    * Id: 7
    * Method: Registry key (Volatile Environment) manipulation
    * Syntax: `winpwnage.py --use uac --id 7 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 16299
* UAC bypass using eventvwr.exe
    * Id: 8
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 8 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 15031
* UAC bypass using compmgmtlauncher.exe
    * Id: 9
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 9 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 15031	
* UAC bypass using computerdefaults.exe
    * Id: 10
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 10 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: n/a
* UAC bypass using cliconfg.exe (DLL payload only)
    * Id: 11
    * Method: DLL hijack using makecab and wusa
    * Syntax: `winpwnage.py --use uac --id 11 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 9800
* UAC bypass using mcx2prov.exe (DLL payload only)
    * Id: 12
    * Method: DLL hijack using makecab and wusa
    * Syntax: `winpwnage.py --use uac --id 12 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 10147
* UAC bypass using migwiz.exe (DLL payload only)
    * Id: 13
    * Method: DLL hijack using makecab and wusa
    * Syntax: `winpwnage.py --use uac --id 13 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 10147	
* UAC bypass using sysprep.exe (DLL payload only)
    * Id: 14
    * Method: DLL hijack using makecab and wusa
    * Syntax: `winpwnage.py --use uac --id 14 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 9600
* UAC bypass using token manipulation
    * Id: 15
    * Method: Token manipulation
    * Syntax: `winpwnage.py --use uac --id 15 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 17686
* UAC bypass using sdclt.exe (Folder)
    * Id: 16
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 16 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 14393
	* Fixed in: n/a
* UAC bypass using cmstp.exe
    * Id: 17
    * Method: Malicious ini file
    * Syntax: `winpwnage.py --use uac --id 16 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: n/a
* UAC bypass using .NET Code Profiler (DLL payload only)
    * Id: 18
    * Method: Registry key (Class) manipulation and DLL hijack
    * Syntax: `winpwnage.py --use uac --id 18 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: n/a
* UAC bypass using mocking trusted directories (DLL payload only)
    * Id: 19
    * Method: Mock SystemRoot directory and DLL hijack
    * Syntax: `winpwnage.py --use uac --id 19 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: n/a
* UAC bypass using wsreset.exe
    * Id: 20
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use uac --id 19 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 17134
	* Fixed in: n/a

## Persistence techniques:
* Persistence using explorer.exe (DLL payload only)
    * Id: 1
    * Method: DLL hijack using makecab and wusa
    * Syntax: `winpwnage.py --use persist --id 1 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: 9800
* Persistence using mofcomp.exe (SYSTEM privileges)
    * Id: 2
    * Method: Malicious mof file using EventFilter EventConsumer and binding
    * Syntax: `winpwnage.py --use persist --id 2 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a		
* Persistence using schtasks.exe (SYSTEM privileges)
    * Id: 3
    * Method: Malicious scheduled task
    * Syntax: `winpwnage.py --use persist --id 3 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Persistence using image file execution option and magnifier.exe
    * Id: 4
    * Method: Image File Execution Options debugger and accessibility application
    * Syntax: `winpwnage.py --use persist --id 4 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a	
* Persistence using userinit key
    * Id: 5
    * Method: Registry key (UserInit) manipulation
    * Syntax: `winpwnage.py --use persist --id 5 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Persistence using HKCU run key
    * Id: 6
    * Method: Registry key (HKCU Run) manipulation
    * Syntax: `winpwnage.py --use persist --id 6 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Persistence using HKLM run key
    * Id: 7
    * Method: Registry key (HKLM Run) manipulation
    * Syntax: `winpwnage.py --use persist --id 7 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Persistence using wmic.exe (SYSTEM privileges)
    * Id: 8
    * Method: Malicious mof file using EventFilter EventConsumer and binding
    * Syntax: `winpwnage.py --use persist --id 8 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Persistence using startup files
    * Id: 9
    * Method: Malicious lnk file in startup directory
    * Syntax: `winpwnage.py --use persist --id 9 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Persistence using cortana windows app
    * Id: 10
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use persist --id 10--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 14393
	* Fixed in: n/a
* Persistence using people windows app
    * Id: 11
    * Method: Registry key (Class) manipulation
    * Syntax: `winpwnage.py --use persist --id 11--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 14393
	* Fixed in: n/a
* Persistence using bitsadmin.exe
    * Id: 12
    * Method: Malicious bitsadmin job
    * Syntax: `winpwnage.py --use persist --id 12--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Persistence using Windows Service (SYSTEM privileges)
    * Id: 13
    * Method: Malicious Windows Service
    * Syntax: `winpwnage.py --use persist --id 13--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a

## Elevation techniques:
* Elevate from administrator to NT AUTHORITY SYSTEM using handle inheritance
    * Id: 1
    * Method: Handle inheritance
    * Syntax: `winpwnage.py --use elevate --id 1--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using token impersonation
    * Id: 2
    * Method: Token impersonation
    * Syntax: `winpwnage.py --use elevate --id 2--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using named pipe impersonation
    * Id: 3
    * Method: Named pipe impersonation
    * Syntax: `winpwnage.py --use elevate --id 3--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using schtasks.exe (non interactive)
    * Id: 4
    * Method: Malicious scheduled task that gets deleted once used
    * Syntax: `winpwnage.py --use elevate --id 4--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using wmic.exe (non interactive)
    * Id: 5
    * Method: Malicious mof file using EventFilter EventConsumer and binding that gets deleted once used
    * Syntax: `winpwnage.py --use elevate --id 5--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using Windows Service (non interactive)
    * Id: 6
    * Method: Malicious Windows Service that gets deleted once used
    * Syntax: `winpwnage.py --use elevate --id 6--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using mofcomp.exe (non interactive)
    * Id: 7
    * Method: Malicious mof file using EventFilter EventConsumer and binding that gets deleted once used
    * Syntax: `winpwnage.py --use elevate --id 7--payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a

## AWL bypass techniques:
* Bypass Application Whitelisting using forfiles.exe
    * Id: 1
    * Method: Executes payload because it's a match for notepad.exe in the system directory
    * Syntax: `winpwnage.py --use execute --id 1--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using pcalua.exe
    * Id: 2
    * Method: Executes payload by running pcalua.exe with parameter -a
    * Syntax: `winpwnage.py --use execute --id 2--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using vsjitdebugger.exe
    * Id: 3
    * Method: Execute payload by calling it with vsjitdebugger.exe
    * Syntax: `winpwnage.py --use execute --id 3--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a	
* Bypass Application Whitelisting using bash.exe if Linux subsystem is installed
    * Id: 4
    * Method: Executes payload by running bash.exe with parameter -c
    * Syntax: `winpwnage.py --use execute --id 4--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 1020
	* Fixed in: n/a
* Bypass Application Whitelisting using diskshadow.exe
    * Id: 5
    * Method: Executes payload by running diskshadow.exe script
    * Syntax: `winpwnage.py --use execute --id 5--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a	
* Bypass Application Whitelisting using Advpack.dll
    * Id: 6
    * Method: Execute payload by calling the RegisterOCX function in Advpack.dll
    * Syntax: `winpwnage.py --use execute --id 6--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using dxcap.exe
    * Id: 7
    * Method: Executes payload by running dxcap.exe with parameter -c
    * Syntax: `winpwnage.py --use execute --id 7--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using ieadvpack.dll
    * Id: 8
    * Method: Execute payload by calling the RegisterOCX function in ieadvpack.dll
    * Syntax: `winpwnage.py --use execute --id 8--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using ieframe.dll
    * Id: 9
    * Method: Execute payload by calling the OpenURL function in ieframe.dll
    * Syntax: `winpwnage.py --use execute --id 9--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using pcwutl.dll
    * Id: 10
    * Method: Execute payload by calling the LaunchApplication function in pcwutl.dll
    * Syntax: `winpwnage.py --use execute --id 10--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using ftp.exe
    * Id: 11
    * Method:  Executes payload by running ftp.exe script
    * Syntax: `winpwnage.py --use execute --id 11--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a	
* Bypass Application Whitelisting using shdocvw.dll
    * Id: 12
    * Method: Execute payload by calling the OpenURL function in shdocvw.dll
    * Syntax: `winpwnage.py --use execute --id 12--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using url.dll
    * Id: 13
    * Method: Execute payload by calling the OpenURL function in url.dll
    * Syntax: `winpwnage.py --use execute --id 13--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using zipfldr.dll
    * Id: 14
    * Method: Execute payload by calling the RouteTheCall function in zipfldr.dll
    * Syntax: `winpwnage.py --use execute --id 3--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a	
* Bypass Application Whitelisting using sqltoolsps.exe
    * Id: 15
    * Method: Executes payload by running sqltoolsps.exe with parameters -noprofile -command Start-Process
    * Syntax: `winpwnage.py --use execute --id 15--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a
* Bypass Application Whitelisting using appvlp.exe
    * Id: 16
    * Method: Executes payload by running a batch file with appvlp.exe
    * Syntax: `winpwnage.py --use execute --id 15--payload c:\\windows\\system32\\cmd.exe`
	* Requires: n/a
	* Works from: 7600
	* Fixed in: n/a

## Installing the Dependencies:
```pip install -r requirements.txt```

## Build with py2exe:
In order for a successful build, install the py2exe (http://www.py2exe.org) module and use the provided build.py script to compile all the scripts in to a portable executable.  This only seems to work on Python 2, not on Python 3.

```python build.py winpwnage.py```

## Build with PyInstaller:
This build works on both Python 2 and Python 3 and puts the .exe file into the __dist__ directory.
```
pip install pyinstaller
pyinstaller --onefile winpwnage.py
```
On Windows 10, Access Denied errors can accure while compiling, rerun until success or elevate the prompt. 

## Read:
* https://wikileaks.org/ciav7p1/cms/page_2621770.html
* https://wikileaks.org/ciav7p1/cms/page_2621767.html
* https://wikileaks.org/ciav7p1/cms/page_2621760.html
* https://msdn.microsoft.com/en-us/library/windows/desktop/bb736357(v=vs.85).aspx
* https://winscripting.blog/2017/05/12/first-entry-welcome-and-uac-bypass/
* https://github.com/winscripting/UAC-bypass/
* https://www.greyhathacker.net/?p=796
* https://github.com/hfiref0x/UACME
* https://bytecode77.com/hacking/exploits/uac-bypass/performance-monitor-privilege-escalation
* https://bytecode77.com/hacking/exploits/uac-bypass/slui-file-handler-hijack-privilege-escalation
* https://media.defcon.org/DEF%20CON%2025/DEF%20CON%2025%20workshops/DEFCON-25-Workshop-Ruben-Boobeb-UAC-0day-All-Day.pdf
* https://lolbas-project.github.io
