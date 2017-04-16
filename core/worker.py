# Import python modules
import datetime
import time

# Import pywikibot
import pywikibot
from pywikibot.site import APISite

# Import lib
from tinydb import TinyDB, Query

# Import core modules
from core import proxy_spoiler
import core.config

class Worker:
	db = TinyDB('db/proxy_cache.json')
	user = Query()

	def checkIP(self, ip):
		matches = self.db.search(self.user.ip == ip)

		if len(matches) == 0:
			print("now checking ip:", ip)
			if proxy_spoiler.spoil(ip):
				self.db.insert({"ip": ip, "proxy": True})
			else:
				self.db.insert({"ip": ip, "proxy": False})
		else:
			print("skipping ip", ip, "because already exists in cache")

	def run(self):
		try:
			oldtime = datetime.datetime.now() - datetime.timedelta(hours=12, minutes=0, seconds=0)
			api = APISite("fi")
			site = pywikibot.Site()
			print("now checking...")
			while True:
				timenow = datetime.datetime.now()
				oldtime2 = timenow
				counter = 0

				for rev in api.recentchanges(start=timenow, end=oldtime, showAnon=True, showBot=False):
					if counter >= core.config.scan_limit:
						break
					self.checkIP(rev["user"])
					counter += 1
				oldtime = oldtime2

				if datetime.datetime.now() - oldtime <= datetime.timedelta(hours=0, minutes=core.config.sleeptime, seconds=0):
					sl = datetime.timedelta(hours=0, minutes=core.config.sleeptime, seconds=0) - (datetime.datetime.now() - oldtime)
					print("sleeping for:", sl)
					time.sleep((sl.seconds))
		except KeyboardInterrupt:
			print("yuno terminated...")
