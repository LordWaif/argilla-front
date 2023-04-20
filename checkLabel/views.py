from django.http import HttpResponse
from django.template import loader

def home(request):
    home = loader.get_template('checkLabel/index.html')
    return HttpResponse(home.render({}, request))