from pygrowth.eventfile import EventFile
from pygrowth.extractor import Extractor
from pygrowth.util import NumpyEncoder
import numpy as np
import arrow
import json

# meta_data example
# {
#   "energy_range_kev": [500, 1e4],
#   "channel": 0,
#   "detector_id": "growth-fy2016a",
#   "header_data": {
#     ... FITS header key/value/comment ...
#    }
# }


class CountHistory:

    def __init__(self, meta_data=None):
        self.time_origin = None
        self.time_bin_edge_list = None
        self.count_list = None
        self.effective_time_list = None
        self.gti_list = None
        self.meta_data = meta_data if meta_data else {}
        self.time_axis = "absolute"

    def summary_json(self):
        return {
            "time_origin": self.time_origin,
            "time_axis": self.time_axis,
            "nbins": len(self.count_list),
            "max_count": np.max(self.count_list),
            "mean_count": np.mean(self.count_list),
            "min_count": np.min(self.count_list),
            "stddev_count": np.std(self.count_list),
        }

    def __str__(self):
        return str(self.summary_json())

    def time_bin_width(self):
        time_bin_width_list = self.time_bin_edge_list[1:] - self.time_bin_edge_list[0:-1]
        return time_bin_width_list

    def time_bin_center(self):
        return (self.time_bin_edge_list[1:] + self.time_bin_edge_list[0:-1]) / 2

    def count_rate(self):
        """ Returns count rate (count divided by the time bin width) in units of counts s^-1."""
        time_bin_width_list = self.time_bin_width()

        if len(time_bin_width_list) != len(self.count_list):
            raise RuntimeError("Lengths of time bin list and count list differ")

        return self.count_list / time_bin_width_list

    def count_rate_error(self, error_function=lambda x: np.sqrt(x)):
        time_bin_width_list = self.time_bin_width()

        if len(time_bin_width_list) != len(self.count_list):
            raise RuntimeError("Lengths of time bin list and count list differ")

        return error_function(self.count_list) / time_bin_width_list

    def energy_range(self):
        if "extraction_option" in self.meta_data and "energy_range_kev" in self.meta_data["extraction_option"]:
            return self.meta_data["extraction_option"]
        else:
            return None

    def plot(self, panel, options={}):
        color = "black" if "color" not in options else options["color"]
        linewidth = 1 if "linewidth" not in options else options["linewidth"]
        markersize = 3 if "markersize" not in options else options["markersize"]
        alpha = 1 if "alpha" not in options else options["alpha"]

        panel.errorbar(self.time_bin_center(), self.count_rate(),
                       xerr=self.time_bin_width() / 2, yerr=self.count_rate_error() / 2,
                       fmt="o", color=color,
                       linewidth=linewidth,
                       markersize=markersize, markerfacecolor=color, markeredgewidth=0.0, fillstyle="full",
                       alpha=alpha)

        # If "same" is true in options, styling will not be performed
        # like ROOT's "same" option.
        if "same" not in options or options["same"] is False:
            self._set_plot_style(panel, options)

    def _set_plot_style(self, panel, options={}):
        if "xlabel" in options:
            panel.set_xlabel(options["xlabel"])
        elif self.time_axis == "absolute":
            panel.set_xlabel("Time (s)")
        else:
            panel.set_xlabel("Time since {} (s)".format(arrow.get(self.time_origin)))

        if "ylabel" in options:
            panel.set_ylabel(options["ylabel"])
        else:
            panel.set_ylabel("Count rate (s$^{-1}$)")

        if "title" in options:
            panel.set_title(options["title"])

        if "ylim" in options:
            panel.set_ylim(options["ylim"])
        else:
            ylim = panel.get_ylim()
            panel.set_ylim(0, ylim[1])

        if "xlim" in options:
            panel.set_xlim(options["xlim"])

        if "grid" not in options or options["grid"] is False:
            panel.grid(True)


MAX_TIME_BINS = 1e5


