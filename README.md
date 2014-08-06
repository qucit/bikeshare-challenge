Qucit Bikeshare Prediction Challenge
====================================

Goals
-----
* Predict the number of bikes docked in Bordeaux bikeshare system 2 hours in advance.
The error to minimize is the Root Mean Square Error on the number of docked bikes averaged over all stations, RMSE(2) = avg(RMSE(n,2))

where

![equation](http://www.sciweavers.org/tex2img.php?eq=RMSE%28n%2Ch%29%20%3D%20%20%20%5Csqrt%7B%20%5Cfrac%7B1%7D%7BT%7D%20%20%5Csum_%7Bt%3D1%7D%5E%7BT%7D%20%20%5Cbig%28%20%5Cwidehat%7BB%7D_%7Bn%2Ch%2Ct%7D%20-%20B_%7Bn%2Ct%7D%20%20%5Cbig%29%5E2%20%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

is the RMS Error on the number of bikes for station n with a prediction horizon h

* And/or you can build a beautiful dataviz using this dataset

* But you can also propose your own original use
	* predictions on various time horizons
	* interesting patterns and insights
	* ...

The data
--------
* Static data for all 139 stations
	* Name
	* Total number of slots (the actual available number of slots may be less than this number due to malfunctionning/broken slots)
	* GPS coordinates
	* Whether the station is a 'VCub+' station, ie allowing longer renting (up to 20 hours free of charge) if the user validated in a tram or bus during the previous 75 minutes before renting a bike.
	* Whether the station has a credit card terminal allowing renting to casual users
* 3 months of bikeshare data for each station (1 hour timestep)
	* status of the station (0: out of order, 1: OK)
	* number of docked bikes (0 when a station is out of order does not correspond to the actual number)
	* number of available slots (0 when a station is out of order does not correspond to the actual number)
* 3 months of weather history (1 hour timestep)
	* precipitations (in millimeters per hour)
	* temperature (in °C)
	* ...

Beware that there are a few holes in the dataset (not all 1 hour periods have data for all stations : that's a real-life dataset !)

How to submit your solution ?
--------------------------
* Fork the project
* Create a branch whose name matches your github username
	* git branch your_github_username
	* git checkout your_github_username
* In this branch, create your own subdirectory 'bikeshare-challenge/submissions/your_github_username/' with your solution
* Do not modify anything outside your directory
* Your solution should include a file README.md with 
	* a short summary of the method used
	* if you choose the prediction challenge :
		* the splitting choice of the dataset into a training and testing set
		* the corresponding errors obtained on both part of the dataset
* Submit a pull request when you're done !

Languages
---------
Our favorite languages are python (pandas, scikit-learn, ...) for data analytics and javascript (leaflet, d3js) for dataviz, but you can use other ones if you need to (well, no fortran77 please ;) )

To use this dataset in a research paper
---------------------------------------
cite this url.