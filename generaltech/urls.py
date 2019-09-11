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

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('feed/page/<int:page_num>', views.index_pages, name='index_pages'),
    path('article/<slug:article_id>', views.article, name='article'),
    path('author/<slug:author_id>', views.author, name='author'),
    path('author/<slug:author_id>/feed/page/<int:page_num>', views.author_pages, name='author_pages'),
    path('tag/<slug:tag_id>', views.tag, name='tag'),
    path('tag/<slug:tag_id>/feed/page/<int:page_num>', views.tag_pages, name='tag_pages'),
    path('newsletter/', views.newsletter, name='newsletter'),
]
