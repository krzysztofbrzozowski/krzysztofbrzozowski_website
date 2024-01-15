from django.contrib import admin
from django.contrib.sites.models import Site

from .models import IndexMeta, AboutMeta, GalleryImage

admin.site.register(GalleryImage)

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')
    
admin.site.register(Site, SiteAdmin)
admin.site.register(IndexMeta)
admin.site.register(AboutMeta)
