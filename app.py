import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

GC_METRICS = ['GCPauseTimePercentage', 'HeapCount',
       'MaxAllocRateMBSec', 'MaxSizePeakMB', 'MaxSuspendDurationMSec',
       'MeanCpuMSec', 'MeanPauseDurationMSec', 'MeanSizeAfterMB',
       'MeanSizePeakMB', 'NumInduced', 'NumWithPinEvents',
       'NumWithPinPlugEvents', 'PinnedObjectPercentage', 'PinnedObjectSizes',
       'ProcessDuration', 'TotalAllocatedMB', 'TotalCpuMSec',
       'TotalPauseTimeMSec', 'TotalPromotedMB', 'TotalSizeAfterMB',
       'TotalSizePeakMB']

df = pd.read_csv('./scripts/test.csv')

app = dash.Dash()
GC_METRIC_UNITS = {
    'GCPauseTimePercentage': '%',
    'HeapCount': 'Count',
    'MaxAllocRateMBSec': 'MB',
    'MaxSizePeakMB': 'MB',
    'MaxSuspendDurationMSec': 'MSec',
    'MeanCpuMSec': 'MSec',
    'MeanPauseDurationMSec': 'MSec',
    'MeanSizeAfterMB': 'MB',
    'MeanSizePeakMB': 'MB',
    'NumInduced': 'Count',
    'NumWithPinEvents': 'Count',
    'NumWithPinPlugEvents': 'Count',
    'PinnedObjectPercentage': '%',
    'PinnedObjectSizes': 'Count',
    'ProcessDuration': 'Sec',
    'TotalAllocatedMB': 'MB',
    'TotalCpuMSec': 'MSec',
    'TotalPauseTimeMSec': 'MSec',
    'TotalPromotedMB': 'MB',
    'TotalSizeAfterMB': 'MB',
    'TotalSizePeakMB': 'MB'
}

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-metricname',
                options=[{'label': i, 'value': i} for i in GC_METRICS],
                value='GCPauseTimePercentage'
            ),
            dcc.Dropdown(
                id='crossfilter-testname',
                options=[{'label': i, 'value': i} for i in df.Test.unique()],
                value='Legacy@ConcurrentSpin'
            ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(
            id='test-graph'
        )
    ])
])


@app.callback(
    dash.dependencies.Output('test-graph', 'figure'),
    [dash.dependencies.Input('crossfilter-metricname', 'value'),
    dash.dependencies.Input('crossfilter-testname', 'value')]
)
def update_metric(metric, test):
    print(metric)
    print(test)
    return {
        'data': [
            go.Scatter(
                x=df['Date'],
                y=df[df['Test'] == test][metric],
                mode='markers',
                name=metric,
                opacity=0.7
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': GC_METRIC_UNITS[metric]},
        )
    }



if __name__ == '__main__':
    app.run_server()
