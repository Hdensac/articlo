from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'seller', 'created_at')
    list_filter = ('seller', 'created_at')
    search_fields = ('title', 'description')
