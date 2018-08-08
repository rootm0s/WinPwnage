import ctypes

"""
Hides the console window
"""
try:
	ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
except Exception as error:
	pass

"""
Displays if we are elevated or not
"""	
if (ctypes.windll.shell32.IsUserAnAdmin() == True):
	ctypes.windll.user32.MessageBoxA(0,"High IL","",0x0|0x40)
else:
	ctypes.windll.user32.MessageBoxA(0,"Medium IL","",0x0|0x40)