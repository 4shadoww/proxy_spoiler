# Import python modules
import datetime
import time

# Import pywikibot
import pywikibot
from pywikibot.site import APISite

# Import core modules
from core import proxy_spoiler
import core.config

class Worker:
	counter = 0

	def run(self):
		try:
			oldtime = datetime.timedelta(hours=12, minutes=0, seconds=0)
			timenow = datetime.datetime.now()
			api = APISite("fi")
			site = pywikibot.Site()

			print("now checking...")

			for rev in api.recentchanges(start=timenow, end=timenow-oldtime, showAnon=True, showBot=False):
				if self.counter >= core.config.first_scan:
					break

				#print(rev)
				print("checking:", rev["user"])
				proxy_spoiler.spoil(rev["user"])

				self.counter += 1

		except KeyboardInterrupt:
			print("yuno terminated...")
