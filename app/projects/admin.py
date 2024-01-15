from django.contrib import admin

from .models import ProjectsMeta, Category, ProjectAuthor, Project, Tag

def make_draft(modeladmin, request, queryset):
    queryset.update(status='d')
make_draft.short_description = "Mark selected stories as DRAFT"

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as PUBLISHED"

def make_withdrawn(modeladmin, request, queryset):
    queryset.update(status='w')
make_withdrawn.short_description = "Mark selected stories as WITHDRAWN"


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [make_draft, make_published, make_withdrawn]


admin.site.register(Category)
admin.site.register(ProjectAuthor)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
admin.site.register(ProjectsMeta)