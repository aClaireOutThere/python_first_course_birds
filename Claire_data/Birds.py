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


print('####### Final Project --- Birds #######')

def utc_to_local(utc_dt):
    ''' Converts UTC datetime objects to local time. '''
    local_tz = pytz.timezone('Europe/Stockholm')
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
                 

def preprocess(filename):
    ''' Preprocessing function to fix corrupted or wrong data from a txt file.
    Returns a list of datetimes in local time and a list of movements (int)
    for each datetime. '''
    with open(filename, 'r') as myfile:
            Lines = myfile.readlines()
    List = [line.split(" ") for line in Lines] # only one space sep because some lines contain several dates
    strings = [[i for i in L if i] for L in List] # Removes the blanks from Lines
    
    raw_dates = [] # List for string dates
    total_mov = [] # List for movements converted to (int)
    for string in strings:
        raw_dates.append(string[0] + ' ' + string[1])
        total_mov.append(int(string[2].strip()))
    
    utc_dates = [] # List for converted datetime objects - UTC format
    for date_time_str in raw_dates:
        utc_dates.append(datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f'))

    ### inserting datetimes between places with a separation > than 2.5 min 
    for i in range(1,len(utc_dates)):
        interval = utc_dates[i] - utc_dates[i-1]
        if interval.total_seconds() > 150:
            utc_dates.insert(i, utc_dates[i-1] + timedelta(seconds=120)) # adds a new datetime with 2 min sep.
            total_mov.insert(i,int((total_mov[i] + total_mov[i-1]) / 2)) # value inserted = avg between next and previous mov
    
    ### fixes when counter sets to 0 and when a value is wrong
    Acc = 0
    for i in range(1,len(total_mov)):
        if total_mov[i] == 0: # the counter sets to 0 in the text file
            Acc = total_mov[i-1] # changes the accumulated amount of mov. with the last lecture
        total_mov[i] += Acc 
        delta = total_mov[i] - total_mov[i-1]
        if delta < 0: # wrong data 
            total_mov[i] = total_mov[i-1]    
        if delta > 8: # mov. are limited to 4 per minute
            total_mov[i] = total_mov[i-1] + 8
            
    local_dates = [utc_to_local(utcdate) for utcdate in utc_dates] # UTC to local datetimes
    list_dates = local_dates[1:]
    list_mov = diff(total_mov)
    
    ### saving corrected data - UTC ###
    
    with open("corrected_data.txt", "w") as output:
        for i in range(len(utc_dates)):
            output.write(utc_dates[i].strftime('%Y-%m-%d %H:%M:%S.%f') + "   " + str(total_mov[i]) + "\n")

    return list_dates, list_mov
    

### MAIN ###      
file = "bird_jan25jan16.txt"

list_dates, list_mov = preprocess(file)

print(list_dates[0], list_mov[0])




#%%

listofymd=[] #list to save all the dates, removing hours,minutes,seconds
summingTheDay=0 #variable to sum the observations for the day
listOfObsPerDay=[] #list of total observations for the days, in matching order

for i in range(len(list_dates)):
    
    dateInString=list_dates[i].strftime("%Y-%m-%d") #Y/M/D in string
    if dateInString not in listofymd: #If the day has not been added yet
        listofymd.append(dateInString)
        if i!=0: listOfObsPerDay.append(summingTheDay) #if not first day, and if we are at a new day, append total sum
        summingTheDay=0 #reset total sum
    if i==(len(list_dates)-1): #if we have reached the end (the last obs.)
        listOfObsPerDay.append(summingTheDay) #append the sum for that day
        
    summingTheDay+=(list_mov[i]) #on every iteration this gets excecuted. sum added.
    
    
with open("birdsDaysData.txt","w") as outputday: #creating an external file. 
    for i in range(len(listofymd)):
        outputday.write(listofymd[i] + "   " + str(listofymd) + "\n")


print(len(listofymd))
print(len(listOfObsPerDay))
#plot(listofymd,listOfObsPerDay)
        



listOfHours=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
# list of the hours of the day
listOfObsPerHour=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# list of zeros of observation for each hour.
for i in range(len(list_dates)):
    
    hourInString=list_dates[i].strftime("%H") #only extract the hour in string
    for j in range(24): # both lists are of lenght 23
        
            if hourInString==listOfHours[j]: listOfObsPerHour[j]+=list_mov[i] #find which index the hour is in, add the observation
print(listOfObsPerHour)
print(len(listOfObsPerHour))
#plot(listOfHours,listOfObsPerHour)

with open("birdsHoursData.txt","w") as outputHour: #create new file
    for i in range(len(listOfHours)):
        outputHour.write(listOfHours[i] + "   " + str(listOfObsPerHour) + "\n")



print('days from, to: ', listofymd[0], listofymd[-1])
print('length: ', len(listofymd))
#%%

list_y_m = [] # list of dates as y-m ignoring days and hours
listObsPerMonth = [] #list of total number of movements detected in each month
totSumForMonth = 0 # total number of movements in month


for i in range(len(listofymd)):
    
    date_y_m = listofymd[i][:-3]#Y/M in string
    
    if date_y_m not in list_y_m: #If the date is not on the list
        
        list_y_m.append(date_y_m)
        
        if i!=0: #if it is not the first observations (thus the first month), then it must be a new month, append total sum and average
            listObsPerMonth.append(totSumForMonth) 
        totSumForMonth =0 #reset total sum
    
    if i==(len(listofymd)-1): #if we have reached the end (the last obs.)
        listObsPerMonth.append(totSumForMonth) #append the sum for the month 
    
    totSumForMonth +=(listOfObsPerDay[i])

f = open("birdsMonthData.txt","w")#creating an external file. 
for i in range(len(list_y_m)-1):
    f.write(list_y_m[i] + " " + str(listObsPerMonth[i]) + "\n")
    
#to Liam: so my code does work but your listofymd (list of date with days) and listOfObsPerDay contain only 42 days for some reason thats why theres only 2 lines in the BirdsMonthData.txt also you can start a new line by adding + "\n"

print('obs:',len(listOfObsPerDay),len(listofymd))









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
enddate = date(2016, 1, 16)
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

### PLOTTING SUN DATA ###


fig, ax1 = subplots()
ax2 = ax1.twinx()


ax1.plot(timelist, sunrise, label='sunrise')
ax1.plot(timelist, sunset, label = 'sunset')
ax1.plot(timelist, sunshine, label = 'amount of sunshine in hours')
ax1.grid()


title('sunrise vs sunset over the course of 1 year')
ax1.set_ylabel('time of day')


### PLOTTING OTHER DATA ###


ax2.plot(timelist, listOfObsPerDay, label='observations per day')

ax2.set_ylabel('number of observations')


myFmt = DateFormatter("%m")

# Make ticks on occurrences of each month:
ax1.xaxis.set_major_locator(MonthLocator())

# Get only the month to show in the x-axis:
ax1.xaxis.set_major_formatter(DateFormatter('%b %Y'))
# '%b' means month as locale’s abbreviated name

ax1.tick_params(axis='x', labelrotation=65)
ax1.set_yticks(range(0, 24, 2))

handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles += handles2
labels += labels2
print(type(handles))
fig.legend(handles, labels, loc='upper right')
  
show()
#%%


###PLOTTING NEW STUFF###

plot(month_time_list, month_prec_data_list)
plot(month_time_list, month_temp_data_list)

