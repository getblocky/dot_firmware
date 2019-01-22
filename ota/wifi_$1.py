
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
