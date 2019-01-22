import sys 
core = sys.modules['Blocky.Core']

class MicroWebSrv :
	
	# ===( Constants )============================================================
	
	_indexPages = [
		"index.html",
		"index.htm",
	]
	_mimeTypes = {
		".txt"	 : "text/plain",
		".htm"	 : "text/html",
		".html"	: "text/html",
		".css"	 : "text/css",
		".csv"	 : "text/csv",
		".js"	: "application/javascript",
		".xml"	 : "application/xml",
		".xhtml" : "application/xhtml+xml",
		".json"	: "application/json",
		".zip"	 : "application/zip",
		".pdf"	 : "application/pdf",
		".jpg"	 : "image/jpeg",
		".jpeg"	: "image/jpeg",
		".png"	 : "image/png",
		".gif"	 : "image/gif",
		".svg"	 : "image/svg+xml",
		".ico"	 : "image/x-icon"
	}
	_html_escape_chars = {
		"&" : "&amp;",
		'"' : "&quot;",
		"'" : "&apos;",
		">" : "&gt;",
		"<" : "&lt;"
	}
	_pyhtmlPagesExt = '.pyhtml'
	
	# ===( Utils	)===============================================================
	
	def HTMLEscape(s) :
		return ''.join(MicroWebSrv._html_escape_chars.get(c,