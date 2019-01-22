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
		library = ''
		version = 0.0
		if line.startswith('from '):
			library = line.split('.')[1].split(' ')[0]
			if '#version' in line :
				print('line',line,line.split('=')[1])
				version = float(line.split('=')[1])
			r.append([library,version])
	f.close()
	return r

def get_library_version(lib):
	if '{}.py'.format(lib) not in os.listdir('Blocky'):
		return None
	line = ''
	f = open('Blocky/{}.p