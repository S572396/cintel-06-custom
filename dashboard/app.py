import pandas as pd
from shiny.express import ui
import plotly.express as px
from shinywidgets import render_plotly
from shiny import render

infile = r"C:\Users\19564\Documents\cintel-06-custom\cintel-06-custom\dashboard\Electric_Vehicle_Population_Data_20240406 (2).csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(infile)

# Calculate the total for each year and add a new column
df['Total_Count_Per_Year'] = df.groupby('Model Year')['Model Year'].transform('count')

# Define the Shiny UI Page Layout
ui.page_opts(title="EV Count Live Data Example", fillable=True)

# Define the Shiny UI sidebar
with ui.sidebar(open="open"):
    ui.h2("EV Vehicles by Year", class_="text-center", style="color:red")
    ui.input_slider("Select_Year", "Year", 2010, 2030, 5)
    
    # Use checkbox_group to filter
    ui.input_checkbox_group(
        "selected_attribute",
        "Select Attribute",
        ["Model Year", "Make", "Model", "Electric_Vehicle_Type"],
        selected=["Model Year"],
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
    
# Plotly Scatterplot
with ui.h2("Plotly Scatterplot"):
    @render_plotly
    def plotly_scatterplot():
        scatter = px.scatter(
            df,
            title="EV Data",
            x=df["Model Year"],
            y=df['Total_Count_Per_Year'],
            color="Model Year"
        )
        return scatter

# Projected EV Counts Line Chart
with ui.h2("Projected EV Counts"):
    @render_plotly
    def projected_ev_counts():
        last_year_data = df.groupby('Model Year').last().reset_index()
        last_year_data['Growth_Rate'] = last_year_data['Total_Count_Per_Year'].pct_change().mean()
        max_year = df['Model Year'].max()
        future_years = list(range(max_year + 1, 2031))  # Future years from the max year in the data to 2030
        projected_counts = [last_year_data['Total_Count_Per_Year'].iloc[-1] * ((1 + last_year_data['Growth_Rate']) ** (year - max_year)) for year in future_years]
        
        projected_df = pd.DataFrame({
            'Model Year': future_years,
            'Projected_Count': projected_counts
        })
        
        line_chart = px.line(
            projected_df,
            title="Projected EV Counts",
            x='Model Year',
            y='Projected_Count'
        )
        
        return line_chart
