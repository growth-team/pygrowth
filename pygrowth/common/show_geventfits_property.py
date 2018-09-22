#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'GROWTH-Team'
__date__    = '2018 September 22'
__version__ = '0.01'
"""
2019-09-22 generated by Teru Enoto 
"""

import argparse 
import pygrowth.common.geventfits as gevt

if __name__=="__main__":

	parser = argparse.ArgumentParser(
		prog='show_geventfits_property.py',
		usage='show_geventfits_property.py gevent.fits',
		description='A script to check basic property of a GROWTH event fits file.',
		epilog='',
		add_help=True,
		)

	parser.add_argument(
		'geventfits',metavar='geventfits',type=str,        
		help='Input GROWTH event fits file.')
	args = parser.parse_args()	

	gf = gevt.GEventFits(args.geventfits)
	gf.show_property()