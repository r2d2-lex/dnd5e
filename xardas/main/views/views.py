from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import TemplateDoesNotExist


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    return render(request, 'main/index.html')
