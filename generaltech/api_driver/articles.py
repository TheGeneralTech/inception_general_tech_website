import requests
from requests.exceptions import HTTPError
import random
import datetime
from django.http import Http404

from django.conf import settings

class Articles:

    def getContentFromApi(self, parameters, published=True, req_type=None):
        try:
            URL = f'{settings.API_ADDR}/{settings.API_VER}/posts'
            if published:
                URL += '/published'
            if req_type != None:
                URL += f'/{req_type}'
            response = requests.get(URL, params=parameters)
            response.raise_for_status()
        except HTTPError as http_error:
            print(f'HTTP error occured: {http_error}')
            raise Http404("Page does not exist")
        except Exception as err:
            print(f'Some error occured: {err}')
            raise Http404("Page does not exist")
        else:
            return response

    def getIndexPageArticles(self):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'limit': settings.ARTICLE_LIMIT,
            'offset': '0'
        })
        response_dict = response.json()
        articles = response_dict['posts']
        articles = list(map(self.formatArticle, articles))
        tags = response_dict['topTags']
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'limit': settings.FEATURED_LIMIT,
            'offset': '0'
        }, req_type = "featured")
        response_dict = response.json()
        featured_articles = response_dict
        featured_articles = list(map(self.formatArticle, featured_articles))
        main_article = featured_articles[0]
        featured_articles = featured_articles[1:]
        return main_article, featured_articles, articles, tags

    def getArticleContent(self, article_url):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'q_type': 'single',
            'url': article_url,
            'suggestions': settings.RELATED_ARTICLE_COUNT
        })
        response_dict = response.json()
        response_dict['titleImage']['height_perc'] = 1/response_dict['titleImage']['data-aspect-ratio']*100
        response_dict['created_on'] = self.formatCreationDate(response_dict['created_on'])
        response_dict['suggestions'] = list(map(
            self.formatArticle, response_dict['suggestions']
        ))
        response_dict['url'] = f'{settings.WEBSITE_ADDR}/article/{response_dict["url"]}'
        response_dict['twitter_acc'] = settings.TWITTER_ACC
        return response_dict

    def getDraftContent(self, article_uuid):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'q_type': 'single',
            'uuid': article_uuid,
            'suggestions': settings.RELATED_ARTICLE_COUNT
        }, published=False, req_type="drafts")
        response_dict = response.json()
        response_dict['created_on'] = self.formatCreationDate(response_dict['created_on'])
        response_dict['suggestions'] = list(map(
            self.formatArticle, response_dict['suggestions']
        ))
        response_dict['url'] = f'{settings.WEBSITE_ADDR}/draft/{response_dict["url"]}'
        response_dict['twitter_acc'] = settings.TWITTER_ACC
        return response_dict

    def getAuthorArticlesAndDetails(self, author_id):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'q_type': 'default',
            'limit': settings.ARTICLE_LIMIT,
            'offset': '0',
            'authorUsername': author_id
        }, req_type = "authors")
        response_dict = response.json()
        articles = response_dict['posts']
        articles = list(map(self.formatArticle, articles))
        return response_dict['author'], articles

    def getTagArticlesAndDetails(self, tag_id):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'q_type': 'default',
            'limit': settings.ARTICLE_LIMIT,
            'offset': '0',
            'tag': tag_id
        }, req_type = "tags")
        response_dict = response.json()
        articles = response_dict['posts']
        articles = list(map(self.formatArticle, articles))
        return response_dict['tag'], articles

    def getIndexFeedArticles(self, page_num):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'limit': settings.ARTICLE_LIMIT,
            'offset': page_num * settings.ARTICLE_LIMIT
        })
        response_dict = response.json()
        articles = response_dict['posts']
        articles = list(map(self.formatArticle, articles))
        return articles, response_dict['hasMore']

    def getAuthorFeedArticles(self, author_id, page_num):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'q_type': 'default',
            'limit': settings.ARTICLE_LIMIT,
            'offset': page_num * settings.ARTICLE_LIMIT,
            'authorUsername': author_id
        }, req_type = "authors")
        response_dict = response.json()
        articles = response_dict['posts']
        articles = list(map(self.formatArticle, articles))
        return articles, response_dict['hasMore']

    def getTagFeedArticles(self, tag_id, page_num):
        response = self.getContentFromApi(parameters={
            'project': settings.PROJECT_UUID,
            'q_type': 'default',
            'limit': settings.ARTICLE_LIMIT,
            'offset': page_num * settings.ARTICLE_LIMIT,
            'tag': tag_id
        }, req_type = "tags")
        response_dict = response.json()
        articles = response_dict['posts']
        articles = list(map(self.formatArticle, articles))
        return articles, response_dict['hasMore']

    def formatArticle(self, article):
        article['created_on'] = self.formatCreationDate(article['created_on'])
        return article

    def formatCreationDate(self, timestamp):
        # Timestamp coverted into miliseconds for compatibility
        d = datetime.datetime.fromtimestamp(timestamp / 1000)
        if d.date() == datetime.date.today():
            return "Today at " + d.strftime("%I:%M %p")
        elif d.date() == datetime.date.today() - datetime.timedelta(days=1):
            return "Yesterday at " + d.strftime("%I:%M %p")
        else:
            return d.strftime("%b %d, %Y")
