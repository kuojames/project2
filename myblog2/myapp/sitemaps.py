from django.contrib.sitemaps import Sitemap
from myapp import models

# 網站地圖記錄網站的資料分布在哪個url上，並記錄一些附加訊息。

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return models.Post.published.all()
    def lastmod(self, obj):
        return obj.updated    