from landsat_request import *
import argparse

import pandas as pd


def getparser():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    requiredargs = parser.add_argument_group("Required Arguments")
    optionalargs = parser.add_argument_group("Optional Arguments")
    requiredargs.add_argument("-path", "--path", type=int, required=True, help="Specify the Image Path")
    requiredargs.add_argument("-row", "--row", type=int, required=True, help="Specify the Image Row")
    requiredargs.add_argument("-date", "--date", type=str, required=True, help="Specify Date of Image")
    optionalargs.add_argument("-rt", "--rt", action='store_true',required=False, help="Include Real Time Images (Preprocessed)")

    return parser



def main():

	parser = getparser()
	args = parser.parse_args()

	path = args.path
	row = args.row
	date = args.date
	realtime = args.rt

	scene_request = landsat_request(path, row, date=date, realtime=realtime)


	available = scene_request.find_scene(download=True)

	if available:
		scene_request.download_scene()
	else:
		print("No Scene Available")




main()
