from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.views import View

import datetime

from django.conf import settings
from .api_driver.articles import Articles


class IndexPageView(View):
    def get(self, request):
        context = getBaseContext()
        main_article, featured_articles, articles, tags =  Articles().getIndexPageArticles()
        context['posts'] = articles
        context['featured_posts'] = featured_articles
        context['main_article'] = main_article
        context['tags'] = tags[:10]
        return render(request, 'generaltech/index.html', context)


class IndexFeedView(View):
    def get(self, request, page_num):
        context = getBaseContext()
        articles, has_more = Articles().getIndexFeedArticles(page_num)
        context['posts'] = articles
        rendered_posts = render_to_string('generaltech/normal_articles.html', context)
        json_response = {
            'hasMore': has_more,
            'posts': rendered_posts,
        }
        return JsonResponse(json_response)


class ArticlePageView(View):
    def get(self, request, article_id):
        article = Articles().getArticleContent(article_id, False)
        context = getBaseContext()
        context['article'] = article
        return render(request, 'generaltech/article.html', context)


class RelatedArticleView(View):
    def get(self, request, article_id):
        """Return related articles"""
        context = getBaseContext()
        related_articles = Articles().getRelatedArticles(article_id)
        rendered_articles = {}
        for article in related_articles:
            context['article'] = article
            rendered_articles[article['url']] = render_to_string('generaltech/article_template.html', context)
        json_response = { 'articles': rendered_articles }
        return JsonResponse(json_response)


class DraftPageView(View):
    def get(self, request, article_id):
        context = getBaseContext()
        article = Articles().getDraftContent(article_id)
        context['article'] = article
        return render(request, 'generaltech/article.html', context)


class AuthorPageView(View):
    def get(self, request, author_id):
        context = getBaseContext()
        author_details, articles = Articles().getAuthorArticlesAndDetails(author_id)
        context['author'] = author_details
        context['posts'] = articles
        return render(request, 'generaltech/author.html', context)


class AuthorFeedView(View):
    def get(self, request, author_id, page_num):
        context = getBaseContext()
        articles, has_more = Articles().getAuthorFeedArticles(author_id, page_num)
        context['posts'] = articles
        rendered_posts = render_to_string('generaltech/normal_articles.html', context)
        json_response = {
            'hasMore': has_more,
            'posts': rendered_posts,
        }
        return JsonResponse(json_response)


class TagPageView(View):
    def get(self, request, tag_id):
        context = getBaseContext()
        tag_details, articles = Articles().getTagArticlesAndDetails(tag_id)
        context['tag'] = tag_details
        context['posts'] = articles
        return render(request, 'generaltech/tag.html', context)


class TagFeedView(View):
    def get(self, request, tag_id, page_num):
        context = getBaseContext()
        articles, has_more = Articles().getTagFeedArticles(tag_id, page_num)
        context['posts'] = articles
        rendered_posts = render_to_string('generaltech/normal_articles.html', context)
        json_response = {
            'hasMore': has_more,
            'posts': rendered_posts,
        }
        return JsonResponse(json_response)


def getBaseContext():
    return {
        'date': datetime.datetime.now().strftime("%A, %d %b %Y"),
        'facebook_link': f'https://www.facebook.com/{settings.FACEBOOK_ACC}',
        'twitter_link': f'https://twitter.com/{settings.TWITTER_ACC}',
    }
