import pandas as pd

import dash
from dash.dependencies import Input , Output
import dash_core_components as dcc 
import dash_html_components as html
import webbrowser
import plotly.graph_objects as go
import plotly.express as px



app = dash.Dash()
app.title = 'Terrorism Data Analysis'


def load_data():
    
    globalterror = 'global_terror.csv'
    
    global df
    df = pd.read_csv(globalterror) 
       
    month = {
            "January"  :  1,
            "February" :  2,
            "March"    :  3,
            "April"    :  4,
            "May"      :  5,
            "June"     :  6,
            "July"     :  7,
            "August"   :  8,
            "September":  9,
            "October"  : 10,
            "November" : 11,
            "December" : 12
           }


    global month_list   
    month_list=[{"label":key , "value": values} for key,values in month.items()]    
    
    global date_list
    date_list =[{"label": i , "value": i}  for i in  range(1,32) ]
    
    
    global region_list
    region_list =[{"label": str(i) , "value": str(i)}  for i in sorted(df['region_txt'].unique().tolist())]
    
    global country_list
    #country_list = [{"label": str(i) , "value": str(i)}  for i in sorted(df['country_txt'].unique().tolist())] # check .tolist()
    country_list=df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()
    
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
 
    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    
    global attacktype_list
    attacktype_list = [{"label": str(i) , "value": str(i)}  for i in (df['attacktype1_txt'].unique().tolist())]
   
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict = {str(year) : str(year) for year in year_list}
    
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                               
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
    




def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    

def create_app_ui():
    
    main_layout = html.Div(
    [    
    html.H1(id='Main_title', children='Terrorism Analysis with Insights'),
    html.Hr(),
    dcc.Tabs(id="Tabs", value="Map",children=[
        dcc.Tab(label="Map tool" ,id="Map-tool",value="Map", children=[
              dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
              ]),
        
        #html.H3(id='filter_title', children='Filters'),
        html.Br(),
        
        html.Div([
            html.Br(),
            html.Br(),
        html.Table([
                
                html.Tr([
                    
                    html.Td([
                        html.Table([
                        html.Tr([
                                            
                            html.Td([
                                        html.H4(id='loc_hed',children=' ') 
                                        
                                  ])
                            
                            ]),
                        
                        html.Tr([
                                            
                            html.Td([
                                        dcc.Dropdown( 
                                                        id='region-dropdown',
                                                        options = region_list,
                                                        multi=True,
                                                        placeholder='select region',
                                                    )                                
                                  ])
                            
                            ]),
                        html.Tr([
                            
                            html.Td([
                                        dcc.Dropdown( 
                                                        id='country-dropdown',
                                                        options = [{'label': 'All', 'value': 'All'}],
                                                        multi=True,
                                                        placeholder='select country',
                                                    ),
                                  ])
                            
                            ]),
                        html.Tr([
                            
                            html.Td([
                                      dcc.Dropdown( 
                                                        id='state-dropdown',
                                                        options = [{'label': 'All', 'value': 'All'}],
                                                        multi=True,
                                                        placeholder='select state',
                                                    ),
                                ])
                            
                            ]),
                        html.Tr([
                            
                            html.Td([
                                        dcc.Dropdown( 
                                                        id='city-dropdown',
                                                        options = [{'label': 'All', 'value': 'All'}],
                                                        multi=True,
                                                        placeholder='select city'
                                                    ),
                                
                                ])
                            
                            ])
                        
                       ]), 
                        
                        ]),
                    html.Td([
                        html.Table([
                         html.Tr([
                                            
                            html.Td([
                                        html.H4(id='time_hed',children=' ')                                
                                  ])
                            
                            ]),
                            
                            
                         html.Tr([
                            
                            html.Td([
                                      dcc.Dropdown( 
                                                        id='month-dropdown',
                                                        options = month_list,
                                                        multi=True,
                                                        placeholder='select month'
                                                 ),
                                ])
                            
                            ]),
                        html.Tr([
                            
                            html.Td([
                                     dcc.Dropdown( 
                                                        id='date-dropdown',
                                                        options = date_list,
                                                        multi=True,
                                                        placeholder='select date'
                                                    ),
                                ])
                            
                            ]),
                        html.Tr([
                            
                            html.Td([
                                      dcc.Dropdown( 
                                                        id='attacktype-dropdown',
                                                        options = attacktype_list,
                                                        multi=True,
                                                        placeholder='select attacktype'
                                                    ),
                                ])
                            
                            ]),
                        
                        ]),
                        ]),
                    
                    
                    ]),
                
           
                ]),
        html.Br(),
        html.Br(),
        html.Br(),
        ],id='table_div',style = {'background-image': 'url(/assets/xyz.png)','background-repeat':'no-repeat'}),
       
        
       
        html.Br(),
        html.Hr(),
        html.Br(),
            
        dcc.RangeSlider(
            id = 'year-slider',
            min = min(year_list),
            max = max(year_list),
            value=[min(year_list),max(year_list)],
            marks= year_dict,
            ),
        
        
        html.Hr(),
            
        html.Br(),
     ]),

        dcc.Tab(label = "Chart Tool", id="chart-tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
            dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
            html.Br(),
            
            html.Div([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Input(id="search", placeholder="Search Filter"),
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            ],id='chart_back',style = {'background-image': 'url(/assets/xyz.png)','background-repeat':'no-repeat'}),
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
            html.Hr(),
            html.Br()
              ]),
      
         ]),
        
        dcc.Loading(id='graph-object',type='graph')   
        #html.Div(id='graph-object', children = ["World Map is loading...."]) ,
        
    ]  
    )
    
    return main_layout


