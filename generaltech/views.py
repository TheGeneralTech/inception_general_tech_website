from django.shortcuts import render
from django.http import Http404

import datetime
import requests
import mistune
from requests.exceptions import HTTPError


def index(request):
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'project': 'pinkadda',
                                    'limit': '20',
                                    'offset': '0'
                                })
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
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'q_type': 'single',
                                    'url': article_id
                                })
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error occured: {http_error}')
        raise Http404('Page does not exist')
    except Exception as err:
        print(f'Other error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        context['a_title'] = response_dict['title']
        context['a_titleImage'] = response_dict['titleImage']
        context['a_text'] = mistune.markdown(response_dict['description'])
        context['a_created_on'] = formatCreationDate(
            response_dict['created_on'])
        context['author_url'] = response_dict['author'] #fixe_me
        context['author'] = response_dict['author'] #fixe_me
    return render(request, 'generaltech/article.html', context)


def author(request, author_id): #fix_me
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'project': 'pinkadda',
                                    'limit': '20',
                                    'offset': '0'
                                })
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
        context['author'] = author_id #fixe_me
        context['posts'] = posts
    return render(request, 'generaltech/author.html', context)


def tag(request, tag_id):
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'project': 'pinkadda',
                                    'limit': '20',
                                    'offset': '0'
                                })
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
        context['tag'] = tag_id #fixe_me
        context['posts'] = posts
    return render(request, 'generaltech/tag.html', context)

def newsletter(request):
    pass


def getBaseContext():
    date = getDate()
    context = {
        'date': date,
    }
    return context

def getDate():
    d = datetime.datetime.now()
    return d.strftime("%A, %d %b %Y")


def formatPost(post):
    post['created_on'] = formatCreationDate(post['created_on'])
    return post


def formatCreationDate(timestamp):
    # Timestamp coverted into miliseconds for compatibility
    d = datetime.datetime.fromtimestamp(timestamp / 1000)
    if d.date() == datetime.date.today():
        return "Today at " + d.strftime("%I:%M %p")
    elif d.date() == datetime.date.today() - datetime.timedelta(days=1):
        return "Yesterday at " + d.strftime("%I:%M %p")
    else:
        return d.strftime("%b %d, %Y")
