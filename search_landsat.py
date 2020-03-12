from landsat_request import *
import argparse
import pandas as pd

# Set Panda Display Options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def getparser():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    requiredargs = parser.add_argument_group("Required Arguments")
    optionalargs = parser.add_argument_group("Optional Arguments")
    requiredargs.add_argument("-path", "--path", type=int, required=True, help="Specify the Image Path")
    requiredargs.add_argument("-row", "--row", type=int, required=True, help="Specify the Image Row")
    optionalargs.add_argument("-cloud", "--cloud", type=int, required=False, help="Specify Date of Image")
    optionalargs.add_argument("-rt", "--rt", action='store_true',required=False, help="Include Real Time Images (Preprocessed)")

    
    return parser



def main():

	# Parse Args
	parser = getparser()
	args = parser.parse_args()

	# Set Paramaters
	path = args.path
	row = args.row
	if args.cloud == None:
		cloud = 100
	else:
		cloud = args.cloud
	realtime = args.rt

	# Create Scene Request Object & Search for Scenes
	scene_request = landsat_request(path, row, cloud, realtime=realtime)

	available = scene_request.find_scene()

	# Display Results to User
	if available:
		scenes = scene_request.getScene_df()
		print(scenes[['productId', 'cloudCover', 'acquisitionDate']].sort_values('acquisitionDate', ascending=False).to_string(index=False, header=True, col_space=30, justify='right'))
	else:
		print("There are no Scenes with these parameters:")
		print("\tPath: {}\n\tRow: {}\n\tLess than or equal to {}% Cloudcover".format(path, row, cloud))



main()
