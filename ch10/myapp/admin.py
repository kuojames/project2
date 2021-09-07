from django.contrib import admin
from myapp import models

# Register your models here.

class Poll_admin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'enabled')
    ordering = ('-created_at', )

class Poll_item_admin(admin.ModelAdmin):
    list_display = ('poll', 'name')
    ordering = ('poll', )

admin.site.register(models.Profile)
admin.site.register(models.Poll, Poll_admin)
admin.site.register(models.Poll_item, Poll_item_admin)

