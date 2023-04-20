from django.http import HttpResponse
from django.template import loader
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from django.shortcuts import render

def home(request):
    home = loader.get_template('checkLabel/index.html')
    x = [1, 2, 3, 4, 5]
    y1 = [10, 20, 30, 40, 50]
    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(
    width=auto,  # define a largura do gráfico em pixels
    height=auto,  # define a altura do gráfico em pixels
    margin=dict(l=20, r=20, t=30, b=20)  # define a margem em pixels para o gráfico
)
    fig.add_trace(go.Scatter(x=x, y=y1, name='Linha 1'), row=1, col=1)
    plot_div = fig.to_html(full_html=False, config={"displayModeBar": False, "scrollZoom": False})
    
    context = {
        'plot_div': plot_div,    
    }
    return HttpResponse(home.render(context, request))