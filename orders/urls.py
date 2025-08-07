from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('article/<int:article_id>/order/', views.order_article, name='order_article'),
    path('success/<int:order_id>/', views.order_success, name='success'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('seller-restriction/', views.seller_restriction_view, name='seller_restriction'),
]