@app.callback(
    Output("date-dropdown","options"),
    [
    Input("month-dropdown","value"),
    ]
    )
def update_date(month):
    date_list = [x for x in range(1, 32)]
    option = []
    
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option
       

@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def update_country(region_value):
    
    option = []
    if region_value is  None:
        option = []
    else:
        for i in region_value:
            if i in country_list.keys():
                option.extend(country_list[i])
    return [{'label':i , 'value':i} for i in option]

@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def update_state(country_value):
  
    option = []
    if country_value is None :
        option = []
    else:
        for i in country_value:
            if i in state_list.keys():
                option.extend(state_list[i])
    return [{'label':i , 'value':i} for i in option]


@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def update_city(state_value):
  
    option = []
    if state_value is None:
        option = []
    else:
        for i in state_value:
            if i in city_list.keys():
                option.extend(city_list[i])
    return [{'label':i , 'value':i} for i in option]

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c


@app.callback(
    dash.dependencies.Output('graph-object', 'children' ),
    [
    dash.dependencies.Input('region-dropdown','value'),
    dash.dependencies.Input('country-dropdown','value'),
    dash.dependencies.Input('state-dropdown','value'),
    dash.dependencies.Input('city-dropdown','value'),
    dash.dependencies.Input('date-dropdown','value'),
    dash.dependencies.Input('month-dropdown','value'),
    dash.dependencies.Input('year-slider','value'),
    dash.dependencies.Input('attacktype-dropdown','value'),
    dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('cyear_slider', 'value'), 
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )
def update_app_ui(region_value,country_value,state_value,city_value,date_value,month_value,year_value,attacktype_value,Tabs,chart_year_selector, chart_dp_value, search,subtabs2):
    
    fig = None
     
    if Tabs == "Map":        
            print("region value passed is = "+ str(region_value))
            print("region data type  = "+ str(type(region_value)))
        
            print("country value passed is = "+ str(country_value))
            print("country data type  = "+ str(type(country_value)))
        
            print("state value passed is = "+ str(state_value))
            print("state data type  = "+ str(type(state_value)))
        
            print("city value passed is = "+ str(city_value))
            print("city data type  = "+ str(type(city_value)))
        
            print("date value passed is = "+ str(date_value))
            print("date data type  = "+ str(type(date_value)))
        
            print("month value passed is = "+ str(month_value))
            print("month data type  = "+ str(type(month_value)))
        
            print("year value passed is = "+ str(year_value))
            print("year data type  = "+ str(type(year_value)))
        
            print("attacktype value passed is = "+ str(attacktype_value))
            print("attacktype data type  = "+ str(type(attacktype_value)))
        
            
            
            year_range = range(year_value[0], year_value[1]+1)
            new_df = df[df["iyear"].isin(year_range)]
            
            
            if month_value==[] or month_value is None:
                pass
            else:
                if date_value==[] or date_value is None:
                    new_df = new_df[new_df["imonth"].isin(month_value)]
                else:
                    new_df = new_df[new_df["imonth"].isin(month_value)
                                    & (new_df["iday"].isin(date_value))]
            
            
            if region_value==[] or region_value is None:
               pass
            else:
                if country_value==[] or country_value is None :
                    new_df = new_df[new_df["region_txt"].isin(region_value)]
                else:
                    if state_value == [] or state_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                        (new_df["country_txt"].isin(country_value))]
                    else:
                        if city_value == [] or city_value is None:
                            new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value))]
                        else:
                            new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                            (new_df["country_txt"].isin(country_value)) &
                                            (new_df["provstate"].isin(state_value))&
                                            (new_df["city"].isin(city_value))]
            
            if attacktype_value == [] or attacktype_value is None:
                pass
            else:
                new_df = new_df[new_df["attacktype1_txt"].isin(attacktype_value)]
            
            
            figure = go.Figure()
            
            
            if new_df.shape[0]:
                pass
            else: 
                new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
                
                new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
        
            
            figure = px.scatter_mapbox(new_df,
                                       lat="latitude",
                                       lon="longitude",
                                       hover_data=["region_txt","country_txt","provstate","city","attacktype1_txt","nkill","iyear"],
                                       zoom=1.3,
                                       height=600,
                                       color="attacktype1_txt"
                                      )
            figure.update_layout( mapbox_style ='open-street-map',
                                  autosize = True,
                                  margin = dict(l=0, r=0,t=25,b=20),
                                  legend=dict(
                                                orientation="h",
                                                yanchor="top",
                                                y=1.02,
                                                xanchor="center",
                                                x=1
                                             )
                                )
            fig = figure
            
    elif Tabs=="Chart":
        fig = None
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value,template='presentation')
        fig = chartFigure        
            
            
    return dcc.Graph(figure=fig)


def main():
    print("Welcome to terrosism data analysis")

    load_data()
    open_browser()

    global app
    app.layout = create_app_ui()
    
    app.run_server()
    
    print("thanks for using, see you again")

    app = None
    df = None

if __name__ == '__main__':  
   main()