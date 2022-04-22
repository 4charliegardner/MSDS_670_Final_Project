# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 11:03:34 2022

@author: Charlie Gardner
"""

import os
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
os.chdir('G:/Python/.jupyter/MSDS670/')

#%%

#Load geoshape files of North Carolina's census tracts 
##Need to first unzip the 'zipped_tl_2019_37_tract.7z' file from github
##Original fie retrieved from https://www.census.gov/cgi-bin/geo/shapefiles/index.php

NCsf ='tl_2019_37_tract.shp'
NCmap_df = gpd.read_file(NCsf)

#Pull out Forsyth County shapefile data
fmap_df = NCmap_df.loc[NCmap_df['COUNTYFP'] == '067']

#Check that data was properly formatted into a geodatframe
print(fmap_df.info())
fmap_df.plot()


#%%
#Load spreadsheet with student data
xlsx = pd.ExcelFile('CG_final_viz_project_data.xlsx' )

#Load ACS 2019 census tract data on Spanish speaking residents of Forsyth County
fc_span = pd.read_excel(xlsx, 'Spanish')

#Convert GEOID column from being integer to object
fc_span['GEOID'] = fc_span['GEOID'].astype(str)

#Check that data was properly formated into a dataframe
print(fc_span.info())
fc_span.head()

#%%

#Merge geodataframe with shapefiles with ACS 2019 census tract data on GEOID
merged = fmap_df.merge(fc_span, on='GEOID')

#Check data
print(merged.info())
merged.plot()


#%%

#Load Geocoded Addresses of Forsyth County High Schools
wsf_hs = pd.read_excel(xlsx, 'HS_Geocodes')

#Load Geocoded addesses of WSF Applicants
wsf_geocode = pd.read_excel(xlsx, 'App_Geocodes')

#Load Geocoded address of WSF Applicants who heard via Friends & Family
heard_ff = pd.read_excel(xlsx, 'Heard_FF')



#%%

#Plot 1

# Creating and Formatting Axes
fig, ax = plt.subplots(1, figsize=(30, 30))
ax.axis('off')

# add a title
ax.set_title('WSF Scholarship Applicants grouped by where they live \nand where they attend high school (in Forsyth County)', 
             fontdict={'fontsize': '50', 'fontweight' : '3'})

#Create map of Forysth County
merged.plot(color = 'whitesmoke', linewidth=1, alpha= .5, ax=ax, edgecolor='black')

#Add heatplot with applicant addresses
sns.kdeplot( x=wsf_geocode['Longitude'], y=wsf_geocode['Latitude'], cmap = 'Blues', alpha = .6, shade=True, bw_adjust=.75)

#Add bubbleplots with where the applicants attend high school 
plt.scatter(y=wsf_hs.Latitude, x=wsf_hs.Longitude, s=wsf_hs.No_Students*75, c='khaki', label="High Schools")


# Loop through the data points to annotate labels
for i, label in enumerate (wsf_hs.Name):
    plt.annotate( label, (wsf_hs.Longitude[i]-.015, wsf_hs.Latitude[i]+.005), fontsize=12,  color='k', weight = 'bold')
    
for i, value in enumerate (wsf_hs.No_Students):
    plt.annotate(value, (wsf_hs.Longitude[i]-.0035, wsf_hs.Latitude[i]-.002), fontsize=20, color='midnightblue', weight = 'bold')



#%%

#Plot 2

# Creating and Formatting Axes
fig, ax = plt.subplots(1, figsize=(25, 25))
ax.axis('off')

# Add a title
ax.set_title('Applicants who heard about WSF Scholarships via guidance counselor\n(Grouped by high school and overlaying map of Latinx community)', fontdict={'fontsize': '40', 'fontweight' : '3'})

# Create colorbar as a legend and to the figure
cbar = plt.cm.ScalarMappable(cmap= 'Greys', norm=plt.Normalize(vmin= 0, vmax=100))
cbar = fig.colorbar(cbar, aspect=50, pad= 0, orientation="horizontal")
cbar.ax.tick_params(labelsize=20)
cbar.set_label(label = 'Percent of Spanish Speakers', size = 25)

#Create map with Census data on Latinx Population
variable = 'Percent_Pop_Spanish'
merged.plot(column=variable, cmap='Greys', linewidth=1, alpha= .50, ax=ax, edgecolor='black')

#Add highschools with a bubbleplots to count students who applied for WSF Scholarships
plt.scatter(y=wsf_hs.Latitude, x=wsf_hs.Longitude, s=wsf_hs.Heard_Via_Guidance*75, c='powderblue', label="High Schools")

# Loop through the data points to annotate labels
for i, label in enumerate (wsf_hs.Name):
    plt.annotate( label, (wsf_hs.Longitude[i]-.015, wsf_hs.Latitude[i]+.005), fontsize=12,  color='k', weight = 'bold')
    
for i, value in enumerate (wsf_hs.Heard_Via_Guidance):
    plt.annotate(value, (wsf_hs.Longitude[i]-.0035, wsf_hs.Latitude[i]-.002), fontsize=20, color='midnightblue', weight = 'bold')

#%%

#Plot 3

# Creating and Formatting Axes
fig, ax = plt.subplots(1, figsize=(25, 25))
ax.axis('off')

# Add a title
ax.set_title('Applicants who heard about WSF Scholarships via family & friends\n(Grouped by high school and overlaying map of Latinx community)', fontdict={'fontsize': '40', 'fontweight' : '3'})

# Create colorbar as a legend and to the figure
cbar = plt.cm.ScalarMappable(cmap= 'Greys', norm=plt.Normalize(vmin= 0, vmax=100))
cbar = fig.colorbar(cbar, aspect=50, pad= 0, orientation="horizontal")
cbar.ax.tick_params(labelsize=20)
cbar.set_label(label = 'Percent of Spanish speakers per neighborhood', size = 25)

#Create map with Census data on Latinx Population
variable = 'Percent_Pop_Spanish'
merged.plot(column=variable, cmap='Greys', linewidth=1, alpha= .50, ax=ax, edgecolor='black')

#Add heatplot with applicant addresses
sns.kdeplot( x=heard_ff['Longitude'], y=heard_ff['Latitude'], cmap = 'Blues', alpha = .4, shade=True, bw_adjust=.5)

#Add highschools with a bubbleplots to count students who applied for WSF Scholarships
plt.scatter(y=wsf_hs.Latitude, x=wsf_hs.Longitude, s=wsf_hs.Heard_Via_Family*75, c='lightsalmon', label="High Schools")

# Loop through the data points to annotate labels
for i, label in enumerate (wsf_hs.Name):
    plt.annotate( label, (wsf_hs.Longitude[i]-.015, wsf_hs.Latitude[i]+.005), fontsize=12,  color='k', weight = 'bold')
    
for i, value in enumerate (wsf_hs.Heard_Via_Family):
    plt.annotate(value, (wsf_hs.Longitude[i]-.0035, wsf_hs.Latitude[i]-.002), fontsize=20, color='midnightblue', weight = 'bold')
    
