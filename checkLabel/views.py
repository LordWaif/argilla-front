from django.http import HttpResponse,JsonResponse
from django.template import loader
import plotly.express as px
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
    context = {
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
import plotly.graph_objs as go
@csrf_exempt
def graficos(request):
    dados = request.body
    dados = json.loads(dados)

    batch = []
    acc_x = []
    hammings_loss = []
    inv_hammings_loss = []
    jensenshannon = []
    trusting = []
    entropy = []

    for i in dados:
        acc_x.append(i['accuracy']*100)
        hammings_loss.append(i['hamming_loss'])
        inv_hammings_loss.append((1-i['hamming_loss'])*100)
        trusting.append(i['trusting'])
        jensenshannon.append((1-i['jensenshannon'])*100)
        entropy.append(i['entropy']*100)
        batch.append(i['batch_id']) 

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=batch, y=acc_x, name='Acurácia'))
    fig.add_trace(go.Scatter(x=batch, y=inv_hammings_loss, name='Concordância Simples'))
    fig.add_trace(go.Scatter(x=batch,y=jensenshannon,name='Concordância JensenShannon'))
    fig.add_trace(go.Scatter(x=batch,y=entropy,name='Entropia'))

    fig.update_layout(
        xaxis=dict(
            zeroline=True,  # Exibe uma linha de zero no eixo x
            range=[0, batch[-1]],
            title="batch"
        ),
        yaxis=dict(
            zeroline=True,  # Exibe uma linha de zero no eixo y
            range=[0, 100],
            title=""
        ),
        width=600,
        height=300,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(229, 229, 229)',
        title='Métricas'
    )
    fig.update_xaxes(
        tickmode="linear",
        dtick=1
    )
    return JsonResponse({'graph_metrics':fig.to_html(full_html=False, config={"displayModeBar": False, "scrollZoom": False})})