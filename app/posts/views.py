from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.db.models import Count, Q, F
from django.conf import settings

from .models import PostsMeta, Post, Author

POST_PER_PAGE = settings.POST_PER_PAGE

def get_author(user):
    queryset = Author.objects.filter(user=user)
    if queryset.exists():
        return queryset[0]
    return None


def get_category_count():
    return Post.objects.filter(Q(status__icontains='p')).values('categories__title').annotate(Count('categories__title'))


def get_tags():
    return Post.objects.filter(Q(status__icontains='p')).values('tags__title').distinct()


def get_searched_category_or_tag(category, request):
    queryset = Post.objects.all()
    if 'category' in str(request):
        queryset = queryset.filter(Q(categories__title__icontains=category)).distinct()
    else:
        queryset = queryset.filter(Q(tags__title__icontains=category)).distinct()

    if queryset.exists():
        return queryset
    return None


def posts(request):
    seo_metatags = PostsMeta.objects.filter(applicable=True).distinct()
    most_recent = Post.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[:3]
    category_count = get_category_count()
    tags = get_tags()
    queryset = Post.objects.all()
    post_list = queryset.filter(Q(status__icontains='p')).distinct().order_by('-timestamp')
    paginator = Paginator(post_list, POST_PER_PAGE)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'seo_metatags': seo_metatags,
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'category_count': category_count,
        'tags': tags,
        'page_request_var': page_request_var
    }
    return render(request, 'posts/posts.html', context)


def post(request, slug):
    most_recent = Post.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[:3]
    tags = get_tags()
    category_count = get_category_count()
    post = get_object_or_404(Post, slug=slug)
    
    Post.objects.filter(slug=post.slug).update(view_count=F('view_count') + 1)
    post.view_count += 1

    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'tags': tags,
    }
    return render(request, 'posts/post.html', context)


def posts_category_or_tag_redir(request):
    return redirect(reverse("post-list"))


class SearchPostListView(ListView):
    model = Post
    paginate_by = POST_PER_PAGE
    template_name = 'posts/posts.html'
    context_object_name = 'queryset'

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        context = super(SearchPostListView, self).get_context_data(**kwargs)
        context.update({
            'searchq': q,
            'most_recent': super(SearchPostListView, self).get_queryset().filter(Q(status__icontains='p')).order_by('timestamp')[:3],
            'category_count': get_category_count(),
            'tags': get_tags()
        })
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = super(SearchPostListView, self).get_queryset().filter(Q(status__icontains='p')).order_by('timestamp')
        queryset = queryset.filter( Q(title__icontains=q) | Q(overview__icontains=q) ).distinct()
        return queryset


# When you click on tag or category in POSTS this method will call.
def search_results_posts_category_or_tag(request, slug):
    category_count = get_category_count()
    tags = get_tags()
    most_recent = Post.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[:3]
    post_list = get_searched_category_or_tag(slug, request)
    paginator = Paginator(post_list, POST_PER_PAGE)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'category_count': category_count,
        'tags': tags,
        'page_request_var': page_request_var
    }
    return render(request, 'posts/posts.html', context)