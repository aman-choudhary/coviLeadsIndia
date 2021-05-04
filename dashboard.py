import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import timeago
import datetime
from datetime import datetime
import pytz
import dash_table as dt
import tweepy

# Covid19India API
timeseries_country_url = "https://api.covid19india.org/csv/latest/case_time_series.csv"
statewise_url = "https://api.covid19india.org/csv/latest/state_wise_daily.csv"
vac="http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv"

#Add your credentials here
twitter_keys = {
        'consumer_key':        'XXXXXXXXXXXX',
        'consumer_secret':     'XXXXXXXXXXXX',
        'access_token_key':    'XXXXXXXXXXXX',
        'access_token_secret': 'XXXXXXXXXXXX'
    }

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

s1=['created_at','id_str','full_text','retweet_count','user.name','user.screen_name',
'user.followers_count','user.verified','user.favourites_count']
append_str = 'retweeted_status.'
s2=[append_str + sub for sub in s1]

# Get the data into the app

timeseries_country = pd.read_csv(timeseries_country_url)
statewise=pd.read_csv(statewise_url)
statecode = "statecodes.csv"
statecode=pd.read_csv(statecode)
loc = "statelocation.csv"
loc=pd.read_csv(loc) 
vac=pd.read_csv(vac)
vac=vac.dropna(axis=1)
vac30D = vac.iloc[-1]

#Extract useful info from the dataset
total_confirmedd=int(timeseries_country['Total Confirmed'].tail(1))
new_confirmedd=int(timeseries_country['Daily Confirmed'].tail(1))
total_recovery=int(timeseries_country['Total Recovered'].tail(1))
new_recovery=int(timeseries_country['Daily Recovered'].tail(1))
total_deceased=int(timeseries_country['Total Deceased'].tail(1))
new_deceased=int(timeseries_country['Daily Deceased'].tail(1))
total_active=total_confirmedd-total_recovery-total_deceased
new_active=new_confirmedd-new_recovery-new_deceased
 

# Instanciate the app
app = dash.Dash(__name__,title="CoviLeads", meta_tags = [{"name": "viewport", "content": "width=device-width,initial-scale=1.0"}])
server=app.server

