from django.shortcuts import render
from django.http import Http404

import datetime
import requests

def index(request):
    response = requests.get('https://api.pinkadda.com/v1/posts/published?project=pinkadda&limit=10&offset=0')
    response_dict = response.json()
    posts = response_dict['posts']
    posts = posts[3:] #fix_me remove this later
    featured_posts = response_dict['featured']
    main_article = featured_posts[0] #fix_me after main_article post type is defined in the api
    date = getDate()
    context = {
        'date': date,
        'posts': posts,
        'featured_posts': featured_posts,
        'main_article': main_article,
    }
    return render(request, 'generaltech/index.html', context)

def article(request, article_id):
    #raise Http404("Article not found")
    pass

def writer(request, writer_id):
    pass

def getDate():
    date = datetime.datetime.now()
    return date.strftime("%A, %d %b %Y")