import glob
import os

def pull_location_file(location):
    
    """
    This function matches an inputted city within CONUS to the associated climate file for that location. 
    The location is matched via a dictionary to the associated The file
    pulled corresponds to the parameter input which could either be average temperature or average precipitation.
    The file name is returned.
    
    Inputs:
    location (string): structured "City, ST" in which the state is the two letter state abbreviation.
    
    Returns:
    used_filepath (string): filepath corresponding to the location of the city climate file.
    
    """
    
    ## Load the dictionary with cities and their corresponding Cooperative Observer Identification Numbers.
    #    This dictionary can be expanded to all cities located in the climate directory.
    
    city_dictionary = {'Raleigh, NC': '317074', 'Albany, NY': '300047',
                      'Seattle, WA': '457478', 'Dallas, TX': '412243',
                      'Salt Lake City, UT': '427578', 'Bismark, ND': '320818',
                      'Kansas City, MO': '234379', 'Flagstaff, AZ': '023009',
                      'Indianapolis, IN': '124260', 'Tallahassee, FL': '088756'}
    
    # Pull the city's ID
    desired_ID = city_dictionary[location]
    
    # Find the filepath of the individual station file
    filepath = glob.glob(os.getcwd() + '/CONUS_city_climate_stats/USC00'+ desired_ID +'.FLs.52j.tavg') 
    
    # Originally interpreted as a list, and must me pulled as a string.
    used_filepath = filepath[0]
    
    return used_filepath

## Testing functionaliy
def test_pull_location_file():
    # Prompt error if true filename does not match function generated filename
    assert pull_location_file('Kansas City, MO') == os.getcwd() + '/CONUS_city_climate_stats/USC00234379.FLs.52j.tavg'
    assert pull_location_file('Tallahassee, FL') == os.getcwd() + '/CONUS_city_climate_stats/USC00088756.FLs.52j.tavg'
    return

test_pull_location_file()

## Passes all tests.


# In[13]:


import glob
import os
import pandas as pd

def parse_climate_data(used_filename):
    
    """
    Processes a city climate data file that includes and format into a Pandas dataframe.
    Values of -9999 are interpreted as missing values. Each datapoint is scaled accordingly.
    
    Parameters:
        used_filename (String) - The filename of the city climate file to be parsed.
    Returns:
        (df) - A DataFrame containing all of the parsed and adjusted data.
    """
    
    ## Specify column names to hold the station average temperatures for each month for a range of years
    headings = ['Station Climate ID', 'Year', 'January', 'February', 'March', 'April',
                                 'May', 'June', 'July', 'August', 'September',
                                 'October', 'November', 'December']
    
    ## We need to specify the witdths so the correct data can be pulled. Matches documentation
    widths = [11, 5, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    
    ## Generate a dataframe based upon file organization and widths provided. Encoded nan values are taken into account.
    df = pd.read_fwf(used_filename, names=headings, header=None, widths=widths, na_values=[-9999])
    
    ## These lines handle special characters which pertain to "flags" applied to the downloaded dataset. These flags can
    #     be ignored for the purposes of this project as many are informational and do not indicate insufficient data quality.
    #     "regex" specifies the letters that become replaced. This is the easiest way to maintain negative values.
    df[['January','February','March','April','May','June','July','August',
       'September','October','November','December']]= df[['January','February','March','April','May','June','July','August',
       'September','October','November','December']].replace(regex=['a','b','c','d','e','f','g','h','i','E','X',
                                                                   'D','I','L','M','O','S','W','A','M','Q'], value="")
    
    ## Further data adjustment. Measurements must be divided by 100 as the data is encoded as integers but represent
    #     measurements in degrees Celsius to the hundreths place
    df[['January','February','March','April','May','June','July','August',
       'September','October','November','December']]= df[['January','February','March','April','May','June','July','August',
       'September','October','November','December']].astype(float)/100

    return df

## Testing functionality
def test_parse_climate_data():
    
    used_filepath = pull_location_file('Raleigh, NC')
    df_tested = parse_climate_data(used_filepath)
    
    ## Matching expected values in the dataframe to the true generated values. Most efficient way to test if the dataframe
    #     was generated correctly
    assert len(df_tested) == 131 #Checks number of rows
    assert df_tested.size == 1834 #Checks size
    assert df_tested.loc[128, 'January'] == 8.30 #Matches dataframe value to expected value
    assert df_tested['April'].dtypes == 'float64' #Checks to make sure all special characters were filtered out for a month.
    
    return

test_parse_climate_data()

## Passes all tests.