# Python script: 03 Remove blanks imported Excel file.py 
# AIM: How to read data from Excel file excluding null and blank cells and save cleansed data to a new folder as a .csv file.

import pandas as pd  
import os 
import numpy as np

project_folder = os.path.join('c:' + os.sep, 'Users','OGTSLCEF','OneDrive - NHS','Documents','Python Scripts','18 Seaborn_charts')
data_folder_path = os.path.join(project_folder,'data')

print(f'Data folder path:{project_folder}')
print(f'Data folder path shortened:{data_folder_path}')

# Display data folder files contents
data_folder_contents = os.listdir(data_folder_path)
print(f'Data folder path shortened:{data_folder_contents}')

# 1. Import Excel file into Python selecting specific sheet, rows and columns
data_raw = pd.read_excel(os.path.join('data','INE total and foreign population figures Spain.xlsx'),
                         sheet_name = 'INE_Total_population',
                         skiprows = 7,
                         usecols = 'A:B',
                         nrows = 212)
data_raw.head()
print(data_raw)

data_raw.columns

data_raw.columns = ['Year','Total_population']
data_raw.head()

# 2. Then remove null values from data_raw dataframe

### 2.1 Applying standard dropna() method to the entire dataset  based on values from "Total_populatiion" column 

#  The dropna() method removes any rows with null values in any column by default 
#  Arguments for dropna() method: 
#    - axis = 0 : drop rows (default)
#    - axis = 1 : drop columns
# (...)   
data_cleansed = data_raw.dropna(axis = 0, subset = ['Total_population'],inplace = False)
data_cleansed.head()

data_cleansed.tail()

### 2.2 The issue we find is that these are not NULL values they are empty cells
#### Replacing empty cells ith Nan values using np.nan method
# - The np. isnan() function returns a boolean array indicating which elements in the input array are NaN
imported_data_na = data_cleansed.replace(r'^\s*$', np.nan, regex = True)
print(imported_data_na)

imported_data_na.head()
imported_data_na.tail()
# Compared to what we had previously, we now have NaN values in
# # the "Total_population" column instead of empty cells.
# run this line below to check that  
data_cleansed.tail()

### 2.3 Empty cells are now replaces with NaN values. 
# # We can now use the drop.na() method   
imported_data_na.tail()

# - Now that we have NaN values in the "Total_population" column, we can use the dropna() method to remove rows with NaN values in that column
imported_data_clean = imported_data_na[['Year','Total_population']] 
imported_data_clean.head()
imported_data_clean.tail()

#- We apply the dropna() to the axis = 0 (rows)  
#- axis = 0 : drop null values based on ROWS (in Python 0 refers to ROWS)
# - Also we subset 'Year' and 'Total_population'columns only

# - This code below DOES NOT allows us to create the flag below.
imported_data_clean_test = imported_data_na.dropna(axis = 0, 
                                              subset = ['Year','Total_population'],
                                              inplace= False
                                              )
imported_data_clean_test.shape

### 2.4 Create a FLAG for rows containing Enero (January) data only
imported_data_clean = imported_data_na.dropna()
imported_data_clean.head()      
imported_data_clean.tail()

# The code below creates a flag with values "True" or "False" for rows
# containing "Enero" in the "Year" column
imported_data_clean['Enero_flag'] = imported_data_clean['Year'].str.contains('enero', case = False)
imported_data_clean.tail()

#- Then we can use those boolean "True" or "False" values to populate a new column. 
impported_data_clean_flag = imported_data_clean.copy()
impported_data_clean_flag.head()

#  This code below creates a new column called Jan_Flag that 
# # contains "Y" values for rows containing "Enero" in the "Year" column.
impported_data_clean_flag.loc[impported_data_clean_flag['Year'].str.contains('enero', case = False),'Jan_flag'] = 'Y'
impported_data_clean_flag.head()

### 2.5 Finally subset rows where newly created column "Jan_flag" takes value "Y" 
# - This approach below works fine. Using a Similar approach as DPLYR in R
final_population_data = impported_data_clean_flag[impported_data_clean_flag.Jan_flag == 'Y']
final_population_data.head()
final_population_data.tail()

final_population_data

# Get number of rows from "final_population_data" dataframe
df = final_population_data
num_rows = len(df.index)
print(f"Number of rows: {num_rows}")

# Another approach suggestged by copylot
# - Suggestioned by GitHub Copilot
# subset previos code using loc method to filter rows including Enero (January) Jan_flag = 'Y' only
final_population_data_copilot = imported_data_clean.loc[imported_data_clean['Year'].str.contains('enero', case = False)]
final_population_data_copilot.head()

df1 = final_population_data_copilot
num_rows_df1 = len(df1.index)
print(f'Number of ros in df1: {num_rows_df1}')

### 2.6 Keep only Year and Total_population from  final_population_data 
# # and output it as .csv file to a new folder called "data_cleansed"

# #### 2.6.1 First created new folder called "data_cleansed" in the same directory as this notebook
#### 2.6.1 First created new folder called "data_cleansed" in the same directory as this notebook
# Suggested by GitHub Copilot
if not os.path.exists('data_cleansed'):
    os.makedirs('data_cleansed')

# I use - We use makedirs() method to create a new directory
os.makedirs(os.path.join(project_folder,'data_cleansed'), exist_ok = True)

#### 2.6.2 Then subset columns from  dataset "final_population_data" keeping just "year" and "total population"   
final_population_data.head()  
final_population_data_output = final_population_data[['Year','Total_population']]
final_population_data_output.head()  

# 2.6.3 Finally save this "final_population_data_output" to "data_cleansed" new sub-folder in the project directory as a .csv file
final_population_data_output.head()
final_population_data_output.to_csv(os.path.join('data_cleansed','final_population_data_cleansed.csv'),index = False)

# - Final output excluding both empty cells and NaN values in the "Total_population" columns saved as .csv file in the "data_cleansed" new sub-folder in the project directory.
