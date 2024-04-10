import pandas as pd
from shiny.express import ui
import plotly.express as px
from shinywidgets import render_plotly
from shiny import render

infile = r"C:\Users\19564\Documents\cintel-06-custom\cintel-06-custom\dashboard\Electric_Vehicle_Population_Data_20240406 (2).csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(infile)

# Define the Shiny UI Page Layout
ui.page_opts(title="EV Count Live Data Example", fillable=True)

# Define the Shiny UI sidebar
with ui.sidebar(open="open"):
    ui.h2("EV Vehicles by Year", class_="text-center", style="color:red")
    ui.input_slider("Select_Year", "Year", 2010, 2030, 5)
    
    # Use checkbox_group to filter
    ui.input_checkbox_group(
        "select_attribute_list",
        "Select Attribute",
        ["Make Year", "Make", "Model", "Electric_Vehicle_Type"],
        selected=["Make Year"],
        inline=True
    )



    ui.hr()
    ui.h6("Links")
    ui.a("place link when done")

# Data Grid
with ui.h2("Data Grid"):
    @render.data_frame
    def EV_data_grid():
        return render.DataGrid(df, height=100)
