import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
from shiny.express import ui, input  
from shinywidgets import render_plotly
from shiny import render, reactive

# File path
infile = r"C:\Users\19564\Documents\cintel-06-custom\cintel-06-custom\dashboard\Electric_Vehicle_Population_Data_20240406 (2).csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(infile)

# Calculate the total for each year and add a new column
df['Total_Count_Per_Year'] = df.groupby('Model Year')['Model Year'].transform('count')

# Reactive calculation for future EV counts
@reactive.calc()
def future_ev_counts():
    X = df[['Model Year']]
    y = df['Total_Count_Per_Year']
    
    # Fit linear regression model to existing data
    model = LinearRegression()
    model.fit(X, y)
    
    future_years = np.arange(2025, 2036).reshape(-1, 1)  # Years from 2025 to 2035
    projected_counts = model.predict(future_years)
    
    future_df = pd.DataFrame({
        'Model Year': future_years.flatten(),
        'Projected_Count': projected_counts
    })
    
    return future_df

# Define the Shiny UI Page Layout
ui.page_opts(
    title="Sandra's EV Count Data for Washington State", 
    fillable=True
)

# Define the Shiny UI sidebar
with ui.sidebar(open="open"):
    ui.h2("EV Vehicles by Year", class_="text-center", style="color:red")
    ui.input_slider("Select_Year", "Year", 2010, 2030, 5)
    
    # Use dropdown to select a single year
    ui.input_select("selected_future_year", "Select Future Year", 
                     choices=[str(year) for year in range(2025, 2036)])

# Data Grid
with ui.h2("Data Grid"):
    @render.data_frame
    def EV_data_grid():
        return render.DataGrid(df, height=110)

# Plotly Scatterplot
with ui.h2("EV Scatterplot for Year"):
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

# Projected EV Counts Line Chart using Linear Regression
with ui.h2("Predicted EV Counts Linear Regression"):
    @render_plotly
    def projected_ev_counts():
        future_df = future_ev_counts()
        
        selected_year = int(input.selected_future_year())  # Get the selected year from the dropdown
        
        # Calculate linear regression line
        X = future_df[['Model Year']]
        y = future_df['Projected_Count']
        
        model = LinearRegression()
        model.fit(X, y)
        
        x_range = np.arange(2025, 2036).reshape(-1, 1)
        y_range = model.predict(x_range)
        
        # Predict the EV count for the selected year
        predicted_count = model.predict([[selected_year]])
        
        line_chart = px.line(
            future_df,
            title="Predicted EV Counts",
            x='Model Year',
            y='Projected_Count'
        )
        
        # Add regression line to the line chart
        line_chart.add_trace(go.Scatter(
            x=x_range.flatten(),
            y=y_range,
            mode='lines',
            name='Linear Regression',
            line=dict(color='black', width=2)
        ))
        
        # Add predicted count as a marker on the line chart
        line_chart.add_trace(go.Scatter(
            x=[selected_year],
            y=[predicted_count],
            mode='markers',
            name='Predicted Count',
            marker=dict(color='red', size=10)
        ))
        
        # Add legend to the chart
        line_chart.update_layout(
            legend_title='Year',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return line_chart

# Display predicted EV count as a numeric value in a grid
with ui.h2("Predicted EV Count"):
    @render.data_frame
    def display_predicted_count():
        future_df = future_ev_counts()
        
        selected_year = int(input.selected_future_year())
        
        # Calculate linear regression line
        X = future_df[['Model Year']]
        y = future_df['Projected_Count']
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict the EV count for the selected year
        predicted_count = model.predict([[selected_year]])
        
        # Create DataFrame to display predicted count
        predicted_df = pd.DataFrame({
            'Model Year': [selected_year],
            'Predicted_Count': [int(predicted_count[0])]
        })
        
        return predicted_df

        
        

















