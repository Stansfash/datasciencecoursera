# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())  # Cast to int
min_payload = int(spacex_df['Payload Mass (kg)'].min())  # Cast to int

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'Cape Canaveral', 'value': 'Cape Canaveral'},
            {'label': 'Kennedy Space Center', 'value': 'Kennedy Space Center'},
            {'label': 'Vandenberg', 'value': 'Vandenberg'},
            {'label': 'Guiana Space Centre', 'value': 'Guiana Space Centre'}
        ],
        value='ALL',  # Default value
        placeholder="Select a Launch Site here",
        searchable=True,
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,  # Minimum payload value
        max=max_payload,  # Maximum payload value
        step=1000,  # Step size for the slider
        value=[min_payload, max_payload],  # Default range
        marks={i: str(i) for i in range(0, max_payload + 1, 1000)},  # Labels for the slider
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_success_pie_chart(selected_site):
    # Filter the DataFrame based on the selected site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Count the number of successful and failed launches
    success_counts = filtered_df['class'].value_counts()
    
    # Create the pie chart
    fig = px.pie(
        success_counts,
        values=success_counts.values,
        names=success_counts.index,
        title=f'Success Counts for {selected_site} Launch Site'
    )
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_success_payload_scatter(selected_site, payload_range):
    # Filter the DataFrame based on the selected site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Further filter based on the payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    # Create the scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Payload vs Launch Success for {selected_site}',
        labels={'class': 'Launch Success (1=Success, 0=Failure)'}
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
