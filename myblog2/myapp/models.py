from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model): # 貼文
    
    objects = models.Manager()
    published = PublishedManager() # 管理器

    state_choices = {
        ('draft', 'Draft'), 
        ('published', 'Published'),
    }
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=state_choices, default='draft')

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title    

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Comment(models.Model): # 留言
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # related_name 解說 : https://blog.csdn.net/hpu_yly_bj/article/details/78939748
    # Post.comment_set.all() 可以查到post對應的comment，而Post.comments.all()也有同樣效果
    name = models.CharField(max_length=80, default='None')
    email = models.EmailField(null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {self.name} on {self.post}'    



