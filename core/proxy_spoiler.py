import core.config
import urllib.request
import http.client
import socket

socket.setdefaulttimeout(core.config.timeout)

def isproxy(targetIP, port, protocol="http"):
	proxy_support = urllib.request.ProxyHandler({protocol:targetIP+":"+port})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)
	html = urllib.request.urlopen("http://www.google.com").read()
	if "google" in str(html):
		return True

def spoil(targetIP):
	for port in core.config.commonports:
		try:
			if isproxy(targetIP, port, protocol="http"):
				print("found from port", port)
				return True, port
			else:
				print("\"google\" not found from response using port", port)
		except socket.timeout:
			print("timeout:", port)
		except urllib.error.URLError:
			print("connection refused on port", port)
		except http.client.BadStatusLine:
			print("[http.client.BadStatusLine] proxy may have found from port", port)
			return None, port
		except ConnectionResetError:
			print("[ConnectionResetError] proxy may have found from port", port)
			return None, port
		except urllib.error.URLError:
			print("url error on port", port)

	return False, None
