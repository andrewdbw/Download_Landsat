import os, shutil
import pandas as pd
import requests
import argparse
import datetime


class landsat_request:
	
	def __init__(self, path, row, cloud=100, date=None, realtime=False):
		self.path = path
		self.row = row
		self.realtime = realtime

		if cloud:
			self.cloud = cloud
		else:
			self.cloud = 100
		
		if date:
			self.date = str(datetime.datetime.strptime(date, '%Y-%m-%d')).split(' ')[0]
		else:
			self.date = False

	def getDownloadlist(self):
		if self.download_list:
			return self.download_list
		else:
			print("No Scene Selected")

	def getPath(self):
		return self.path

	def getRow(self):
		return self.row

	def getCloud(self):
		return self.cloud

	def getDate(self):
		return self.date

	def getScene_df(self):
		return self.scene_df
			
		
	def find_scene(self, download=False):

		if download:
			print('\nDownloading Landsat Images with following parameters:')
			print("\nPATH: {}\nROW: {}\nDATE: {}".format(self.path, self.row, self.date))

		else:
			print('\nSearching Landsat Images with following parameters:')
			print("\nPATH: {}\nROW: {}\nCLOUDCOVER <=: {}%".format(self.path, self.row, self.cloud))
		
		if self.realtime:
			print("REAL TIME DATA: TRUE")
	

		# READ LANDSAT DATA
		s3_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip') # Reads Entire File to Memory
		
		#s3_scenes = pd.read_csv(os.path.join(r'/Users/Andrew/Downloads/', 'scene_list'))
		# Download Locally for Faster Reading
		# Download Link: http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz

		# FILTER LANDSAT IMAGES
		download_list = []

		if self.date:
			scenes = s3_scenes[(s3_scenes.path == self.path) & (s3_scenes.row == self.row) &
			                   (s3_scenes.acquisitionDate.str.contains(self.date))]
		else:
			scenes = s3_scenes[(s3_scenes.path == self.path) & (s3_scenes.row == self.row) & (s3_scenes.cloudCover <= self.cloud)]

		if not self.realtime:
			scenes = scenes[(~scenes.productId.str.contains('_RT'))]


		print('\nFound {} images\n'.format(len(scenes)))
		
		if len(scenes):
			for i in range(len(scenes)):
				scene = scenes.sort_values('acquisitionDate', ascending=False).iloc[i]
				download_list.append(scene)
		else:
			return False
			
		
		del s3_scenes
		
		self.download_list = download_list
		self.scene_df = scenes

		return True
	
	def download_scene(self, directory=None):
		
		if directory:
			dl_directory = directory
		else:
			dl_directory = os.path.expanduser(r'~/Downloads')
		
		# Download every image in Download List ( Currently limited to one )


		for scene in self.download_list:
		
			# Create Image Directory
			entity_dir = os.path.join(dl_directory, scene.productId)
			if os.path.isdir(entity_dir):
				shutil.rmtree(entity_dir)
			os.mkdir(entity_dir)
			
			# Get HTML for AWS Image Locations
			response = requests.get(scene.download_url)
			print("Downloading Image:\t{}\nAcquisition Date:\t{}\nCloud Cover:\t\t{}%".format(scene.productId, scene.acquisitionDate, scene.cloudCover))
			
			
			if response.status_code == 200: # Connection Successful
			
				# Loop through and Parse HTML Lines
				for line in response.iter_lines():
					line = str(line)
					
					# Filter to Listed Items in HTML (These are the Links to each band/dataset download)
					if line.find('li') > 0:
						# Example of Line:
						# <li><a href="LC08_L1TP_149039_20170411_20170415_01_T1_B8_wrk.IMD">LC08_L1TP_149039_20170411_20170415_01_T1_B8_wrk.IMD</a> (11.3KB)</li>
						file = line.split(r'"', 2)

						
						
						# Download TIF and Text Files
						if file[1][-4:] == '.TIF' or file[1][-4:] == '.txt':
							print("\tDownloading: {}".format(file[1]))
							
							response = requests.get(scene.download_url.replace('index.html', file[1]), stream=True)
							
							with open(os.path.join(entity_dir, file[1]), 'wb') as output:
								shutil.copyfileobj(response.raw, output)
								
							del response
			
			else:
				print("Could Not Connect")

			print()
				
				
			
		
