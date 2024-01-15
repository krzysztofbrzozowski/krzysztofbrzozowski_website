import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.db import models


class IndexMeta(models.Model):
    meta_image = models.ImageField()
    meta_title = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=160)
    meta_keywords = models.TextField()
    meta_robots = models.CharField(max_length=60, default='all,follow')

    og_meta_title = models.CharField(max_length=100)
    og_meta_type = models.CharField(max_length=100, default='website')
    og_meta_image = models.ImageField(null=True, blank=True)
    # og_meta_site_name = models.CharField(max_length=100, default=settings.DEFAULT_PAGE_NAME)
    og_meta_site_name = models.CharField(max_length=100)
    og_meta_description = models.TextField(max_length=200)

    applicable = models.BooleanField()

    def __str__(self):
        return self.meta_title

    def save(self):
        if not self.og_meta_image:
            self.og_meta_image = self.meta_image
            
        super(IndexMeta, self).save()


class AboutMeta(models.Model):
    meta_image = models.ImageField()
    meta_title = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=160)
    meta_keywords = models.TextField()
    meta_robots = models.CharField(max_length=60, default='all,follow')

    og_meta_title = models.CharField(max_length=100)
    og_meta_type = models.CharField(max_length=100, default='website')
    og_meta_image = models.ImageField(null=True, blank=True)
    # og_meta_site_name = models.CharField(max_length=100, default=settings.DEFAULT_PAGE_NAME)
    og_meta_site_name = models.CharField(max_length=100)
    og_meta_description = models.TextField(max_length=200)

    applicable = models.BooleanField()

    def __str__(self):
        return self.meta_title

    def save(self):
        if not self.og_meta_image:
            self.og_meta_image = self.meta_image
            
        super(AboutMeta, self).save()


class GalleryImage(models.Model):
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField()
    thumbnail_min = models.ImageField(null=True, blank=True)
    featured = models.BooleanField()

    def __str__(self):
        return self.title

    def save(self):
        if not self.thumbnail_min:
            im = Image.open(self.thumbnail)
            output = BytesIO()
            im.thumbnail((512, 512), Image.ANTIALIAS)
            im.save(output, format='JPEG', quality=90)
            output.seek(0)
            self.thumbnail_min = InMemoryUploadedFile(
                output,'ImageField',
                f"{self.thumbnail.name.split('.')[0]}_min.jpg",
                'image/jpeg', sys.getsizeof(output), None
            )
            
        super(GalleryImage, self).save()