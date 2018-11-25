import os
import sys
import astropy.io.fits as fits
from astropy.time import Time, TimeDelta
import arrow

SEC_IN_MIN = 60.0


class EventFile(object):

    def __init__(self):
        self.meta_data = None
        self.nevents = 0
        self.file_path = None

        self.unix_time = None
        self.energy = None  # in MeV
        self.channel = None
        self.trigger_count = None


class EventFitsFile(EventFile):
    """Represents EventFile in the FITS format.
       Columns:
       - timeTag
       - unixTime
       - boardIndexAndChannel
       - triggerCount
       - phaMax
       - phaMaxTime
       - phaMin
       - phaFirst
       - phaLast
       - maxDerivative
       - baseline
       - waveform
       - preciseTime
       - energy
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
        self._event_header = self.hdu['EVENTS'].header
        start_unix_time = self.hdu['EVENTS'].data['unixTime'][0]
        stop_unix_time = self.hdu['EVENTS'].data['unixTime'][-1]
        event_hdu = self.hdu['EVENTS']
        self.meta_data = {
            "original_file_name": os.path.basename(file_path),
            "detector_id": self._event_header['DET_ID'],
            "obs_site": self._event_header['OBS_SITE'],
            "start": start_unix_time,
            "end": stop_unix_time,
            "exposure_sec": event_hdu.data['unixTime'][-1] - event_hdu.data['unixTime'][0],
            "start_datetime": str(arrow.get(start_unix_time)),
            "end_datetime": str(arrow.get(stop_unix_time)),
            "num_rows": self.nevents,
            "fits_header": {}
        }

        for key, value in self._event_header.items():
            self.meta_data["fits_header"][key] = value

        # Load data into lists
        self._load_into_lists()

    def _load_into_lists(self):
        self.unix_time = self.hdu["EVENTS"].data["unixTime"]
        self.energy = self.hdu["EVENTS"].data["energy"]
        self.channel = self.hdu["EVENTS"].data["boardIndexAndChannel"]
        self.trigger_count = self.hdu["EVENTS"].data["triggerCount"]

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
