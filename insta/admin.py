from django.contrib import admin
from .models import

class ArticleAdmin(admin.ModelAdmin):

admin.site.register(Article, ArticleAdmin)
admin.site.register(tags)
