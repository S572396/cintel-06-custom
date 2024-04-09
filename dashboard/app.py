import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from shiny import App, reactive, render, ui
from pathlib import Path

# Read data
def dat():
    infile = Path(__file__).parent / "C:/Users/19564/Documents/cintel-06-custom/cintel-06-custom/dashboard/Electric_Vehicle_Population_Data_20240406 (2).csv"
    return pd.read_csv(infile)

# Preprocess data and train model
def model_and_df():
    df = dat()
    
    df['count_of_EV'] = df.groupby('Model Year')['Model Year'].transform('count')
    
    X = df[['Model Year']].values
    y = df['count_of_EV'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model, df

# Define reactive function for histogram data
@reactive.calc()
def ev_count_histogram(df, selected_year):
    filtered_df = df[df['Model Year'] <= selected_year]
    fig = px.histogram(filtered_df, x="Model Year", title="Electric Vehicle Count by Year")
    return fig

# Define reactive function for scatter plot data
@reactive.calc()
def ev_count_scatter(df, selected_year):
    filtered_df = df[df['Model Year'] <= selected_year]
    fig = px.scatter(filtered_df, x="Model Year", y="count_of_EV", title="Electric Vehicle Count Scatter Plot")
    return fig

# Define Shiny UI
def main():
    @reactive.calc()
    def get_selected_year():
        return ui.selected_year().get()

    with ui.page_auto():
        ui.sidebar()

        # Input slider for selecting the year range
        ui.input_slider("selected_year", "Select Year", 2012, 2030, 2025)

        with ui.card():
            render(ev_count_histogram(model_and_df()[1], get_selected_year))

        with ui.card():
            render(ev_count_scatter(model_and_df()[1], get_selected_year))

    # Set the default selected year
    ui.selected_year(2025)

if __name__ == "__main__":
    main()




