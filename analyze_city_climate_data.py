import pandas as pd
import plotly.graph_objects as go
from load_city_climate_files import pull_location_file, parse_climate_data

def analyze_city_climate_data(location, timescale, start_year, end_year):
    
    """
    This function plots the average temperature for a particular city within CONUS over the course of a start year
    and an end year specified by the user. The average temperatures correspond either to the annual average (average across
    an entire year) or the average temperature for one month for that year which is also specified by the user. The
    time series plot generated is interactive for the user. This function MUST be ran by the user due to the nature of the
    plotting software used for the dropdown widgets.
    
    Inputs:
    location (string): structured "City, ST" in which the state is the two letter state abbreviation.
    
    timescale (string): Either "Annual" or one of the months of the year.
    
    start_year (integer): the year that will mark the start of the time series
    
    end_year (integer): the year that will mark the end of the time series
    
    Returns:
    Time series plotly plot of the average temperature across a certain timescale for a location.
    
    """
    
    ## Must have try and except block here to account for how this function reacts to inputs from a dropdown Jupyter
    #     widget. An error is generated upon first generating the dropdown menu. The table automatically updates based
    #     a change in the inputs, and if an input is not filled, an error will be generated. This is not something that
    #     can be solved by another method as there is no "direct" source.
    try:
        
        ## Start by pulling the dataframe for the location
        used_file_path = pull_location_file(location)

        df_city_data = parse_climate_data(used_file_path)
        
        
        if timescale == 'Annual':
            
            ## Find average of all monthly averages to generate a new column
            df_city_data['Average'] = df_city_data[['January','February','March','April','May','June','July','August',
           'September','October','November','December']].mean(axis=1)
            
            ## Any rows or columns with missing data should not be calculated in with the averages (inaccurate average)
            #     or illustrated in the plot
            df_city_data = df_city_data.dropna()
            
            ## Averages to be plotted
            plotted_data = df_city_data['Average']
            
            ## Slice dataframe to reflect average for the climateology of the location (Recent 30 year average)
            df_average = df_city_data.loc[(df_city_data['Year'] >= 1981) & (df_city_data['Year'] <= 2010)]
            
            ## Climateology Average to be used
            plotted_average = df_average['Average'].mean(axis=0)

        ## Only use monthly averages
        else:
            
            ## Any rows or columns with missing data should not be illustrated in the plot
            df_city_data = df_city_data.dropna(subset=[timescale])
            
            ##Averages to be plotted
            plotted_data = df_city_data[timescale]

            ## Slice dataframe to reflect average for the climateology of the location (Recent 30 year average)
            df_average = df_city_data.loc[(df_city_data['Year'] >= 1981) & (df_city_data['Year'] <= 2010)]
        
            ## 30-year average for that month being plotted
            plotted_average = df_average[timescale].mean(axis=0)
        
        ## Use plottly commands in order to create an interactive figure that can be easily updated
        fig = go.Figure()

        ## Plot the observational averages
        fig.add_trace(go.Scatter(x=df_city_data['Year'],
                y=plotted_data, mode='lines+markers',
                                name = 'Average Temperature'))

        ## Plot the climateology average
        fig.add_hline(y=plotted_average, line_color="red",
                      annotation_text = '1981-2010 Mean: ' + str(round((plotted_average),1)) + '°C',
                     annotation_position='top left')
        
        ## Add figure title, axis labels, and adjusted user time range
        fig.update_layout(xaxis=dict(
            tickmode="array",
            range = [start_year, end_year]),
            xaxis_title="Year",
            yaxis_title="Temperature °C",
            showlegend=False,
            title = location + ' ' + timescale + ' Average Temperature', 
            title_x=0.5,
            font=dict(size=14))
        
        ## Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray',mirror=True,ticks='outside',showline=True)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray',mirror=True,ticks='outside',showline=True)

        fig.show()
    
    ## Except block for when dropdown initially fails before fields are filled out
    except Exception:
        pass
    
## Test that the averages calculated closely match the actual averages (referenced NCDC website)
def testing_averages():
    
    ## Define Initial Conditions
    location = ['Dallas, TX', 'Raleigh, NC', 'Albany, NY']
    timescale = ['January', 'June', 'November']
    start_year = 1890
    end_year = 2021
    
    ## Loop through each city and month to see if averages are within .3 deg C of actual averages found
    for test in range(len(location)):
        ## Create Dataframe
        used_file_path = pull_location_file(location[test])
        df_city_data = parse_climate_data(used_file_path)
        
        ## Create Average Column for Annual Analysis
        df_city_data['Average'] = df_city_data[['January','February','March','April','May','June','July','August',
           'September','October','November','December']].mean(axis=1)
        
        ## drop nans for monthly and annual data
        df_city_data = df_city_data.dropna(subset=[timescale[test]])
        df_city_data_annual = df_city_data.dropna()
            
        ## Slice dataframe to reflect average for the climateology of the location (Recent 30 year average)
        df_average = df_city_data.loc[(df_city_data['Year'] >= 1981) & (df_city_data['Year'] <= 2010)]
        df_average_annual = df_city_data_annual.loc[(df_city_data_annual['Year'] >= 1981) & (df_city_data_annual['Year'] <= 2010)]
        
        ## 30-year average for that month/year being plotted
        plotted_average = df_average[timescale[test]].mean(axis=0)
        plotted_average_annual = df_average_annual['Average'].mean(axis=0)
        
        ## Actual Averages for the three cities that are each tested during loop below with respective months
        actual_average = [6.70, 24.20, 5.11]
        ## Actual Annual Averages for the three cities
        actual_average_annual = [17.92, 15.83, 9.56]
        
        assert abs(plotted_average - actual_average[test]) <= .3
        assert abs(plotted_average_annual - actual_average_annual[test]) <= .3
    
    
    return
    
testing_averages()

## Function passes all tests

## Commment on testing: Testing for the accuracy related to the values being pulled for this function and all functions called
#     is cumulative towards the understanding of the reliability of this function. The plotting software should be trusted to
#     be working accurately, it is the numeric outputs that should be tested.