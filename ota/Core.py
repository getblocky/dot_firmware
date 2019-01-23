#version=2.1

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
TimerInfo = [time.ticks_ms()