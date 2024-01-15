from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.db.models import Count, Q, F
from django.conf import settings

from .models import ProjectsMeta, ProjectAuthor, Project

POST_PER_PAGE = settings.POST_PER_PAGE

def get_category_count():
    return Project.objects.filter(Q(status__icontains='p')).values('categories__title').annotate(Count('categories__title'))


def get_tags():
    return Project.objects.filter(Q(status__icontains='p')).values('tags__title').distinct()
    

def get_searched_category_or_tag(category, request):
    queryset = Project.objects.all()
    if 'category' in str(request):
        queryset = queryset.filter(Q(categories__title__icontains=category)).distinct()
    else:
        queryset = queryset.filter(Q(tags__title__icontains=category)).distinct()

    if queryset.exists():
        return queryset
    return None


def projects(request):
    seo_metatags = ProjectsMeta.objects.filter(applicable=True).distinct()
    most_recent = Project.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[:3]
    category_count = get_category_count()
    tags = get_tags()
    queryset = Project.objects.all()
    project_list = queryset.filter(Q(status__icontains='p')).distinct().order_by('-timestamp')
    paginator = Paginator(project_list, POST_PER_PAGE)
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
    return render(request, 'projects/projects.html', context)


def project(request, slug):
    most_recent = Project.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[:3]
    category_count = get_category_count()
    tags = get_tags()
    project = get_object_or_404(Project, slug=slug)

    Project.objects.filter(slug=project.slug).update(view_count=F('view_count') + 1)
    project.view_count += 1

    context = {
        'project': project,
        'most_recent': most_recent,
        'category_count': category_count,
        'tags': tags,
    }
    return render(request, 'projects/project.html', context)


def projects_category_or_tag_redir(request):
    return redirect(reverse("project-list"))


# When you click on tag or category in PROJECTS this method will call.
def search_results_projects_category_or_tag(request, slug):
    category_count = get_category_count()
    tags = get_tags()
    most_recent = Project.objects.filter(Q(status__icontains='p')).order_by('-timestamp')[:3]
    project_list = get_searched_category_or_tag(slug, request)
    paginator = Paginator(project_list, POST_PER_PAGE)
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
    return render(request, 'projects/projects.html', context)


class SearchProjectListView(ListView):
    model = Project
    paginate_by = POST_PER_PAGE
    template_name = 'projects/projects.html'
    context_object_name = 'queryset'

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        context = super(SearchProjectListView, self).get_context_data(**kwargs)
        context.update({
            'searchq': q,
            'most_recent': super(SearchProjectListView, self).get_queryset().filter(Q(status__icontains='p')).order_by('timestamp')[:3],
            'category_count': get_category_count(),
            'tags': get_tags()
        })
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = super(SearchProjectListView, self).get_queryset().filter(Q(status__icontains='p')).order_by('timestamp')
        queryset = queryset.filter( Q(title__icontains=q) | Q(overview__icontains=q) ).distinct()
        return queryset