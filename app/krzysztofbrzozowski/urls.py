"""
URL configuration for krzysztofbrzozowski project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import os

from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from core.views import (
    about,
    error_400,
    error_403,
    error_404,
    error_500,
    index, 
    privacy_policy,
    redirect_github,
    SearchListView,
)

from core.sitemaps import (
    PostSitemap,
    ProjectSitemap,
    StaticViewSitemap
)

from posts.views import (
    post,
    posts,
    posts_category_or_tag_redir,
    search_results_posts_category_or_tag, 
    SearchPostListView
)

from projects.views import (
    project,
    projects,
    projects_category_or_tag_redir,
    search_results_projects_category_or_tag, 
    SearchProjectListView
)

sitemaps = {
    'posts': PostSitemap,
    'projects': ProjectSitemap,
    'static': StaticViewSitemap
}

with open(os.environ.get('ADMIN_PATH_FILE')) as f:
    ADMIN_PATH = f.read().strip()

urlpatterns = [
    path('', index, name='main'),
    path(':', index, name='main'),
    path('posts/category/', posts_category_or_tag_redir, name='category-post-list'),   #this is only redirect
    path('posts/category/<slug>', search_results_posts_category_or_tag, name='category-post-search-list'),
    path('projects/category/', projects_category_or_tag_redir, name='category-project-list'),   #this is only redirect
    path('projects/category/<slug>', search_results_projects_category_or_tag, name='category-project-search-list'),
    path('github/', redirect_github, name='redirect-github'),
    path('about/', about, name='about'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('posts/', posts, name='post-list'),
    path('post/<slug>/', post, name='post-detail'),
    path('projects/', projects, name='project-list'),
    path('project/<slug>/', project, name='project-detail'),
    path('search/', SearchListView.as_view(), name='search'),
    path('search-posts/', SearchPostListView.as_view(), name='search-posts'),
    path('search-projects/', SearchProjectListView.as_view(), name='search-projects'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('posts/tag/', posts_category_or_tag_redir, name='tag-post-list'),  #this is only redirect
    path('posts/tag/<slug>', search_results_posts_category_or_tag, name='tag-post-search-list'),
    path('projects/tag/', projects_category_or_tag_redir, name='tag-project-list'),   #this is only redirect
    path('projects/tag/<slug>', search_results_projects_category_or_tag, name='tag-project-search-list'),

    path('robots.txt', TemplateView.as_view(template_name="base/robots.txt", content_type="text/plain"), name="robots-file"),
    
    path(f'{ADMIN_PATH}/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler500 = error_500

# TODO set as no debug since NGINX not configured yet
# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print(f'Output from urls ->  {urlpatterns:}')

