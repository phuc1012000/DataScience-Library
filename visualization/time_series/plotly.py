import plotly.graph_objs as go
import plotly.offline as py
import pandas as pd

py.init_notebook_mode(connected=True)

def base_line(df, column, hue ,title_figure = 'Trend', x_title = None, y_title = 'Count', _list = None):
    data = []

    if x_title is None:
        x_title = column

    if _list is None:
        _list = list(df[hue].value_counts().index)

    for values in _list:
        _df = df.loc[df[hue] == values]

        data.append(go.Scatter(
            x = _df[column].value_counts().sort_index().index,
            y = _df[column].value_counts().sort_index().values,
            name = str(values)
        ))

    layout = go.Layout(dict(title = title_figure,
                      xaxis = dict(title = x_title),
                      yaxis = dict(title = y_title),
                      )
                      )

    py.iplot(dict(data=data, layout=layout), filename='basic-line')
