# RSS/ATom Feed 介紹 https://www.playpcesor.com/2007/09/rssatom-feed.html
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from myapp import models

class LatestPostsFeed(Feed):
    title = 'My Post'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog'

    def items(self):
        return models.Post.published.all()[:5]

    def  item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
