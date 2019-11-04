"""generaltech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from . import views
from .views import IndexPageView, IndexFeedView, ArticlePageView, RelatedArticleView, DraftPageView, AuthorPageView, AuthorFeedView, TagPageView, TagFeedView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', IndexPageView.as_view(), name='index_page'),
    path('feed/page/<int:page_num>', IndexFeedView.as_view(), name='index_feed'),
    path('article/<slug:article_id>', ArticlePageView.as_view(), name='article_page'),
    path('article/<slug:article_id>/related', RelatedArticleView.as_view(), name='article_related_feed'),
    path('draft/<slug:article_id>', DraftPageView.as_view(), name='draft_page'),
    path('author/<slug:author_id>', AuthorPageView.as_view(), name='author_page'),
    path('author/<slug:author_id>/feed/page/<int:page_num>', AuthorFeedView.as_view(), name='author_feed'),
    path('tag/<slug:tag_id>', TagPageView.as_view(), name='tag_page'),
    path('tag/<slug:tag_id>/feed/page/<int:page_num>', TagFeedView.as_view(), name='tag_feed')
]
