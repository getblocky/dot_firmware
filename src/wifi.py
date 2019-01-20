#version=1.0
import sys

core = sys.modules['Blocky.Core']
wlan_sta  = core.network.WLAN(core.network.STA_IF)

async def connect(ap=None):
	if core.eeprom.get('EXT_SOCKET') == True :
		print('wifi.py ->  exit ')
		return
	print('[WIFI] -> Connecting')
	await core.indicator.show('wifi-connecting')
	wlan_sta.active(True)
	if ap == None :
		while not wlan_sta.isconnected() :
			await core.wait(100)

	else :
		while not wlan_sta.isconnected():
			l = []
			core.wifi_list = wlan_sta.scan()
			for x in core.wifi_list:
				l.append(x[0].decode('utf-8'))
			print(l , sep = '\r\n')
			for preference in [p for p in core.config.get('known_networks') if p['ssid'] in l]:
				print('[',core.Timer.runtime(),'] Connecting to network {0}...'.format(preference['ssid']))
				print(preference)
				wlan_sta.connect(preference['ssid'],preference['password'])
				for check in range(50):
					if wlan_sta.isconnected():
						break
					print('.',end='')
					await core.wait(250)
				if wlan_sta.isconnected():
					print('Connected to ' ,  preference)
					break
			if wlan_sta.isconnected():
				core.flag.wifi = True
				print('Syncing NTP Time -> ', end = '')
				count   = 0
				for _ in range(5):
					try :
						await core.Timer.sync_ntp()
						print('OK')
						break
					except Exception as err:
						print('[NTP] -> {}'.format(err))
						await core.wait(10000)
				break
			await core.wait(10000)
			print('[WIFI] -> Reconneting')
