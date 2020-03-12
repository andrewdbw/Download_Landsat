Landsat Download Python Module (Command Line Tools)

SEARCH TOOL:

	python search_landsat.py -path path_number -row row_number [-cloud cloud_percentage] [-rt]

	-path <path_number>
		Input Landsat WRS Path Number *Required

	-row <row_number>
		Input Landsat WRS Row Number *Required

	-cloud <cloud_percentage>
		Input Cloud cover percentage to search for (i.e. 5 = 5% or less cloudcover)

	-rt
		Includes Real Time Data

DOWNLOAD TOOL:

	python download_landsat.py -path path_number -row row_number [-date acquisition_date] [-rt]

	-path <path_number>
		Input Landsat WRS Path Number *Required

	-row <row_number>
		Input Landsat WRS Row Number *Required

	-date <acquisition_date>
		Input Specified acquisition date (Found from Search Landsat Tool)
			* If not included will bulk download all landsat images with the defined path and row

	-rt
		Includes Real Time Data
