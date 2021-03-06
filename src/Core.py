#version=2.2

# All public variable across the system to avoid duplicate import
import os , json
prescript  = "import sys\ncore=sys.modules['Blocky.Core']\n"
import Blocky.EEPROM
eeprom = Blocky.EEPROM.EEPROM('eeprom')
rtc = False
asyncio = None
asyn = None
flag = None
mqtt = None
BootMode = None
indicator = None
config = None
ota_file = None
deinit_list = []
alarm_list = []
user_namedtask = []
wdt_timer = None
wifi_list  = {}
ext_socket = None
user_code = None
version = [2.0,'Nidalee Build']
dict = {}
import time,machine,neopixel,binascii,ure,gc,hashlib,network,sys
import micropython,socket,struct,_thread,random
import urequests
import Blocky.Global as flag
import Blocky.asyn as asyn
import Blocky.Timer as Timer
from Blocky.Indicator import indicator
from Blocky.Pin import getPort

cfn_btn = machine.Pin(12 , machine.Pin.IN , machine.Pin.PULL_UP)
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()
wifi = None # Wifi class started in Main
TimerInfo = [time.ticks_ms() , time.ticks_ms() , None , None]
hardware = {"uart" : ['repl',None,None],"spi" : ['flash',None,None]}
async def cleanup():
	print('[CLEANER] -? START')
	global deinit_list , alarm_list
	for x in deinit_list:
		try :
			print('deinit' , x)
			x.deinit()
		except:
			pass
	deinit_list = []	#refresh the list
	alarm_list = [] #delete all alarm stuff
	for x in asyn.NamedTask.instances :
		if x.startswith('user'):
			await asyn.NamedTask.cancel(x)

	a=False
	while a == False :
		a = True
		for x in asyn.NamedTask.instances:
			if x.startswith('user'):
				a = False
				break
		if a == True :
			break
		await asyncio.sleep_ms(10)
	print('[CLEANER] -? DONE')

async def call_once(name,function):
	print('[CALLING] {} -> {}'.format(name,function))
	try :
		if name in asyn.NamedTask.instances:
			if asyn.NamedTask.is_running(name):
				await asyn.NamedTask.cancel ( name )
				while asyn.NamedTask.is_running (name):
					await asyncio.sleep_ms(10)
	except Exception as err:
		del asyn.NamedTask.instances[name]
	#mainthread.call_soon(asyn.NamedTask(name,function))

	if function != None :
		print('[CALLING] {} -> {}  DONE '.format(name,function))
		mainthread.call_soon( asyn.NamedTask(name,function) ())
		# Avoid pend throw for just stated-generator
		await asyncio.sleep_ms(0)
	else :
		print('[CANCEL] {}'.format(name))

def download(filename , path):
	response = None
	gc.collect()
	try :
		print('[Downloading]  File -> ' + str(filename), end = '')
		response = urequests.get('https://raw.githubusercontent.com/getblocky/dot_firmware/master/ota/{}'.format(filename))
		if response.status_code == 200 :
			f = open('temp.py','w')
			f.write(response.content)
			print('#',end = '')
			piece = 0
			while True :
				piece += 1
				response = None
				gc.collect()
				try :
					response =  urequests.get('https://raw.githubusercontent.com/getblocky/dot_firmware/master/ota/{}_${}.{}'.format(filename.split('.')[0] , piece , filename.split('.')[1]))
					if response.status_code == 200 :
						f.write(response.content)
						print('#' , end = '')
					else :
						raise Exception
				except Exception :
					print('Pieces = ' , piece)
					f.close()
					os.rename('temp.py' , path)
					break
		else :
			print('[Download] Failed . Library ' , filename , 'not found on server')
	except Exception as err:
		import sys
		sys.print_exception(err)
		print('Failed')

	del response
	gc.collect()

def get_list_library(file):
	f = open(file)
	cell = ''
	while True :
		t  = f.read(1)
		cell += t
		if cell[-2:] == '\n\n' or len(t)==0:
			break
	cell = cell.split('\n')
	r = []
	for line in cell :
		try :
			library = ''
			version = 0.0
			if line.startswith('from ') or line.startswith('import ') or line.startswith('#require '):
				library = line.split('.')[1].split(' ')[0]
				if '#version' in line :
					print('line',line,line.split('=')[1])
					version = float(line.split('=')[1])
				r.append([library,version])
		except :
			pass
	f.close()
	return r

def get_library_version(lib):
	if '{}.py'.format(lib) not in os.listdir('Blocky'):
		return None
	line = ''
	f = open('Blocky/{}.py'.format(lib))
	while True :
		temp = f.read(1)
		if len(temp) == 0 or temp == '\n' or temp == '\r':
			break
		line += temp
	# #version=1.0
	if not line.startswith('#version'):
		f.close()
		return 0.0
	f.close()
	return float(line.split('=')[1])

"""
	Patch function , do not use await core.asyncio.sleep_ms(time) with time > 5s , this will block OTA process
	since it need to wait for the _sleep_ms task to be done.

	core.asyncio.sleep_ms(time)  ->  core.wait(time)  #ms
"""
async def wait ( time ):
	for x in range( time//500):
		await asyncio.sleep_ms(500)
	await asyncio.sleep_ms(time % 500)

_failsafe = None
def _failsafeActive(state):
	if state == True :
		try :
			wdt_timer.init(mode=machine.Timer.PERIODIC,period=20000,callback = _failsafe)
		except :
			pass
	if state == False :
		try :
			wdt_timer.deinit()
		except :
			pass
