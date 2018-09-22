import os 
import sys
import astropy.io.fits as fits 
from astropy.time import Time, TimeDelta

class GEventFits():
	def __init__(self,eventfits):
		self.eventfits = eventfits
		if not os.path.exists(self.eventfits):
			sys.stderr.write("Error: File does not exist: %s\n" % self.eventfits)
			quit()
		try:
			self.hdu = fits.open(self.eventfits)
		except OSError as e:
			raise 
		sys.stdout.write("Fitsfile loaded: %s (%.2f MB)\n" % (
			self.eventfits,(os.path.getsize(self.eventfits) >> 20)))

		self.nevent = len(self.hdu['EVENTS'].data)

	def show_property(self):
		UTCtoJST_hour = 9.0
		tstart = Time(self.hdu['EVENTS'].data['unixTime'][0],format='unix',scale='utc')
		tstop  =  Time(self.hdu['EVENTS'].data['unixTime'][-1],format='unix',scale='utc')

		dump  = "%s (%.2f MB)\n" % (self.eventfits,(os.path.getsize(self.eventfits) >> 20))
		dump += "OBS_SITE: %s\n" % self.hdu['EVENTS'].header['OBS_SITE']
		dump += "DET_ID  : %s\n" % self.hdu['EVENTS'].header['DET_ID']
		dump += "PL1_VER : %s\n" % self.hdu['EVENTS'].header['PL1_VER']
		dump += "DET_CH0 : %s\n" % self.hdu['EVENTS'].header['DET_CH0']
		dump += "Number of Events: %d\n" % self.nevent		
		dump += "Start (UTC): %s\n" % tstart.utc.isot
		dump += "Stop  (UTC): %s\n" % tstop.utc.isot
		dump += "Start (JST): %s\n" % (tstart + TimeDelta(UTCtoJST_hour*60.0*60.0, format='sec')).utc.isot
		dump += "Stop  (JST): %s\n" % (tstop + TimeDelta(UTCtoJST_hour*60.0*60.0, format='sec')).utc.isot		
		dump += "Duration (min): %.3f\n" % ((tstop-tstart).sec/60.0)
		dump += "All event rate (cps): %.3f\n" % (self.nevent/(tstop-tstart).sec)
		sys.stdout.write(dump)