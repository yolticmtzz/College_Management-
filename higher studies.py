import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from matplotlib.pyplot import text
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pyodbc as py
from plotly.subplots import make_subplots
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
df = pd.read_sql_query('Select * from PlacementPercentage',conn)
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
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="line-chart"),
    ])
@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(all_Batch):
    mask = df.Batch.isin(all_Batch)
    fig = make_subplots(rows=2, cols=1)
    fig = px.bar(df[mask], 
        x="Dept_&_Spec", y="Higher_studies", color='College_Branch', barmode= 'group', text='Higher_studies',
        text_auto='.1f', title = 'Higher Studies Percentage Over the years',template='presentation')
    fig.update_traces(textposition="inside")
    fig.update_layout( title_x=0.5)
    fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                 dict(
                    args=["type", "bar"],
                    label="Bar Chart",
                    method="restyle"
                ),
                dict(
                    args=["type", "Line"],
                    label="Line plot",
                    method="restyle"
                )
            ]),
            direction="down",
        ),
    ]
)

  
   
    return fig

app.run_server(debug=True)