# cintel-06-custom
# Sandra's Electric Vehicle Count Data for Washington State

" This project will data from csv file from data.wa.gov and produce a data grid,
 a scatter plot of the data from, and a linear regression chart from
 the reactive function to predict future EV counts for years from 2025 to 2035.
 It will be interacative, a user can select a year from the 
drop down of years and pick a year and the EV or electric vehicle count will display to 
 them and can also be verified by the user hovering over the results in the linear 
regression chart "

## Imports
''' 
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
from shiny.express import ui, input  
from shinywidgets import render_plotly
from shiny import render, reactive
'''

## Data File converted to csv file:

infile = r"C:\Users\19564\Documents\cintel-06-custom\cintel-06-custom\dashboard\Electric_Vehicle_Population_Data_20240406 (2).csv"

Website: https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2/data_preview