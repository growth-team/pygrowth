__author__ = 'GROWTH-Team'
__date__ = '2018 September 22'
__version__ = '0.01'
"""
2019-09-22 generated by Teru Enoto
"""

import os
import sys
import astropy.io.fits as fits
from astropy.time import Time, TimeDelta

SEC_IN_MIN = 60.0

# TODO: Move this eventfile.py


class EventFile(object):

    def __init__(self):
        self.nevents = 0
        self.file_path = None


class EventFitsFile(EventFile):
    """Represents EventFile in the FITS format.
    :param file_path: path to a file to be opened
    """

    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            raise FileNotFoundError("{} not found".format(self.file_path))
        try:
            self.hdu = fits.open(self.file_path)
        except OSError as e:
            raise

        self.nevents = len(self.hdu['EVENTS'].data)

    def show_property(self):
        sys.stdout.write(str(self))

    def __str__(self):
        UTCtoJST_hour = 9.0
        tstart = Time(self.hdu['EVENTS'].data['unixTime'][0], format='unix', scale='utc')
        tstop = Time(self.hdu['EVENTS'].data['unixTime'][-1], format='unix', scale='utc')

        dump = "%s (%.2f MB)\n" % (os.path.basename(self.file_path), (os.path.getsize(self.file_path) >> 20))
        dump += "OBS_SITE: %s\n" % self.hdu['EVENTS'].header['OBS_SITE']
        dump += "DET_ID  : %s\n" % self.hdu['EVENTS'].header['DET_ID']
        dump += "PL1_VER : %s\n" % self.hdu['EVENTS'].header['PL1_VER']
        dump += "DET_CH0 : %s\n" % self.hdu['EVENTS'].header['DET_CH0']
        dump += "Number of Events: %d\n" % self.nevents
        dump += "Start (UTC): %s\n" % tstart.utc.isot
        dump += "Stop  (UTC): %s\n" % tstop.utc.isot
        dump += "Start (JST): %s\n" % (
            tstart + TimeDelta(UTCtoJST_hour * SEC_IN_MIN * SEC_IN_MIN, format='sec')).utc.isot
        dump += "Stop  (JST): %s\n" % (
            tstop + TimeDelta(UTCtoJST_hour * SEC_IN_MIN * SEC_IN_MIN, format='sec')).utc.isot
        dump += "Duration (min): %.3f\n" % ((tstop - tstart).sec / SEC_IN_MIN)
        dump += "All event rate (cps): %.3f\n" % (self.nevents / (tstop - tstart).sec)
        return dump


def open(file_path):
    if ".fits" in file_path:
        return EventFitsFile(file_path)
    else:
        raise NotImplementedError("EventFile class for this file type is not implemented")