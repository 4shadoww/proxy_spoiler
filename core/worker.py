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
			data = proxy_spoiler.spoil(ip)
			if data[0]:
				self.db.insert({"ip": ip, "proxy": True, "port": data[1], "timestamp": str(datetime.datetime.now())})
			else:
				self.db.insert({"ip": ip, "proxy": False, "port": None, "timestamp": str(datetime.datetime.now())})
		else:
			print("skipping ip", ip, "because already exists in cache")

	def run(self):
		try:
			oldtime = datetime.datetime.utcnow() - datetime.timedelta(hours=12, minutes=0, seconds=0)
			api = APISite("fi")
			site = pywikibot.Site()
			first_scan = True
			print("now checking...")
			while True:
				timeutc = datetime.datetime.utcnow()
				timenow = datetime.datetime.now()

				counter = 0

				for rev in api.recentchanges(start=timeutc, end=oldtime, showAnon=True):
					if counter >= core.config.scan_limit:
						break
					print(rev["user"])
					self.checkIP(rev["user"])
					counter += 1

				oldtime = timeutc
				if datetime.datetime.utcnow() - oldtime <= datetime.timedelta(hours=0, minutes=core.config.sleeptime, seconds=0):
					sl = datetime.timedelta(hours=0, minutes=core.config.sleeptime, seconds=0) - (datetime.datetime.utcnow() - oldtime)
					print("sleeping for:", sl)
					time.sleep((sl.seconds))

		except KeyboardInterrupt:
			print("proxy spoiler terminated...")