# Build the layout
app.layout = html.Div(
	children = [
        
		# (Second row) Cards: Global cases - Global deaths - Global recovered - Global active
        html.Div(
			children = [
				# (Column 1): Global cases
                
				html.Div(
					children = [
                        
						# Title
						html.H6(
							children = "Confirmed Cases",
							style = {
								"textAlign": "center",
								"color": "#222035"
                                
							}
						),
						# Total value
						html.P(
							children = f"{total_confirmedd:,.0f}",
							style = {
								"textAlign": "center",
								"color": "orange",
								"fontSize": 30,
                                "font-weight": "bold"
							}
						),
						# New cases
						html.P(
							children = "new: " +
								f"{new_confirmedd:,.0f}" +
								" (" +
								f"{round(((new_confirmedd) / total_confirmedd) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "orange",
								"fontSize": 14,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
				# (Column 2): Global deaths
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Deceased",
							style = {
								"textAlign": "center",
								"color": "#222035"
							}
						),
						# Total value
						html.P(
							children = f"{total_deceased:,.0f}",
							style = {
								"textAlign": "center",
								"color": "#dd1e35",
								"fontSize": 30,
                                "font-weight": "bold"
							}
						),
						# New deaths
						html.P(
							children = "new: " +
								f"{new_deceased:,.0f}" +
								" (" +
								f"{round(((new_deceased) / total_deceased) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "#dd1e35",
								"fontSize": 14,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
				# (Column 3): Global recovered
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Recovered",
							style = {
								"textAlign": "center",
								"color": "#222035"
							}
						),
						# Total recovered
						html.P(
							children = f"{total_recovery:,.0f}",
							style = {
								"textAlign": "center",
								"color": "#01B075",
								"fontSize": 30,
                                "font-weight": "bold"
							}
						),
						# New recovered
						html.P(
							children = "new: " +
								f"{new_recovery:,.0f}" +
								" (" +
								f"{round(((new_recovery) / total_recovery) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "green",
								"fontSize": 14,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
				# (Column 4): Global active
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Active",
							style = {
								"textAlign": "center",
								"color": "#222035"
							}
						),
						# Total v
						html.P(
							children = f"{total_active:,.0f}",
							style = {
								"textAlign": "center",
								"color": "#e55467",
								"fontSize": 30,
                                "font-weight": "bold"
							}
						),
						# New active
						html.P(
							children = "new: " +
								f"{new_active:,.0f}" +
								" (" +
								f"{round(((new_active) / total_active) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "#e55467",
								"fontSize": 14,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
                
                html.Div(
					children = [
						# Title
						html.H6(
							children = "Vaccinations",
							style = {
								"textAlign": "center",
								"color": "#222035"
							}
						),
						# Total v
						html.P(
							children = f"{vac30D.iloc[-1]:,.0f}",
							style = {
								"textAlign": "center",
								"color": "blue",
								"fontSize": 30,
                                "font-weight": "bold"
							}
						),
						# New active
						html.P(
							children = "new: " +
								f"{(vac30D.iloc[-1]-vac30D.iloc[-2]):,.0f}" +
								" (" +
								f"{round(((vac30D.iloc[-1]-vac30D.iloc[-2]) / vac30D.iloc[-1]) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "blue",
								"fontSize": 14,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				)
			],
			className = "row flex-display"
		),
		# Second Row
        html.Div(
            
					children = [
                        html.P(
							children = "ENTER YOUR CITY AND RESOURCES REQUIRED. PRESS ENTER TO PROCEED.",
							className = "fix_label",
							style = {
								"color": "#222035",
                                "font-size":"14px",
                                "font-weight":"bold",
                                "font-family":"Open Sans"
							}
						),
                        html.P(),
                        dcc.Input(id='city',
                                  type='text',value='Delhi'
                                  , debounce=True,
                                  style=
                                  {
                                      'color':'black',
                                      'background-color':'white',
                                      'width':'100%'
                                      }
                        ),
                        html.P()
						,
                        dcc.Dropdown(id='essentials',
                        options=[
                        {'label': 'Remdesivir', 'value': 'remdesivir'},
                        {'label': 'Oxygen Cylinder', 'value': 'oxygen'},
                        {'label': 'Plasma', 'value': 'plasma'},
                        {'label': 'ICU', 'value': 'icu'},
                        {'label': 'Ventilator', 'value': 'ventilator'},
                        {'label': 'Favipiravir', 'value': 'favipiravir'},
                        {'label': 'Tocilizumab', 'value': 'tocilizumab'},
                        {'label': 'Beds', 'value': 'beds'}
                        ],
                        value="oxygen",
                        clearable=False,
                        style=
                                  {
                                      'color':'black',
                                      'background-color':'white',
                                      'width':'100%'
                                      }
                        )  ,
                        html.Br(),
                        dcc.Loading(
            id="loading-1",
            type="circle",
                        children=html.Div(id="table1"))
						
					],
                    className = "create_container eleven columns",
				)
        ,
        # (Third row): Value boxes - Donut chart - Line & Bars
        html.Div(
			children = [
				# (Column 1) Value boxes
				html.Div(
					children = [
						# (Row 1) Country selector
						html.P(
							children = "Select State ",
							className = "fix_label",
							style = {
								"color": "#222035",
                                "font-family":"Calibri"
							}
						),
						dcc.Dropdown(
							id = "state",
							multi = False,
							searchable = True,
							value = "TT",
							placeholder = "Select Country",
							options = [{"label": statecode['State Name'][i], "value": statecode['State Code'][i]} for i in (range(len(statecode)))],
							className = "dcc_compon"
						),
						# (Row 2) New cases title
						html.P(
							children = "Last Updated On " + " " + str(statewise['Date'].iloc[-1]),
							className = "fix_label",
							style = {
								"textAlign": "right",
								"color": "#222035",
                                "font-family":"Calibri",
                                "font-size":"15PX"
							}
						),
						# (Row 3) New confirmed
						dcc.Graph(
							id = "Confirmed",
							config = {
								"displayModeBar": False
							},
							className = "dcc_compo",
							style = {
								"margin-top": "20px"
							}
						),
						# (Row 4) New deaths
						dcc.Graph(
							id = "Deceased",
							config = {
								"displayModeBar": False
							},
							className = "dcc_compo",
							style = {
								"margin-top": "20px"
							}
						),
						# (Row 5) New recovered
						dcc.Graph(
							id = "Recovered",
							config = {
								"displayModeBar": False
							},
							className = "dcc_compo",
							style = {
								"margin-top": "20px"
							}
						),
						# (Row 6) New active
						dcc.Graph(
							id = "active",
							config = {
								"displayModeBar": False
							},
							className = "dcc_compo",
							style = {
								"margin-top": "20px"
							}
						)
					],
					className = "create_container three columns"
				),
				# (Column 2) Donut chart
				html.Div(
					children = [
						# Donut chart
						dcc.Graph(
							id = "pie_chart",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container four columns",
					style = {
						"maxWidth": "400px"
					}
				),
				# (Columns 3 & 4) Line and bars plot
				html.Div(
					children = [
						dcc.Graph(
							id = "line_chart",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container five columns"
				)
			],
			className = "row flex-display"
		)
        ,
        # Fifth row
        
        html.Div(
			children = [
                
				html.Div(
					children = [
						dcc.Graph(
							id = "map_chart",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "create_container1 eleven columns"
				)
			],
			className = "row flex-display"
		),
        
        
        html.Div(
					children = [
						# Title and subtitle
						html.Div(
							children = [
								html.A(
                                    "Team: Aman Choudhary", 
                                    href='https://www.linkedin.com/in/amanchoudharyy', 
                                    target="_blank",
                                    style={'text-decoration':'none',
                                           'color': '#414141',
                                           'font-weight':'bold',
                                           'font-family':'Open Sans',
                                             'font-size':'16px'}
									
								),
                                html.A(
                                    " & Danish Ranjan ", 
                                    href='https://www.linkedin.com/in/danish-ranjan-62a129168/', 
                                    target="_blank",
                                    style={'text-decoration':'none',
                                           'color': '#414141',
                                           'font-weight':'bold',
                                           'font-family':'Open Sans',
                                             'font-size':'16px'}
									
									
								),
								
							],
					id = 'title19',
                    style={
                'display': 'inline-block',
                'textAlign':'Center',
                'width': '100%',
                'background-color': 'white',
                'padding':'10px'
}
						)
					],
				
            )
	],
	id = "mainContainer",
	style = {
		"display": "flex",
		"flex-direction": "column"
	}
)

# Build the callbacks

# New confirmed cases value box
@app.callback(
	Output(
		component_id = "Confirmed",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_confirmed(state):
	# Filter the data
    fig={
		"data": [
			go.Indicator(
				mode = "number+delta",
				value = statewise[statewise['Status']=='Confirmed'][state].iloc[-1],
				delta = {
					"reference":statewise[statewise['Status']=='Confirmed'][state].iloc[-2] ,
					"position": "right",
					"valueformat": ",g",
					"relative": False,
					"font": {
						"size": 15
					}
				},
				number = {
					"valueformat": ",",
					"font": {
						"size": 20
					}
				},
				domain = {
					"y": [0, 1],
					"x": [0, 1]
				}
			)
		],
		"layout": go.Layout(
			title = {
				"text": "Confirmed Cases",
				"y": 1,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			font = {
				"color": "orange"
			},
			paper_bgcolor = "white",
			plot_bgcolor = "white",
			height = 50
		)
	}
    # Return the figure
    return fig

# Deaths value box
@app.callback(
	Output(
		component_id = "Deceased",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_deaths(state):
    # Build the figure
	fig = {
		"data": [
			go.Indicator(
				mode = "number+delta",
				value = statewise[statewise['Status']=='Deceased'][state].iloc[-1],
				delta = {
					"reference": statewise[statewise['Status']=='Deceased'][state].iloc[-2],
					"position": "right",
					"valueformat": ",g",
					"relative": False,
					"font": {
						"size": 15
					}
				},
				number = {
					"valueformat": ",",
					"font": {
						"size": 20
					}
				},
				domain = {
					"y": [0, 1],
					"x": [0, 1]
				}
			)
		],
		"layout": go.Layout(
			title = {
				"text": "Deceased ",
				"y": 1,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			font = {
				"color": "#dd1e35"
			},
			paper_bgcolor = "white",
			plot_bgcolor = "white",
			height = 50
		)
	}
	# Return the figure
	return fig


# Recovered value box
@app.callback(
	Output(
		component_id = "Recovered",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_recovered(state):
    # Build the figure
	fig = {
		"data": [
			go.Indicator(
				mode = "number+delta",
				value = statewise[statewise['Status']=='Recovered'][state].iloc[-1],
				delta = {
					"reference": statewise[statewise['Status']=='Recovered'][state].iloc[-2],
					"position": "right",
					"valueformat": ",g",
					"relative": False,
					"font": {
						"size": 15
					}
				},
				number = {
					"valueformat": ",",
					"font": {
						"size": 20
					}
				},
				domain = {
					"y": [0, 1],
					"x": [0, 1]
				}
			)
		],
		"layout": go.Layout(
			title = {
				"text": "Recoveries",
				"y": 1,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			font = {
				"color": "green"
			},
			paper_bgcolor = "white",
			plot_bgcolor = "white",
			height = 50
		)
	}
	# Return the figure
	return fig


# Recovered value box
@app.callback(
	Output(
		component_id = "active",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_active(state):
    dt=statewise[statewise['Status']=='Deceased'][state].iloc[-1]
    rt=statewise[statewise['Status']=='Recovered'][state].iloc[-1]
    ct=statewise[statewise['Status']=='Confirmed'][state].iloc[-1]
    dy=statewise[statewise['Status']=='Deceased'][state].iloc[-2]
    ry=statewise[statewise['Status']=='Recovered'][state].iloc[-2]
    cy=statewise[statewise['Status']=='Confirmed'][state].iloc[-2]
    
    # Build the figure
    fig = {
		"data": [
			go.Indicator(
				mode = "number+delta",
				value = ct-dt-rt,
				delta = {
					"reference": cy-ry-dy,
					"position": "right",
					"valueformat": ",g",
					"relative": False,
					"font": {
						"size": 15
					}
				},
				number = {
					"valueformat": ",",
					"font": {
						"size": 20
					}
				},
				domain = {
					"y": [0, 1],
					"x": [0, 1]
				}
			)
		],
		"layout": go.Layout(
			title = {
				"text": "Active Cases",
				"y": 1,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			font = {
				"color": "#e55467"
			},
			paper_bgcolor = "white",
			plot_bgcolor = "white",
			height = 50
		)
	}
	# Return the figure
    return fig

# Donut chart
@app.callback(
	Output(
		component_id = "pie_chart",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_pie_chart(state):
    # Calculate values
	confirmed_value = statewise[statewise['Status']=="Confirmed"][state].sum()
	deaths_value = statewise[statewise['Status']=="Deceased"][state].sum()
	recovered_value = statewise[statewise['Status']=="Recovered"][state].sum()
	active_value = confirmed_value-deaths_value-recovered_value
	# List of colors
	colors = ["#01B075","orange","#dd1e35"]
	# Build the figure
	fig = {
		"data": [
			go.Pie(
				labels = [ "Recovered Cases", "Active Cases","Total Deaths"],
				values = [recovered_value, active_value,deaths_value],
				marker = {
					"colors": colors
				},
				hoverinfo = "percent",
				textinfo = "label+value",
				hole = 0.5,
				rotation = 45,
				insidetextorientation = "radial",
                pull=[0,0,0.1]
			)
		],
		"layout": go.Layout(
			title = {
				"text": f"Total Cases",
				"y": 0.93,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			titlefont = {
				"color": "black",
				"size": 22
			},
			font = {
				"family": "calibri",
				"color": "black",
				"size": 14
			},
			hovermode = "closest",
			paper_bgcolor = "white",
			plot_bgcolor = "white",
			legend = {
				"orientation": "h",
				"bgcolor": "white",
				"xanchor": "center",
				"x": 0.5,
				"y": 0
			}
		)
	}
	# Return the figure
	return fig


# Line and bars chart

@app.callback(
	Output(
		component_id = "line_chart",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_line_chart(state):
	# Filter the data
	cases30D = (statewise[statewise["Status"]=="Confirmed"][state])
	avg30D = cases30D.rolling(window = 7).mean()
	# Build the figure
	fig = {
		"data": [
			go.Bar(
				x = statewise[statewise["Status"]=="Confirmed"]["Date"].tail(30),
				y = cases30D.tail(30),
				name = "Daily confirmed cases",
				marker = {
					"color": "tomato"
				},
				hoverinfo = "text",
				hovertemplate = "<b>Date</b>: %{x} <br><b>Daily confirmed</b>: %{y:,.0f}<extra></extra>"
			),
			go.Scatter(
				x = statewise[statewise["Status"]=="Confirmed"]["Date"].tail(30),
				y = avg30D.tail(30),
				name = "Rolling avg. of the last 7 days - daily confirmed cases",
				mode = "lines",
				line = {
					"width": 3,
					"color": "black"
				},
				hoverinfo = "text",
				hovertemplate = "<b>Date</b>: %{x} <br><b>Rolling Avg.</b>: %{y:,.0f}<extra></extra>"
			)
		],
		"layout": go.Layout(
			title = {
				"text": f"Confirmed Cases in Last 30 Days",
				"y": 0.93,
				"x": 0.5,
				"xanchor": "center",
				"yanchor": "top"
			},
			titlefont = {
				"color": "black",
				"size": 20
			},

			yaxis = {
				"title": "<b>Confirmed cases</b>",
				"color": "black",
				"showline": True,
				"showgrid": True,
				"showticklabels": True,
				"linecolor": "black",
				"linewidth": 1,
				"ticks": "outside",
				"tickfont": {
					"family": "Aerial",
					"color": "white",
					"size": 12
				}
			},
			font = {
				"family": "sans-serif",
				"color": "black",
				"size": 14
			},
			hovermode = "closest",
			paper_bgcolor = "white",
			plot_bgcolor = "white",
			legend = {
				"orientation": "h",
				"bgcolor": "white",
				"xanchor": "center",
				"x": 0.5,
				"y": -0.7
			}
		)
	}
	# Return the figure
	return fig


# Map
@app.callback(
	Output(
		component_id = "map_chart",
		component_property = "figure"
	),
	Input(
		component_id = "state",
		component_property = "value"
	)
)
def update_map(state):
	# Build the figure
    size=statewise.groupby(['Status']).sum().iloc[0][1:38].to_list()
    fig = {
		"data": [
			go.Scattermapbox(
				lon = loc['Longitude'].to_list(),
				lat = loc['Latitude'].to_list(),
				mode = "markers",
                text = statecode["State Name"][1:38].to_list(),
				marker = go.scattermapbox.Marker(
					size = [x/1000 for x in size],
					color = "red",
					colorscale = "HSV",
					showscale = False,
					sizemode = "area",
					opacity = 0.5
				),)
		],
		"layout": go.Layout(
			hovermode = "x",
			paper_bgcolor = "#1f2c56",
			plot_bgcolor = "#1f2c56",
			margin = {
				"r": 0,
				"l": 0,
				"t": 0,
				"b": 0
			},
			mapbox = dict(
				accesstoken = "pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw",
				center = go.layout.mapbox.Center(
					lat = 20.148,
					lon = 82.08
				),
				style = "light",
				zoom = 3
			),
			autosize = True
		)
	}
	# Return the figure
    return fig

@app.callback(Output('table1', 'children'),
              Input('city', 'value'),
              Input('essentials', 'value'))
def input_triggers_spinner(city,ess):
    squery=city+" "+ess+" available verified"
    
    df = [r._json for r in api.search(q=squery,result_type='recent',tweet_mode='extended',count=100)]
    df = pd.json_normalize(df)
    og=df[~df['retweeted_status.full_text'].isnull()][s2]
    nog=df[df['retweeted_status.full_text'].isnull()][s1]
    og.columns=s1
    df=pd.concat([nog,og]).drop_duplicates(subset=['full_text'], keep='first',ignore_index=True)
    df["id_str"]= 'https://twitter.com/twitter/statuses/' + df["id_str"]
    for i in df.index:
        df.at[i,'created_at']=datetime.strftime(datetime.strptime(df.at[i,'created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    df=df.sort_values(by=['created_at'],ascending=False,ignore_index=True)   
    t=datetime.now(pytz.timezone('GMT')).strftime("%Y-%m-%d %H:%M:%S")
    for i in df.index:
        df.at[i,'created_at']=timeago.format(df.at[i,'created_at'],t)
    rows = []
    links = df['id_str'].to_list()
    for x in links:
        link = '[Link](' +str(x) + ')'
        rows.append(link) 
    df['id_str']=rows
    df=df.to_dict('records')
    return dt.DataTable(style_table={
        'overflowY': 'scroll'
        
        },
        style_data={'whiteSpace': 'normal',
                    'height':'auto'},
                        page_size=5,
        data=df,
        style_cell={'textAlign': 'left',
                    'padding': '15px',
                    'margin':'5px',
                    'font-size':'14px',
                    'font-family':'Open Sans'},
        style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'center'
        } for c in ['Likes', 'Replies','ReTweets','URL','Date']
    ],
    style_header={
        'backgroundColor': '#414141',
        'fontWeight': 'bold',
        'color':'white',
        'border': '1px solid black'
    },
    sort_action='native',
        columns=[{'name': 'Tweet', 'id':'full_text'}, 
                 {'name': 'Date', 'id':'created_at'}, 
                 {'name': 'URL', 'id':'id_str','type':'text','presentation':'markdown'},                 
                 {'name': 'Followers', 'id':'user.followers_count'},
                 {'name': 'ReTweets', 'id':'retweet_count'},
                 {'name': 'Username', 'id':'user.name'},  
                 {'name': 'Name', 'id':'user.screen_name'}, 
                 {'name': 'Verified?', 'id':'user.verified'},
                 {'name': 'Favourites', 'id':'user.favourites_count'}
                 ]
)




# Run the app
if __name__ == "__main__":
  app.run_server()
