# 💻 WinPwnage

The meaning of this repo is to study the techniques.

Techniques are found online, on different blogs and repos here on GitHub. I do not take credit for any of the findings, thanks to all the researchers.

Rewrote them and ported it to Python 2.7. The code under _todo_ folders are not tested, do not expect it to work. 

## Techniques implemented:
* UAC bypass using fodhelper
* UAC bypass using computerdefaults
* UAC bypass using slui
* UAC bypass using silentcleanup
* UAC bypass using compmgmtlauncher
* UAC bypass using sdclt (isolatedcommand)
* UAC bypass using sdclt (App Paths)
* UAC bypass using perfmon
* UAC bypass using eventviewer
* UAC bypass using sysprep (dll payload supported)
* UAC bypass using migwiz (dll payload supported)
* UAC bypass using mcx2prov (dll payload supported)
* UAC bypass using cliconfg (dll payload supported)
* Persistence using userinit
* Persistence using image file execution option
* Persistence using hklm run
* Persistence using hkcu run
* Persistence using schtask (SYSTEM privileges)
* Persistence using explorer dll hijack
* Persistence using WMI (SYSTEM privileges)

## Preview:
![alt text](https://i.imgur.com/5j4pKue.jpg)
![alt text](https://i.imgur.com/4Csq6AQ.jpg)

## Installing the Dependencies:
```pip install -r requirements.txt```

## Build:
In order for a successful build, install the py2exe (http://www.py2exe.org) module and use the provided build.py script to compile all the scripts in to a portable executable. On Windows 10, Access Denied errors can accure while compiling, rerun until success or elevate the prompt. 

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
