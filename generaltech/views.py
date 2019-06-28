from django.shortcuts import render
from django.http import Http404

import datetime
import requests
from requests.exceptions import HTTPError


def index(request):
    date = getDate()
    context = {'date': date, }
    try:
        response = requests.get(
            'https://api.pinkadda.com/v1/posts/published',
            params={
                'project': 'pinkadda',
                'limit': '10',
                'offset': '0'
            }
        )
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error occured: {http_error}')
        raise Http404("Page does not exist")
    except Exception as err:
        print(f'Other error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        posts = response_dict['posts']
        posts = list(map(formatPost, posts))
        posts = posts[3:]  # fix_me remove this later
        featured_posts = response_dict['featured']
        featured_posts = list(map(formatPost, featured_posts))
        # fix_me after main article post type is defined in the api
        main_article = featured_posts[0]
        context['posts'] = posts
        context['featured_posts'] = featured_posts
        context['main_article'] = main_article
    return render(request, 'generaltech/index.html', context)


def article(request, article_id):
    raise Http404("Article not found")


def writer(request, writer_id):
    raise Http404("Article not found")


def getDate():
    d = datetime.datetime.now()
    return d.strftime("%A, %d %b %Y")


def formatPost(post):
    post['created_on'] = formatCreationDate(post['created_on'])
    return post


def formatCreationDate(timestamp):
    # Timestamp coverted into miliseconds for compatibility
    d = datetime.datetime.fromtimestamp(timestamp/1000)
    if d.date() == datetime.date.today():
        return "Today at " + d.strftime("%I:%M %p")
    elif d.date() == datetime.date.today() - datetime.timedelta(days=1):
        return "Yesterday at " + d.strftime("%I:%M %p")
    else:
        return d.strftime("%b %d, %Y")
