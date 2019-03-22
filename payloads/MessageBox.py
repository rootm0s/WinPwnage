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
IL = "High IL" if ctypes.windll.shell32.IsUserAnAdmin() else "Medium IL"
ctypes.windll.user32.MessageBoxA(0,IL,"",0x0|0x40)
