import os

try:
  import psutil
except Exception as error:
  print "psutil is required, install it with (pip install psutil)"

def get_process_pid(process_name):
	""" Get process pid by name """
	for proc in psutil.process_iter():
		if proc.name() == process_name:
			return proc.pid
		
def search_dll(dllname,pid):
	""" Returns true if dll is found """
	loaded_dlls = []
	sorted_dlls = []
	open_process = psutil.Process(pid)
	
	for x in open_process.memory_maps():
		for dll in x:
			loaded_dlls.append(str(dll))
			
	for dll in loaded_dlls:
		if dll.endswith(".dll"):
			sorted_dlls.append(dll)

	for dll in sorted_dlls:
		if dllname in dll:
			return True

if search_dll("test.dll",get_process_pid("explorer.exe")) == True:
	print True
else:
	print False
