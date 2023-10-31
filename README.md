## Background
This repository was imported from a private Github enterprise class repository from my 2022 DSC 495 Scientific Computing in Python course and is meant to serve as a coding and data analysis sample to be referenced. Key progamming methods found included basic Python programming habits, big data handling, data visualization, an application of advanced Python skills to render self-updating drop-down menus (widgets), unit testing procedures, and general productive coding habits and documentation. The description of the project in standard README.md format is found below.

# Climate Visualization Project

Author: Logan McLaurin
This software and comes unwarrented at the discretion of NCSU.

## Introduction

Climate change has become a central focus of research in the geosciences. Attempts to forecast and interpret such changes can provide insight as to how climate change is impacting our planet as well as many other aspects of human civiliazation. Even so, it is arguably just as important to consider the climate change that has already occurred based on prior observations. The ability to analyze historical data regarding the Earth's temperature and its trends is fundamental towards addressing current and future implications of a changing climate.

## Methodology

Average air temperature data is analyzed on global and local scales for the years between 1890 and 2021. Datasets such as those provided by the *National Centers for Environmental Information* as well as the *NASA Goddard Institude for Space Studies* can provided monthly average air temperature data to be analyzed. Two visual representations of Earth's temperature will be utilized corresponding to a map of global average temperature anomalies as well as timescale plots for select cities showing average temperatures for each year.

### Global Temperature Anomalies Map

The dataset utilized to generate the map of global temperature anamolies is provided by the *NASA Goddard Institude for Space Studies*. The surface temperature analysis is based upon the *Global Historical Climate Network (NOAA/NCDC) version 4* which combines data from weather stations to estimate temperature changes over large regions. This dataset in particular includes both land and sea surface temperature anamolies based upon a 1200 km resolution with records stretching from 1890-2021. This is represented by a gridded scheme of 2° latitude by 2° longitude zones. The average temperature anomalies for each month during a year are recorded in degrees Celsius relative to the 1951-1980 (month) averages for these zones.
<br>
<br>
The file `gistemp1200_GHCNv4_ERSSTv5.nc` located in the local working directory of the project repository contains the temperature anomaly data. This file is loaded into the function `analyze_global_temp_anomalies.py`. No extra processing needs to be completed following loading the dataset by the netcdf4 module (data can be used as is). The function takes in a user specified year and month for which anomalies are to be visualized. The dataset is sliced based on these times and plotted using the *basemap* module through *matplotlib*. Shaded anamolies are created using *pcolormesh* which visually represent the 2 by 2 degree zones described with corresponding latitudes and longitudes.

### Temperature Timeseries Plots for Cities

The *North American Dataset* is utilized to generate average temperature timeseries for select cities and is provided by the *National Centers for Environmental Information*. This dataset includes files for thousands of Cooperative Observer stations which include ASOS stations and other local weather stations across the Continental United States. 
<br>
<br>
The file `load_city_climate_files.py` includes functions to pull and parse through specific city files. The software currently has the capacity to pull 10 different stations matching the city name (city, ST) to the station's individual Cooperative Observer Identification Number. This dictionary can be expanded in future updates to include more cities. Once the files are pulled by filename, the file information must be parsed and modified to remove special observational flags and correct the measurment scale (to reflect degrees Celsius to the hundreths place) so that the station information can be passed to a dataframe via the *pandas* module.
<br>
<br>
The file `analyze_city_climate_data.py` incorporates the processes described above so that average temperature data for a certain time frame and timescale can be visualize on a timescale. The user specifies the particular location, timescale (the averages for a particular month or the annual averages), and a start year and end year for the time series. Annual averages are calculated by averaging all of the monthly averages for each year. The average temperature for the location's climateology are also calcualted based upon the 1981-2010 temperatures corresponding to the same user inputs. This provides a reference point for the time series data and provides a perspective for what the "normal" averages are for the location unique to the timeseries. The *plotly* module is imported to create this timeseries plot based upon the temperature averages and the corresponding years. *plotly* is favored over *matplotlib* in this instance so as to promote an interactive plotting experience for the user. Datatips are included for the scatter of temperature averages for the timeseries plot, and this plot can easily be modified within the figure relative to Jupyter Widgets (matplotlib does not work well with Jupyter widgets).

## Implementation

These visualizations can be paired with Jupyter widgets to enhance the user experience and optimize the functionality of this software. The Jupyter widgets used include dropdown menus which incorporate all of the main inputs described for the analysis of both visualizations above. The functions for the City Climate Timeseries and the Global Anomalies (respectively) included in `Interactive_Climate_Visualization.py` allow for the implementation of these widgets for each process. The widgets are coded to automatically update the map and timeseries upon the change of any of the dropdown values. This promotes easy access to this software so that mulitple different combinations of inputs can be tested quickly and efficiently without any headaches for the user.
<br>
The Jupyter Notebook `Climate_Visualization_Report.ipynb` can be used to plot the Global Temperature Anomalies Map and the Temperature Timeseries Plots for Cities. Both cells MUST be ran by the user for the dropdown menus to generate. These are not self containing cells with the exception of the map. Please feel free to experiment with the software in this jupyter notebook further. Two examples of the generated producted for both the global analyses and the city plots are included below:

## Results and Testing

After reviewing both visualizations, there does appear to be evidence for a warming climate across most of the observed globe and the cities. As far as the global temperature anomalies are concerned, as time advances closer to the present, a greater amount of area exhibits positive average temperature anomalies for each month. Most cities also appear to have a positive trend when observing the times series for most months. This project is a representation of how data visualization can support a broader understanding of a field of research particularly with regards to climate change.

### Testing

The strategies taken with regards to testing the functions of the software relate to ensuring data was loaded correctly comparing numeric results from the plotting to the expected or cross-referenced results. Testing is extensively covered as a part of the Jupyter Notebooks listed and described above. It is, however, rather difficult to quantitatively test the functions of the plotting software directly as there is not a set, desired output that the plotting functions or the widgets can be tested against. However, extinsively testing the data provided to these plotting processes ensures that what is being plotted is reliable data. The visualizations themselves can be "tested" simply by observing whether or not the visualizations make sense without any extreme outliers. Averages and elements plotted in the graphs and anomaly map have been cross-examined with other values for specific locations and general regions provided by NASA and the NCDC. The purpose of these visualizations is to let the data and results speak to the user directly.
