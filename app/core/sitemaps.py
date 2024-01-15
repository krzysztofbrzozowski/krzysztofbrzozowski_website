from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.db.models import Q

from projects.models import Project
from posts.models import Post 


class PostSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return Post.objects.filter(Q(status__icontains='p'))

    def lastmod(self, obj):
        return obj.timestamp

class ProjectSitemap(Sitemap):
    priority = 1

    def items(self):
        return Project.objects.filter(Q(status__icontains='p'))

    def lastmod(self, obj):
        return obj.timestamp

class StaticViewSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return ['about', 'privacy-policy']

    def location(self, item):
        return reverse(item)

