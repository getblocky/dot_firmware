await self._close('unknown message type')
			else :
				await core.wait(1)

			if not self._server_alive():
				await self._close('blynk server is offline')
				print('[Blynk] Connecting back to server')
				core.flag.blynk = False
				await core.indicator.show('blynk-authenticating')
				return
			else :
				core.flag.blynk = True
			await core.wait(1)
