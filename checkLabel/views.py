from django.http import HttpResponse,JsonResponse
from django.template import loader
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from django.shortcuts import render

from checkLabel import scripts
from decouple import config
URL = "http://procyon.tce.pi.gov.br:6900/datasets/"
def home(request):
    api_url = config("ARGILLA_API_URL")
    api_key = config("ARGILLA_API_KEY")
    datasets = scripts.get_dataset_list(api_url,api_key)
    home = loader.get_template('checkLabel/index.html')
    x = [1, 2, 3, 4, 5]
    y1 = [10, 20, 30, 40, 50]
    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(
        width=400,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(229, 229, 229)',
    )
    fig.add_trace(go.Scatter(x=x, y=y1, name='Linha 1'), row=1, col=1)
    plot_div = fig.to_html(full_html=False, config={"displayModeBar": False, "scrollZoom": False})
    
    context = {
        'plot_div': plot_div, 
        'datasets': datasets   
    }
    selected_item = request.GET.get('item')
    if len(datasets) == 0:
        context['choose'] = URL
    elif not selected_item:
        selected_item = datasets[0]['name']
    context['choose'] = URL+"admin/"+selected_item
    context['dt_complete'] = [dt for dt in datasets if dt['name'] == selected_item][0]
    return HttpResponse(home.render(context, request))

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def graficos(request):
    dados = request.body
    dados = json.loads(dados)

    batch = []
    acc_x = []
    hammings_loss = []
    inv_hammings_loss = []
    trusting = []

    for i in dados:
        acc_x.append(i['accuracy']*100)
        hammings_loss.append(i['hamming_loss'])
        inv_hammings_loss.append((1-i['hamming_loss'])*100)
        trusting.append(i['trusting'])
        batch.append(i['batch_id']) 

    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(
        width=400,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(229, 229, 229)',
    )
    fig.update_xaxes(range = [0,len(batch)-1])
    fig.update_yaxes(range = [0,100])
    fig.add_trace(go.Scatter(x=batch, y=inv_hammings_loss, name='Concordância'), row=1, col=1)
    plot_div_inv_hamming_loss = fig.to_html(full_html=False, config={"displayModeBar": False, "scrollZoom": False})
    return JsonResponse({'graph_inv_hamming_loss': plot_div_inv_hamming_loss})