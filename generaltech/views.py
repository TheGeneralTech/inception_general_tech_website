from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string

import datetime
import requests
import mistune
from requests.exceptions import HTTPError
import copy

article_limit = 20

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
        print(f'Some error occured: {err}')
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


def index_pages(request, page_num):
    page_num -= 1
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'project': 'pinkadda',
                                    'limit': article_limit,
                                    'offset': page_num * article_limit,
                                })
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error occured: {http_error}')
        raise Http404("Page does not exist")
    except Exception as err:
        print(f'Some error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        posts = response_dict['posts']
        posts = list(map(formatPost, posts))
        context['posts'] = posts
        rendered_posts = render_to_string('generaltech/normal_articles.html', context)
        json_response = {
            'hasMore': response_dict['hasMore'],
            'posts': rendered_posts,
        }
        return JsonResponse(json_response)


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
        print(f'Some error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        response_dict['description'] = mistune.markdown(response_dict['description'])
        response_dict['created_on'] = formatCreationDate(response_dict['created_on'])
        response_dict['inshort'] = False
        context['article'] = response_dict
    return render(request, 'generaltech/article.html', context)


def article_related(request, article_id):
    """Return related articles"""
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'q_type': 'single',
                                    'url': article_id
                                })
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error ocurred: {http_error}')
        raise Http404('Page does not exist')
    except Exception as err:
        print(f'Some errror ocurred: {err}')
        raise Http404('Page does not exist')
    else:
        ###### Retrieve related posts from api fix_me
        response_dict = response.json()
        response_dict['description'] = mistune.markdown(response_dict['description'])
        response_dict['created_on'] = formatCreationDate(response_dict['created_on'])
        response_dict['inshort'] = True
        related_articles = [ copy.copy(response_dict), copy.copy(response_dict), copy.copy(response_dict) ]
        related_articles[0]['url'] += str(0)
        related_articles[1]['url'] += str(1)
        related_articles[2]['url'] += str(2)
        ######
        rendered_articles = {}
        related_articles[-1]['inshort'] = False
        for article in related_articles:
            context['article'] = article
            rendered_articles[article['url']] = render_to_string('generaltech/article_template.html', context)
        json_response = {
            'articles': rendered_articles
        }
        return JsonResponse(json_response)


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
        print(f'Some error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        posts = response_dict['posts']
        posts = list(map(formatPost, posts))
        context['author'] = author_id #fixe_me
        context['posts'] = posts
    return render(request, 'generaltech/author.html', context)


def author_pages(request, author_id, page_num):
    page_num -= 1
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'project': 'pinkadda',
                                    'limit': article_limit,
                                    'offset': page_num * article_limit,
                                })
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error occured: {http_error}')
        raise Http404("Page does not exist")
    except Exception as err:
        print(f'Some error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        posts = response_dict['posts']
        posts = list(map(formatPost, posts))
        context['posts'] = posts
        rendered_posts = render_to_string('generaltech/normal_articles.html', context)
        json_response = {
            'hasMore': response_dict['hasMore'],
            'posts': rendered_posts,
        }
        return JsonResponse(json_response)


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
        print(f'Some error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        posts = response_dict['posts']
        posts = list(map(formatPost, posts))
        context['tag'] = tag_id #fixe_me
        context['posts'] = posts
    return render(request, 'generaltech/tag.html', context)


def tag_pages(request, tag_id, page_num):
    page_num -= 1
    context = getBaseContext()
    try:
        response = requests.get('https://api.pinkadda.com/v1/posts/published',
                                params={
                                    'project': 'pinkadda',
                                    'limit': article_limit,
                                    'offset': page_num * article_limit,
                                })
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error occured: {http_error}')
        raise Http404("Page does not exist")
    except Exception as err:
        print(f'Some error occured: {err}')
        raise Http404("Page does not exist")
    else:
        response_dict = response.json()
        posts = response_dict['posts']
        posts = list(map(formatPost, posts))
        context['posts'] = posts
        rendered_posts = render_to_string('generaltech/normal_articles.html', context)
        json_response = {
            'hasMore': response_dict['hasMore'],
            'posts': rendered_posts,
        }
        return JsonResponse(json_response)

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
