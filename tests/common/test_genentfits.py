#!/usr/bin/env python

import os 
import pygrowth.common.geventfits as gevt

testfile = '%s/20180110_022850.fits' % os.getenv('PYGROWTH_REPOSITORY_PATH')
gf = gevt.GEventFits(testfile)
gf.show_property()