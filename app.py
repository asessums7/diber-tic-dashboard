# Import Libraries
import pandas as pd
import gspread as gs
import flask
import dash
from dash import dcc, html
import dash_leaflet as dl
from dash.dependencies import Input, Output

# Load Google Sheet
gc = gs.service_account(filename='/Users/asessums/Desktop/diber-tic-survey/client_secret.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1SkSw85Hn0QMuDT5za4nNJmGMi2rujZqHPmq-zw28huM/edit#gid=1131511128')
ws = sh.worksheet('Responses')

# Create Dataframe
df = pd.DataFrame(ws.get_all_records())

# Rename Columns
df.rename(columns={
    'Timestamp': 'Timestamp',
    '1. What is your name?': 'Name',
    '2. What is your country of residence?': 'Country',
    '3. Is this your first time in Diber?': 'First Time',
    '4. Please list other cities you visited during your time in Albania.': 'Other Cities Visited',
    '1. On a scale of 1 to 5, how satisfied are you with the assistance provided by our staff?': 'Staff Rating',
    '2. What improvements would you suggest to make our tourism office more welcoming and informative?': 'Improvements',
    '5. What is your age group?': 'Age Group',
    '6. How many people are in your group?': 'Party Size',
    '7. What is the primary reason for your visit to Diber?': 'Primary Visit Reason',
    '8. Do you follow @visitdiber on any social media channels?': 'Follow Social Media',
    '9. How would you rate the accessibility and clarity of our maps and brochures?': 'Maps Rating',
    '10. Did you encounter any language barriers while seeking information or assistance at our office?': 'Language Barriers',
    '11. Will you visit any of the following Balkan countries during your travels? [Select all that apply]': 'Other Balkan Countries',
    '12. Would you be interested in participating in guided tours or workshops to enhance your experience in our destination?': 'Workshops',
    '4. Anything else you want to to tell us?!': 'Anything Else',
    'Experience in our Office': 'Experience'
}, inplace=True)

# Drop Experience Column
df = df.drop('Experience', axis='columns')

# Convert Timestamp to datetime format with the correct format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M:%S')

# Extract the month from the Timestamp and create a new column 'Month'
df['Month'] = df['Timestamp'].dt.to_period('M')

app = dash.Dash(__name__)
server = app.server

# ...

# ...

# Define layout
# ...

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🇦🇱", className="header-emoji"),
                html.H1(children="Dibër TIC Analytics", className="header-title"),
                html.P(
                    children="""A simple dashboard to visualize the behavior, demographics and trends of tourists visiting the Dibër Tourist Information Center (TIC) in Peshkopi, Albania.""",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.H2("Additional Comments", style={"text-align": "center"}),
                html.P(
                    "The bar charts provide valuable insights into the demographics and behaviors of tourists visiting the TIC in Dibër, Albania. The map below shows the location of the Dibër TIC in Peshkopi for easy reference.",
                    style={"text-align": "center", "margin": "10px 0"},
                ),
                html.P(
                    "Note that data used in this dashboard is based on survey responses collected from July 2023 onward.",
                    style={"text-align": "center"},
                ),
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                html.Div(
                    dcc.Graph(
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": df.groupby('Country')['Timestamp'].count().index,
                                    "y": df.groupby('Country')['Party Size'].sum(),
                                    "type": "bar",
                                    "marker": {
                                        "color": "red",  # Change the color of the bars to red
                                    },
                                },
                            ],
                            "layout": {
                                "title": "Tourists by Country of Residence", 
                                "font": {
                                    "family": "Lato, sans-serif",
                                    "size": 12,
                                    "color": "black"
                                },
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                dcc.Graph(
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "x": df['Age Group'].value_counts().sort_index().index,
                                "y": df['Age Group'].value_counts().sort_index(),
                                "type": "bar",
                                "marker": {
                                    "color": "red",  # Change the color of the bars to red
                                },
                            },
                        ],
                        "layout": {
                            "title": "Tourists' Age Groups"
                        },
                    },
                ),
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                dcc.Graph(
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "x": df.groupby(df['Month'].dt.strftime('%Y-%m'))['Timestamp'].count(),
                                "y": df.groupby('Month')['Timestamp'].count(),
                                "type": "bar",
                                "marker": {
                                    "color": "red",  # Change the color of the bars to red
                                },
                            },
                        ],
                        "layout": {
                            "title": "Tourists by Month"
                        },
                    },
                ),
            ],
            className="wrapper",
        ),
        
        html.Div(
            children=[
                dcc.Graph(
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "x": df['Party Size'].value_counts().index,
                                "y": df['Party Size'].value_counts(),
                                "type": "bar",
                                "marker": {
                                    "color": "red",  # Change the color of the bars to red
                                },
                            },
                        ],
                        "layout": {
                            "title": "Tourists' Group Sizes"
                        },
                    },
                ),
            ],
            className="wrapper",
        ),
        
        html.Div(
            children=[
                dcc.Graph(
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "labels": ['Yes', 'No'],
                                "values": df['Follow Social Media'].value_counts(),
                                "type": "pie",
                                "marker": {
                                    "colors": ['red', 'black'],  # Change the colors of the pie chart slices
                                },
                            },
                        ],
                        "layout": {
                            "title": "Tourists Following @visitdiber on Social Media"
                        },
                    },
                ),
                dcc.Graph(
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "labels": ['Yes', 'No'],
                                "values": df['First Time'].value_counts(),
                                "type": "pie",
                                "marker": {
                                    "colors": ['red', 'black'],  # Change the colors of the pie chart slices
                                },
                            },
                        ],
                        "layout": {
                            "title": "First Time in Diber"
                        },
                    },
                ),
            ],
            className="wrapper",
            style={"columnCount": 2}, 
        ),

        html.Div(
            children=[
                dcc.Graph(
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "x": df['Primary Visit Reason'].value_counts().index,
                                "y": df['Primary Visit Reason'].value_counts(),
                                "type": "bar",
                                "marker": {
                                    "color": "red",  # Change the color of the bars to red
                                },
                            },
                        ],
                        "layout": {
                            "title": "Tourists' Primary Visit Reasons"
                        },
                    },
                ),
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                # Add an interactive map using dash_leaflet.express
                dl.Map(
                    [
                        dl.TileLayer(),
                        dl.Marker(
                            position=[41.684940753589736, 20.43031527416778],
                            children=[
                                dl.Popup(
                                    "Diber Tourist Information Center",
                                    className="popup",
                                    closeOnClick=True,
                                    autoClose=False,
                                    closeOnEscapeKey=False,
                                )
                            ],
                        ),
                    ],
                    center=[41.684940753589736, 20.43031527416778],  # Latitude and Longitude of Diber TIC
                    zoom=15,
                    style={"height": "400px", "margin": "20px 0"},
                ),
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                html.H3("Personal Contact Information", className="footer-title"),
                html.Div(
                    [
                        html.Img(src="/avatar.jpeg", className="avatar"),
                        html.Div(
                            [
                                html.P("Alex Sessums", className="footer-content"),
                                html.P("Email: asessums7@gmail.com", className="footer-content"),
                                html.P("Phone: +355 69 400 2201", className="footer-content"),
                            ],
                            className="contact-info",
                        ),
                    ],
                    className="contact-container",
                ),
            ],
            className="footer",
        )
    ]
)

# ... 

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

### To Do List
# Add Previous Data from CSV file
# Add Google maps link?