class CountHistoryExtractor(Extractor):

    def extract(self, eventfile: EventFile, time_bin_sec, options={}) -> CountHistory:
        """
        Extract a count history from an EventFile by applying a set of filters.

        Accepted filtering options:
        - "time_axis": relative to the time origin or absolute unix time
        - "time_origin": time origin in unix time
        - "energy_range_kev": list of lower/upper energies in keV
        - "time_range": list of lower/upper unix time
        - "channel": integer of extracted channel
        - "duration_before_origin_sec": duration before time origin in sec
        - "duration_after_origin_sec": duration after time origin in sec

        :param eventfile: file to be processed
        :type eventfile: pygrowth.EventFile
        :param time_bin_sec: time bin width in sec
        :type time_bin_sec: float
        :param filter: dict containing filters (see docstring for available filters)
        :type filter: dict
        """
        ACCEPTED_OPTION_KEYS = [
            "time_axis",
            "time_origin",
            "energy_range_kev",
            "time_range",
            "channel",
            "duration_before_origin_sec",
            "duration_after_origin_sec",
        ]

        self.validate_option_keys(options, ACCEPTED_OPTION_KEYS)

        if len(eventfile.unix_time) <= 0:
            raise RuntimeError("Cannot extract count history from a blank event file")

        if not (len(eventfile.channel) == len(eventfile.energy) == len(eventfile.unix_time)):
            raise RuntimeError("The number of rows of the channel/energy/unix_time columns differ")

        # Construct filter
        condition = (eventfile.channel == eventfile.channel)

        if "channel" in options:
            condition &= eventfile.channel == options["channel"]

        if "energy_range_kev" in options:
            if not isinstance(options["energy_range_kev"], list) or len(options["energy_range_kev"]) != 2:
                raise ValueError("Energy range should be a list of 2 energy values in keV")

            condition &= ((options["energy_range_kev"][0] <= eventfile.energy)
                          & (eventfile.energy < options["energy_range_kev"][1]))

        filtered_unix_time = eventfile.unix_time[condition]

        # Create time bins
        _counthistory = CountHistory(meta_data={"extraction_option": options,
                                                "eventfile_meta_data": eventfile.meta_data})
        _counthistory.time_origin = options["time_origin"] if "time_origin" in options else filtered_unix_time[0]
        duration_before_origin_sec = options[
            "duration_before_origin_sec"] if "duration_before_origin_sec" in options else 0
        duration_after_origin_sec = options[
            "duration_after_origin_sec"] if "duration_after_origin_sec" in options else 0

        if duration_before_origin_sec < 0:
            raise ValueError("duration_before_origin_sec option must not be negative")

        if duration_after_origin_sec < 0:
            raise ValueError("duration_after_origin_sec option must not be negative")

        if duration_after_origin_sec == 0:
            duration_sec = filtered_unix_time[-1] - (_counthistory.time_origin - duration_before_origin_sec)
        else:
            duration_sec = (_counthistory.time_origin + duration_after_origin_sec) - \
                (_counthistory.time_origin - duration_before_origin_sec)

        nbins = duration_sec / time_bin_sec

        if not (0 < nbins < MAX_TIME_BINS):
            raise ValueError("Cannot create {} time bins".format(nbins))

        _counthistory.time_bin_edge_list = np.arange(
            _counthistory.time_origin - duration_before_origin_sec,
            _counthistory.time_origin + duration_sec,
            time_bin_sec)

        # Bin events
        _counthistory.count_list, _ = np.histogram(filtered_unix_time, bins=_counthistory.time_bin_edge_list)

        if "time_axis" in options:
            if options["time_axis"] == "relative":
                _counthistory.time_bin_edge_list -= _counthistory.time_origin
                _counthistory.time_axis = "relative"
            elif options["time_axis"] == "absolute":
                pass
            else:
                raise ValueError("time_axis option should be either of \"absolute\" or \"relative\"")

        return _counthistory


class CountHistoryWriter(object):
    pass


class CountHistoryWriterJSON(CountHistoryWriter):

    @classmethod
    def write(cls, dest, counthistory):
        if not hasattr(dest, "write"):
            dest = open(dest, "w")

        result = {
            "type": "counthistory",
            "content": {
                "time_origin": counthistory.time_origin,
                "time_bin_edge_list": list(counthistory.time_bin_edge_list),
                "count_list": list(counthistory.count_list),
                "effective_time_list": list(counthistory.effective_time_list) if counthistory.effective_time_list else [],
                "gti_list": list(counthistory.gti_list) if counthistory.gti_list else [],
                "meta_data": counthistory.meta_data,
                "time_axis": counthistory.time_axis,
            }
        }

        json.dump(result, dest, indent=2, separators=(",", ": "), cls=NumpyEncoder)


class CountHistoryReaderException(Exception):
    pass


class CountHistoryReader(object):
    pass


class CountHistoryReaderJSON(CountHistoryReader):

    @classmethod
    def load(cls, source):
        if not hasattr(source, "read"):
            source = open(source)

        data = json.load(source)

        if "type" not in data or data["type"] != "counthistory":
            raise CountHistoryReaderException("Not a count-history JSON")

        count_history = CountHistory(data["content"]["meta_data"])

        try:
            count_history.time_origin = data["content"]["time_origin"]
            count_history.time_bin_edge_list = np.array(data["content"]["time_bin_edge_list"])
            count_history.count_list = np.array(data["content"]["count_list"])
            count_history.effective_time_list = np.array(data["content"]["effective_time_list"])
            count_history.gti_list = np.array(data["content"]["gti_list"])
            count_history.time_axis = data["content"]["time_axis"]
        except Exception:
            raise CountHistoryReaderException("Invalid count-history JSON")

        return count_history
