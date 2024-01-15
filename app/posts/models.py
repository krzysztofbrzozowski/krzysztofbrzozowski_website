from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.conf import settings
from django.urls import reverse
from django.db.models import F
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from datetime import datetime
from io import BytesIO
from PIL import Image
import sys


User = get_user_model()


class PostsMeta(models.Model):
    meta_image = models.ImageField()
    meta_title = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=160)
    meta_keywords = models.TextField()
    meta_robots = models.CharField(max_length=60, default='all,follow')

    og_meta_title = models.CharField(max_length=100)
    og_meta_type = models.CharField(max_length=100, default='website')
    og_meta_image = models.ImageField(null=True, blank=True)
    og_meta_site_name = models.CharField(max_length=100, default=settings.DEFAULT_PAGE_NAME)
    og_meta_description = models.TextField(max_length=200)

    applicable = models.BooleanField()

    def __str__(self):
        return self.meta_title

    def save(self):
        if not self.og_meta_image:
            self.og_meta_image = self.meta_image
            
        super(PostsMeta, self).save()


class Category(models.Model):
    title = models.CharField(max_length=30)
    
    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=150)
    
    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]

def get_current_date():   
    if getattr(settings, 'CKEDITOR_RESTRICT_BY_DATE', True):
        date_path = datetime.now().strftime('%Y/%m/%d')
        return date_path
    return ''

 
class Post(models.Model):
    meta_title = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=160)
    meta_keywords = models.TextField()
    meta_robots = models.CharField(max_length=60, default='all,follow')

    og_meta_title = models.CharField(max_length=100)
    og_meta_type = models.CharField(max_length=100, default='website')
    og_meta_site_name = models.CharField(max_length=100, default=settings.DEFAULT_PAGE_NAME)
    og_meta_description = models.TextField(max_length=200)

    slug = models.SlugField(null=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField()     # auto_now_add=True creates autotime stamp when model is created
    content = RichTextUploadingField(blank=True, null=True, config_name='default')
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to=get_current_date())
    thumbnail_min = models.ImageField(upload_to=get_current_date(), null=True, blank=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    featured = models.BooleanField()                    # if model is featured it will be displayed on main page
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={ 'slug': self.slug })

    def get_category_start_url(self):
        return reverse('category-post-list')

    def get_category_url(self):
        return reverse('category-post-list', kwargs={ 'slug': self.slug })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    def save(self):
        if not self.thumbnail_min:
            im = Image.open(self.thumbnail)
            output = BytesIO()
            im.thumbnail((256, 256), Image.Resampling.LANCZOS)
            im.save(output, format='JPEG', quality=95)
            output.seek(0)
            self.thumbnail_min = InMemoryUploadedFile(
                output,'ImageField',
                f"{self.thumbnail.name.split('.')[0]}_min.jpg",
                'image/jpeg', sys.getsizeof(output), None
            )
        
        super(Post, self).save()
