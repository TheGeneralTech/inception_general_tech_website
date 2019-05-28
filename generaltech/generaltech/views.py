from django.shortcuts import render
from django.http import Http404

def index(request):
    context = {}
    return render(request, 'generaltech/index.html', context)

def article(request, article_id):
    #raise Http404("Article not found")
    pass