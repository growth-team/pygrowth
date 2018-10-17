#!/usr/bin/env python

import os
import pygrowth.counthistory
import pygrowth.eventfile
import numpy as np
import unittest

TEST_DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "test_data")


class TestCountHistory(unittest.TestCase):

    def test_counthistory_time_bin_width_center(self):
        counthistory = pygrowth.common.counthistory.CountHistory()
        counthistory.time_bin_edge_list = np.array([0.0, 10.0, 20.0])
        assert np.allclose(counthistory.time_bin_width(), [10, 10])
        assert np.allclose(counthistory.time_bin_center(), [5, 15])

    def test_counthistory_count_rate(self):
        counthistory = pygrowth.common.counthistory.CountHistory()
        counthistory.time_bin_edge_list = np.array([0.0, 10.0, 20.0])
        counthistory.count_list = np.array([200, 205])
        assert np.allclose(counthistory.count_rate(), [200 / 10.0, 205 / 10.0])
        assert np.allclose(counthistory.count_rate_error(), [np.sqrt(200) / 10.0, np.sqrt(205) / 10.0])

        # Expect exceptions when bin numbers differ
        counthistory.time_bin_edge_list = np.array([0.0, 10.0])
        counthistory.count_list = np.array([200, 205])
        with self.assertRaises(RuntimeError):
            counthistory.count_rate()
        with self.assertRaises(RuntimeError):
            counthistory.count_rate_error()

    def test_counthistory_summary_json_and_str(self):
        counthistory = pygrowth.common.counthistory.CountHistory()
        counthistory.time_origin = 0
        counthistory.time_bin_edge_list = np.array([0.0, 10.0, 20.0, 30.0])
        counthistory.count_list = np.array([200, 205, 210])

        expected = {
            "time_origin": 0,
            "time_axis": "absolute",
            "nbins": 3,
            "max_count": 210,
            "mean_count": 205.0,
            "min_count": 200,
            "stddev_count": np.std(counthistory.count_list),
        }

        self.assertEqual(counthistory.summary_json(), expected)
        self.assertEqual(str(counthistory), str(expected))


class MockEventFile(pygrowth.common.eventfile.EventFile):

    def __init__(self):
        self.unix_time = []
        self.channel = []
        self.energy = []


class TestCountHistoryExtractor(unittest.TestCase):

    def setUp(self):
        file_path = os.path.join(TEST_DATA_DIR_PATH, "20180101_002728.fits.gz")
        self.eventfile = pygrowth.common.eventfile.open(file_path)
        self.extractor = pygrowth.common.counthistory.CountHistoryExtractor()

    def test_extract_invalid_option(self):
        TIME_BIN_SEC = 10
        with self.assertRaises(ValueError):
            self.extractor.extract(self.eventfile, TIME_BIN_SEC, {"abc": 123})

        with self.assertRaises(ValueError):
            self.extractor.extract(self.eventfile, TIME_BIN_SEC, {"energy_range_kev": 123})

        with self.assertRaises(ValueError):
            self.extractor.extract(self.eventfile, TIME_BIN_SEC, {"energy_range_kev": [123]})

        with self.assertRaises(ValueError):
            self.extractor.extract(self.eventfile, TIME_BIN_SEC, {"duration_before_origin_sec": -1})

        with self.assertRaises(ValueError):
            self.extractor.extract(self.eventfile, TIME_BIN_SEC, {"duration_after_origin_sec": -1})

        with self.assertRaises(ValueError):
            INVALID_TIME_BIN_WIDTH_SEC = -1
            self.extractor.extract(self.eventfile, INVALID_TIME_BIN_WIDTH_SEC)

        with self.assertRaises(ValueError):
            self.extractor.extract(self.eventfile, TIME_BIN_SEC, {"time_axis": "abc"})

    def test_extract_invalid_row_number(self):
        TIME_BIN_SEC = 10
        mock_eventfile = MockEventFile()
        mock_eventfile.unix_time = []
        with self.assertRaises(RuntimeError):
            self.extractor.extract(mock_eventfile, TIME_BIN_SEC)

        mock_eventfile.unix_time = [1]
        mock_eventfile.energy = [1, 2, 3]
        mock_eventfile.channel = [1, 2, 3]
        with self.assertRaises(RuntimeError):
            self.extractor.extract(mock_eventfile, TIME_BIN_SEC)

    def test_extract(self):
        TIME_BIN_SEC = 10

        # Case 1: Relative time axis
        options = {
            "time_axis": "relative",
            "time_origin": 1514734663.0,
            "channel": 0,
            "energy_range_kev": [500, 3000],
            "duration_before_origin_sec": 30.0,
            "duration_after_origin_sec": 120.0,
        }

        counthistory = self.extractor.extract(self.eventfile, TIME_BIN_SEC, options)

        # Expected result
        time_bin_center_list = [-25.0, -15.0, -5.0, 5.0, 15.0, 25.0, 35.0,
                                45.0, 55.0, 65.0, 75.0, 85.0, 95.0, 105.0, 115.0, 125.0, 135.0, ]
        time_bin_width_list = [10] * len(time_bin_center_list)
        count_rate_list = [144.1, 136.3, 142.9, 138.0, 148.8, 144.3, 142.9, 146.5,
                           138.2, 144.6, 141.6, 136.1, 146.3, 138.2, 144.0, 138.1, 142.8, ]
        count_rate_error_list = [3.7960505792204615, 3.6918829883949464, 3.78021163428716, 3.714835124201342, 3.857460304397182, 3.7986839826445156, 3.78021163428716, 3.8275318418009276,
                                 3.717526059088221, 3.8026306683663087, 3.7629775444453557, 3.689173349139343, 3.824918299781056, 3.717526059088221, 3.794733192202055, 3.716180835212409, 3.778888725538237, ]

        assert np.allclose(counthistory.time_bin_center(), time_bin_center_list)
        assert np.allclose(counthistory.time_bin_width(), time_bin_width_list)
        assert np.allclose(counthistory.count_rate(), count_rate_list)
        assert np.allclose(counthistory.count_rate_error(), count_rate_error_list)

        # Case 2: Absolute time axis
        options["time_axis"] = "absolute"

        counthistory = self.extractor.extract(self.eventfile, TIME_BIN_SEC, options)

        # Expected result
        time_bin_center_list = [1514734638.0, 1514734648.0, 1514734658.0, 1514734668.0, 1514734678.0, 1514734688.0, 1514734698.0, 1514734708.0,
                                1514734718.0, 1514734728.0, 1514734738.0, 1514734748.0, 1514734758.0, 1514734768.0, 1514734778.0, 1514734788.0, 1514734798.0, ]
        assert np.allclose(counthistory.time_bin_center(), time_bin_center_list)
