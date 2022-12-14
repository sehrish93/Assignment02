# -*- coding: utf-8 -*-
"""climate data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UTmz2YdjxnUm5gvbHSqMgRuQKHQSZOOW

# Importing libraries
"""

import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import seaborn as sns

"""# Reading files"""

# definging function to read files
def reading_files():
    '''Reading the csv file which i have downloaded from world bank climate data
    skipping the 1st 4 rows which contain unecessary information'''
    data=pd.read_csv(r'C:\Users\Lenovo\Desktop\climate data analysis\API_19_DS2_en_csv_v2_4700503\data.csv',skiprows=4)
    '''returning two files, one the original data and one transposed data file'''
    return data, data.set_index('Country Name').T

# invoking reading files function
data, transposed_data = reading_files()

"""# Data preparation and exploration"""

# Dropping unnecessary columns
data = data.drop(['Unnamed: 66', 'Country Code', 'Indicator Code'], axis=1)

# Exploring data types and number of entities in data file
data.info()

# explore columns of dataframe
data.columns

# Descriptiv statistics of dataframe
data.describe()

# Exploring county names 
data['Country Name'].sort_values().unique()

# Explore factors of climate change
data['Indicator Name'].sort_values().unique()

# taking avaerage of 5 years from 1990 to 2020 and saving it in different columns
data['1991-1995'] = data[['1991', '1992',
                          '1993', '1994', '1995']].mean(axis=1)
data['1996-2000'] = data[['1996', '1997', 
                          '1998', '1999', '2000']].mean(axis=1)
data['2001-2005'] = data[['2001', '2002',
                          '2003', '2004', '2005']].mean(axis=1)
data['2006-2010'] = data[['2006', '2007', 
                          '2008', '2009', '2010']].mean(axis=1)
data['2011-2015'] = data[['2011', '2012', 
                          '2013', '2014', '2015']].mean(axis=1)
data['2016-2020'] = data[['2016', '2017', 
                          '2018', '2019', '2020']].mean(axis= 1)

#  Dropping all the columns from 1960 to 2021
data = data.drop(['1960', '1961', '1962', '1963', '1964',
                  '1965', '1966', '1967', '1968', '1969', 
                  '1970', '1971', '1972', '1973', '1974', 
                  '1975', '1976', '1977', '1978', '1979', 
                  '1980', '1981', '1982', '1983', '1984', 
                  '1985', '1986', '1987', '1988', '1989', 
                  '1990', '1991', '1992', '1993', '1994', 
                  '1995', '1996', '1997', '1998', '1999', 
                  '2000', '2001', '2002', '2003', '2004',
                  '2005', '2006', '2007', '2008', '2009', 
                  '2010', '2011', '2012', '2013', '2014', 
                  '2015', '2016', '2017', '2018', '2019', 
                  '2020', '2021'], axis = 1)


# drop rows in which all the numeric values are null
data = data.dropna(thresh=6)
# Displaying the new formed dataframe which contain 5 year mean columns
data

# checking null values
data.isnull().sum()

# filling missing values with mean value of all the years
data = data.T.fillna(data.mean(axis=1)).T
# checking for null valuea whether the data still have any missing value or not
data.isnull().sum()

# filterng country name and indicator name according to the interest 
options1 = ['Access to electricity (% of population)',
         'CO2 emissions (metric tons per capita)',
         'Electric power consumption (kWh per capita)',
         'Energy use (kg of oil equivalent per capita)',
         'Renewable energy consumption (% of total final energy consumption)']
options2 = ['India', 'Japan', 'Iran, Islamic Rep.', 'Saudi Arabia', 
          'United Arab Emirates', 'China','Turkiye', 'Bangladesh', 'Thailand', 'Qatar']
data = data[data['Indicator Name'].isin(options1)]
data = data[data['Country Name'].isin(options2)]
data

# Grouping the data according to country
data_grouped = data.groupby(['Country Name', 'Indicator Name'])
data_grouped.first()

"""# CO2 emissions"""

# filtering data frame according to co2 emissions
co2 = data[data['Indicator Name'].
           isin(['CO2 emissions (metric tons per capita)'])]

#  plotting bar chart showing the distribution of co2 emission in different countries
co2.set_index('Country Name').plot(kind='bar')
plt.title('CO2 emissions (metric tons per capita)')

"""# Electric power consumption"""

# filtering data acccording eletric power consumption
electric_power = data[data['Indicator Name'].
                      isin(['Electric power consumption (kWh per capita)'])]

# plotting bar chart showing the countries on x axis and values on y axis
electric_power.set_index('Country Name').plot(kind='bar')
plt.title('Electric power consumption (kWh per capita)')

"""# heatmap for qatar"""

# filtering countries for qatar and making a datafrane of only qatar
qatar = data[data['Country Name'].isin(['Qatar'])]
qatar = qatar.drop(['Country Name'],axis=1).T

# Reseting column name to short form to avoid space in heatmap
qatar.set_axis(['CO2',
       'Energy use',
       'Electric power',
       'Renewable energy',
       'Access to electricity'], axis='columns', inplace=True)

# Saving column names to a variable
cols = qatar.columns 
# Converting the columns to numeric
qatar=qatar[cols].apply(pd.to_numeric, errors='coerce') 

# Creating correlation heatmap of different factors for qatar
sns.heatmap(qatar.corr(), cmap="YlGnBu", 
            annot=True, linewidths=3, linecolor='black')
plt.title('Qatar')

"""# Energy use """

# filtering data for energy use factor for all countries
Energy_use = data[data['Indicator Name'].
                isin(['Energy use (kg of oil equivalent per capita)'])]

#plotting the distribution of energy use as line plot showing the 
# distribution of energy use in different countries
Energy_use.drop('Indicator Name',
                axis=1).set_index('Country Name').T.plot().legend(loc='upper right')
plt.title('Energy use (kg of oil equivalent per capita)')

"""# Renewable energy"""

# filtering values for renewable energy consumption
Renewable_energy = data[data['Indicator Name'].
                      isin(['Renewable energy consumption (% of total final energy consumption)'])]

# line plot showing the distribution of renewable energy consumption in different countires
Renewable_energy.drop('Indicator Name',
                      axis=1).set_index('Country Name').T.plot().legend(loc='upper right')
plt.title('Renewable energy consumption (% of total final energy consumption)')

"""# Heatmap for bangladesh"""

# Filtering countries values for bangladesh 
bangladesh = data[data['Country Name'].isin(['Bangladesh'])]
bangladesh = bangladesh.drop(['Country Name', 'Indicator Name'], axis=1).T

# renaming columns to short forms to avoid spcae problem in heatmap
bangladesh.set_axis(['CO2',
       'Energy use',
       'Electric power',
       'Renewable energy',
       'Access to electricity'], axis='columns', inplace=True)
bangladesh.reset_index(drop=True, inplace=True)

# Saving column names to a variable
cols = bangladesh.columns 
# Converting the columns to numeric
bangladesh=bangladesh[cols].apply(pd.to_numeric, errors='coerce') 

# creating correlation heatmap for bangladesh
sns.heatmap(bangladesh.corr(), cmap= 'coolwarm', annot=True)
plt.title('Bangladesh')

"""# Dataframe fro access to electricity"""

# creating dataframe for acces to electricity 
Access_to_electricity = data[data['Indicator Name'].
                             isin(['Access to electricity (% of population)'
                                   ])].set_index('Country Name').drop('Indicator Name',axis=1)
Access_to_electricity

