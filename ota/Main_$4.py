thread.call_soon(core.blynk.log('[DOT_ERROR] {}'.format(str(err))))

core.blynk = None
core.mainthread.create_task(main())
wrapper()
#core._thread.start_new_thread(wrapper,())
			
	
	
		
			
	