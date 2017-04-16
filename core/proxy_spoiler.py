import core.config
import urllib.request
import socket

socket.setdefaulttimeout(core.config.timeout)

def isproxy(targetIP, port, protocol="http"):
	proxy_support = urllib.request.ProxyHandler({protocol:targetIP+":"+port})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)
	html = urllib.request.urlopen("http://www.google.com").read()

	return True

def spoil(targetIP):
	for port in core.config.commonports:
		try:
			if isproxy(targetIP, port, protocol="http"):
				print("found from port", port)
				return True
		except socket.timeout:
			print("timeout:", port)
		except urllib.error.URLError:
			print("connection refused on port", port)

	return False
