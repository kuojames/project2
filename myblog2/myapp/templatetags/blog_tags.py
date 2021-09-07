from django import template
from myapp import models
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

# 自定模板標籤
@register.simple_tag
def total_posts(): # 回傳有published的post數量
    return models.Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = models.Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return models.Post.published.annotate(total_comment=Count('comments')).order_by('-total_comment')[:count] 
    # comments指的是models.Comment的外鍵
    # models.Post.published.annotate(total_comment=Count('comments')) total_comment紀錄Post裡有多少comment

# 自訂模板過濾器
@register.filter(name='markdown') # filter叫markdown，指向markdown_format這個方法
def markdown_format(text):
    return mark_safe(markdown.markdown(text)) # 第一個markdown是套件，第二個是這個套件的方法
    # text+' Hello world'