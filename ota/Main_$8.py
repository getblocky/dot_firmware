
			core.machine.reset()
		except Exception as err :
			core.sys.print_exception(err)
			core.time.sleep_ms(1000)
			core.mainthread.call_soon(core.blynk.log('[DOT_ERROR] {}'.format(str(err))))

core.blynk = None
core.mainthread.create_task(main())
wrapper()
#core._thread.start_new_thread(wrapper,())
