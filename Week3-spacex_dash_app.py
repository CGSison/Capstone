# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Task 0 Launch Site Drop-down option
ls=spacex_df['Launch Site'].unique()
ls=pd.DataFrame(ls,columns=["Launch Site"])
options_1=[]
for i in range(len(ls)):
          options_1.append({'label':ls.iloc[i]['Launch Site'],'value':ls.iloc[i]['Launch Site']})
options_2=[{'label': 'All', 'value': 'All'}]
options_2.extend(options_1)



# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=options_2,
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        class_count= [1]*len(filtered_df)
        filtered_df['class_count']=class_count
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, values='class_count', 
        names='class', 
        title='Share of Successful and Failed Launches of Launch Site {}'.format(entered_site))
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
              )
def get_scatter_chart(entered_site,slider_range):
    
    if entered_site == 'All':
        low, high = slider_range
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x="Payload Mass (kg)", 
        y="class",
        color="Booster Version Category",
        title="Payload Mass (kg) vs Class for All Launch Site")
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        low, high = slider_range
        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df[mask], x="Payload Mass (kg)", 
        y="class", 
        color="Booster Version Category",
        title="Payload Mass (kg) vs Class for Launch Site {}".format(entered_site))
        return fig






# Run the app
if __name__ == '__main__':
    app.run_server()
