from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.db.models import Count, Q, F
from django.shortcuts import render, redirect
from django.conf import settings

from operator import attrgetter
from itertools import chain

from projects.models import ProjectAuthor, Project
from posts.models import Author, Post
from .models import IndexMeta, AboutMeta, GalleryImage


from django.core import serializers


POST_PER_PAGE = settings.POST_PER_PAGE


def get_category_count():
    # This (annotate) returns dictionary
    # 'categories__title' after double underscore it will get this title value from model
    return Post.objects.values('categories__title').annotate(Count('categories__title'))


def get_tags():
    return Post.objects.values('tags__title').distinct()


def index(request):
    seo_metatags = IndexMeta.objects.filter(applicable=True).distinct()

    # project_list = Project.objects.filter(Q(featured=True), Q(status__icontains='p')).distinct()
    # post_list = Post.objects.filter(Q(featured=True), Q(status__icontains='p')).distinct()
    # featured = sorted(chain(post_list, project_list), key=attrgetter('timestamp'), reverse=True)

    latest_posts = Post.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[0:3]
    latest_projects = Project.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[0:3]
    featured = sorted(chain(latest_posts, latest_projects), key=attrgetter('timestamp'), reverse=True)

    latest = Post.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[0:3]
    featured_images = GalleryImage.objects.filter(featured=True)

    context = {
        'seo_metatags': seo_metatags,
        'object_list': featured,
        'latest': latest,
        'featured_images': featured_images,
    }
    return render(request, 'core/index.html', context)


def about(request):
    seo_metatags = AboutMeta.objects.filter(applicable=True).distinct()
    context = {
        'seo_metatags': seo_metatags
    }
    return render(request, 'core/about.html', context)


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def redirect_github(request):
    response = redirect('https://github.com/krzysztofbrzozowski')
    return response


class SearchListView(ListView):
    model = Project
    paginate_by = POST_PER_PAGE
    template_name = 'core/search_results.html'
    context_object_name = 'queryset'

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        context = super(SearchListView, self).get_context_data(**kwargs)
        context.update({
            'searchq': q,
            'category_count': get_category_count(),
            'tags': get_tags()
        })
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        # query = Q(title__icontains=q) | Q(overview__icontains=q) | Q(status__icontains='p')
        query = Q(title__icontains=q) | Q(overview__icontains=q)

        project_list = Project.objects.filter(query, Q(status__icontains='p')).distinct()
        post_list = Post.objects.filter(query, Q(status__icontains='p')).distinct()
        queryset = sorted(chain(post_list, project_list), key=attrgetter('timestamp'))
        return queryset


def error_400(request, exception):
    return render(request, 'error_handlers/error_400.html', {})


def error_403(request, exception):
    return render(request, 'error_handlers/error_403.html', {})


def error_404(request, exception):
    return render(request, 'error_handlers/error_404.html', {})


def error_500(request):
    return render(request, 'error_handlers/error_500.html', {})