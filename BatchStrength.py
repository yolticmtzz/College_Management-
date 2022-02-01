import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from matplotlib.pyplot import title
import plotly.express as px
import pandas as pd
import pyodbc as py
server = 'd2mtrainingdb.database.windows.net'
db = 'd2manalysistraining'
user = 'dbtuser'
pwd = 'Disys@2022'


conn = py.connect('DRIVER={SQL Server};SERVER=' + server +
                      ';DATABASE=' + db +
                      '; UID=' + user +
                      '; PWD=' + pwd +
                      ';Trusted_Connection=no')
cursor = conn.cursor()
df = pd.read_sql_query('execute vdp_total_stud',conn)
all_Batch =df.Batch.unique()
app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout =html.Div([
        dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x} 
                    for x in all_Batch],
            value=all_Batch[:1],
            #labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="pie-chart"),
    ])
@app.callback(
    Output("pie-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(all_Batch):
    mask = df.Batch.isin(all_Batch)

    fig = px.pie(df[mask], names='DEPT', values='Strength',color= 'DEPT',labels='DEPT', 
    title='Strength By Dept for Vadapalani', template='presentation')
    fig.update_layout( title_x=0.5)
   
    return fig

app.run_server(debug=True)