from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('create/', views.create_article, name='create'),
    path('<int:article_id>/', views.article_detail, name='detail'),
    path('<int:article_id>/edit/', views.edit_article, name='edit'),
    path('<int:article_id>/delete/', views.delete_article, name='delete'),
]
