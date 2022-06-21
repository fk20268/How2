#%matplotlib inline
import matplotlib
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data.csv')
df.dropna(inplace = True, thresh = 2)
df.replace(',','', regex = True, inplace=True)
display(df)

#an alternative to display() is print(tabulate(df, headers = 'keys', tablefmt = 'pretty'))

# here we are creating a new, smaller dataframe, and storing only the 2 columns we need in it 
year_and_gross_premiums_received = df[['Underwriting YoA','Gross Premiums Received']].copy()

# uncomment the line below if you would like to see what the new dataframe looks like
#display(gross_premiums_received)

#a variable that holds a list of the lengths of time after the underwriting years
length_of_time = []
# a variable that holds a list of the underwriting years
years = []


# a variable that holds the current year selected, so we are able to tell when it changes,
# here, we are setting it to be equal to the first value in the Underwriting YoA column
current_year_selected = year_and_gross_premiums_received['Underwriting YoA'][0]
years.append(current_year_selected)

# a variable to keep track of the number of iterations there has been for each year 
i = 0

# The below for loop iterates over each value in the Underwriting YoA column and, if the year has changed, it adds it 
# to the end of the list of years (using append(year))
for year in year_and_gross_premiums_received['Underwriting YoA']:
    # != means "not equal"
    if current_year_selected != year:
        # we set "i" back to 0 as the year has changed, so we want to start measuring from 0 again
        length_of_time.append(i)
        i=0
        current_year_selected = year
        years.append(year)
    #we increment i outside of the above for loop as we want to keep track of the length of time when the year doesn't change
    i += 1
# we append once more, as the values of the last year won't have been caught by the if condition 
# this is because the year won't have changed again before the table ends 
length_of_time.append(i)
        
print("this is the list of lengths of time in months: " + str(length_of_time))
print("this is the list of years: " + str(years) + "\n")
print("if the list of lengths of time is confusing, look at the table we printed in the exercise before, and note that there ")
print("are 58 (inc 0) datapoints corresponding to 2013, and 46 to 2014 and so on.\n ")      

# initiate a new dictionary
years_gross_premiums_data = {}

# we will use j to keep track of the current index for the datapoint we need
j=0

# we are going to go through the years and create a dictionary where the key is the year and the value is a list of 
# all the values corresponding to that year in the 'Gross Premiums Received' column
for year in years:
    i = years.index(year)
    #for each year that has elapsed after the underwriting year (for each underwriting year)
    ref_time_unit_list = []
    for time_unit in range(length_of_time[i]):
        ref_time_unit_list.append(int(year_and_gross_premiums_received['Gross Premiums Received'][j]))
        years_gross_premiums_data[year] = ref_time_unit_list
        #increment j
        j+=1

#first, find the size of the biggest array, we will do this by sorting A COPY of the array and taking the last (LARGEST) value
temp_array = length_of_time.copy()
temp_array.sort()
largest_array_size = temp_array[len(temp_array)-1]

# now we can pad with 0s 
for year in years_gross_premiums_data:
    for i in range(largest_array_size - len(years_gross_premiums_data[year])):
        years_gross_premiums_data[year].append(0)
    
    
# now we are able to convert the dictionary we built into a dataframe, and display this
df_years_gross_prem = pd.DataFrame(years_gross_premiums_data) 
#we will add a 'Total' row
df_years_gross_prem.loc['Total1'] = df_years_gross_prem.sum(numeric_only = True, axis = 0)
#This will add the rows
df_years_gross_prem.loc[:,'Total2'] = df_years_gross_prem.sum(numeric_only = True, axis = 1)

display(df_years_gross_prem)

#we will transpose it to get the orientation we want
df_years_gross_prem = df_years_gross_prem.transpose()

display(df_years_gross_prem)