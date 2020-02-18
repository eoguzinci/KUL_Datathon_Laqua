# do not forget to enable gmaps in jupyter notebook by executing the following command
# in ipython shell ``jupyter nbextension enable --py gmaps``

import gmaps
import numpy as np

def get_gmap_figure(LAT, LON, filename = 'apikey.txt'):

	# Reference: https://jupyter-gmaps.readthedocs.io/en/latest/tutorial.html#basic-concepts

	# read google maps API
	with open(filename) as f:
		my_api_key = f.readline()
		f.close

	# get the base map
	gmaps.configure(api_key=my_api_key) # Fill in with your API key

	# zoom the map around the center
	center_of_all_sensors = (np.mean(LAT),np.mean(LON))

	# set the figure properties
	figure_layout = {
		'width': '600px',
		'height': '600px',
		'border': '1px solid black',
		'padding': '1px',
		'margin': '0 auto 0 auto'
	}

	# plot the base map
	fobj = gmaps.figure(center=center_of_all_sensors, layout=figure_layout, zoom_level=13, map_type='TERRAIN')

	# Note:
	#'ROADMAP' is the default Google Maps style,
	#'SATELLITE' is a simple satellite view,
	#'HYBRID' is a satellite view with common features, such as roads and cities, overlaid,
	#'TERRAIN' is a map that emphasizes terrain features.

	# add point locations on top of the base map
	locations = list(zip(LAT,LON)) # provide the latitudes and longitudes
	sensor_location_layer = gmaps.symbol_layer(locations, fill_color='red', stroke_color='red', scale=2)
	fobj.add_layer(sensor_location_layer)
	
	return fobj
