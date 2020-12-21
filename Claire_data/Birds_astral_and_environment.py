# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 15:34:48 2020

@author: Claire Brumat
"""
from numpy import *
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.pyplot import *
from datetime import *
import pytz
from astral import *


#%%

### CREATION OF LISTS FOR SUNRISE AND SUNSET ###


### setting location ###

location = Astral()['Copenhagen'] # I realised Copenhagen is closer than Stockholm
timezone = location.timezone
print(location)


### creating list of dates ###

def timelistfunc(start, end, interval):
    '''
    creates a list of time objects in betweeen start and end,
    time interval for each step is definded

    Parameters
    ----------
    start : date
        start date.
    end : date
        end date.
    interval : timedelta
        time interval between each new date.

    Returns
    -------
    lst : list
        list of time instances in between given time interval

    '''
    lst = []
    next = start
    while next <= end:
        lst.append(next)
        next = next + interval
    return lst


startdate = date(2015, 1, 25)
enddate = date(2016, 1, 17)
timeinterval = timedelta(days=1)

timelist = (timelistfunc(startdate, enddate, timeinterval)) #using previously defined function to create the list of dates


### creating list of sunrise and sunset ###

sunrise = []
sunset = []
sunshine = [] #amount of sunshine

for d in timelist:
    sun = location.sun(local=True, date = d)
    sr_h = sun['dawn'].hour + (sun['dawn'].minute/60) #time of day in hours
    ss_h = sun['dusk'].hour + (sun['dusk'].minute/60) #time of day in hours
    sunrise.append(sr_h) #adding sunrise time
    sunset.append(ss_h) #adding sunset time
    sunshine.append(ss_h - sr_h) #adding time difference between sunset and sunshine


#testing if it worked
print('date : ', timelist[-1])    
print('surise : ', sunrise[-1])
print('sunset : ', sunset[-1])
print('sunshine amount in hours: ', sunshine[-1])



### PLOTTING ###

plot(timelist, sunrise, label='sunrise')
plot(timelist, sunset, label = 'sunset')
plot(timelist, sunshine, label = 'amount of sunshine in hours')

title('sunrise vs sunset over the course of 1 year')
ylabel('time of day')

myFmt = DateFormatter("%m")

# Make ticks on occurrences of each month:
gca().xaxis.set_major_locator(MonthLocator())

# Get only the month to show in the x-axis:
gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))

# '%b' means month as locale’s abbreviated name
xticks(rotation=70)
gca().set_yticks(range(0, 24, 2))

grid()
legend()
    
show()

#%%

### DATA FROM https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer ###



### CREATING FUNCTIONS THAT ENABLE US TO CREATE LISTS FROM OUR TXT FILES ###

def create_time_list(filename):
    '''
    extracts a listof time data from a given file

    Parameters
    ----------
    filename : name of .txt file to extract data from
        
    Returns
    -------
    time_list : list
            list of time data
    '''
    time_list = []
    with open(filename, 'r') as f: #opens .txt file in read mode
        content = f.readlines()[1:] #extracts all the data except for the first line
        for line in content:
            line = line.rstrip() # takes the unnecessary caracters away (f.ex. '\n')
            time, data = line.split(';') # splits the data into time indicator and data, we indicate that the data is splity by ';'
            time_list.append(time) #we only extract the time component and att it to the list
    return time_list
        

def create_data_list(filename):
    '''
    creates list of environmental data 
    extracted from the given .txt file

    Parameters
    ----------
    filename : file to extract data from
        

    Returns
    -------
    data_list : list
        list of given environmental data.

    '''
    data_list = []
    with open(filename, 'r') as f:  #opens .txt file in read mode
        content = f.readlines()[1:] #extracts all the data except for the first line
        for line in content:
            line = line.rstrip() # takes the unnecessary caracters away (f.ex. '\n')
            time, data = line.split(';') # splits the data into time indicator and data, we indicate that the data is splity by ';'
            data_list.append(data)  #we only extract the data component and att it to the list
    return data_list



def save_to_file(col_list, new_filename):
    '''
    takes lists and converts them into a .txt file

    Parameters
    ----------
    col_list : list
        list of data that we previously created.
    new_filename : str
        name of the new file we want to create.

    Returns
    -------
    None.

    '''
    with open(new_filename, 'w') as f:
        for i in range(len(col_list[0])):
            row = ""
            for col in col_list:
                row += str(col[i]) + ";"  
            row = row[:-1] + "\n"
            f.write(row)
        
                
###CREATING THE LISTS USING THE PREVIOUSLY DEFINED FUNCTIONS ###
            

month_time_list = create_time_list('temperature_month.txt') # creates list with the time component = month
month_prec_data_list = create_data_list('precipitation_month.txt') # creates list with monthly precipitation
month_temp_data_list = create_data_list('temperature_month.txt') # creates list with monthly temperature

month_data = [month_time_list, month_prec_data_list, month_temp_data_list] #creates list of lists with monthly data
print("month data: ", month_data)

save_to_file(month_data, "month_prec_temp.txt")


day_time_list = create_time_list('temperature_day.txt') # creates list with the time component = day
day_prec_data_list = create_data_list('precipitation_day.txt') # creates list with daily precipitation
day_temp_data_list = create_data_list('temperature_day.txt') # creates list with daily temperature
day_snow_data_list = create_data_list('snowdebth_day.txt') # creates list with daily snowdebth


day_data = [day_time_list, day_prec_data_list, day_temp_data_list, day_snow_data_list, sunrise, sunset, sunshine] #creates list of lists with datily data
save_to_file(day_data, "day_prec_temp_snow_sun-r, sun-s, light.txt")


#%%

