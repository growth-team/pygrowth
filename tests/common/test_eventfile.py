#!/usr/bin/env python

import os
import pygrowth.common.eventfile

TEST_DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "test_data")


def test_str():
    file_path = os.path.join(TEST_DATA_DIR_PATH, "20180101_002728.fits.gz")
    eventfile = pygrowth.common.eventfile.open(file_path)

    expected = """20180101_002728.fits.gz (9.00 MB)
OBS_SITE: Kanazawa Izumigaoka High School
DET_ID  : growth-fy2016a
PL1_VER : growth-fy2017 Ver1
DET_CH0 : bgo-sakurai-10
Number of Events: 432356
Start (UTC): 2017-12-31T15:27:28.000
Stop  (UTC): 2017-12-31T15:57:31.779
Start (JST): 2018-01-01T00:27:28.000
Stop  (JST): 2018-01-01T00:57:31.779
Duration (min): 30.063
All event rate (cps): 239.695"""

    assert str(eventfile).strip() == expected
