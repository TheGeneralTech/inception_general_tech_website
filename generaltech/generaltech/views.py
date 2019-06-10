from django.shortcuts import render
from django.http import Http404

import datetime
import requests

def index(request):
    result = requests.get('https://api.pinkadda.com/v1/posts/published?project=pinkadda&limit=10&offset=0')
    date = getDate()
    context = {'date': date}
    return render(request, 'generaltech/index.html', context)

def article(request, article_id):
    #raise Http404("Article not found")
    pass

def writer(request, writer_id):
    pass

def getDate():
    date = datetime.datetime.now()
    return date.strftime("%A, %d %b %Y")