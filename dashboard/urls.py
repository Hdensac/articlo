from django.urls import path
from .views import (
    home, seller_dashboard, edit_article, delete_article, order_detail,
    admin_dashboard, admin_users, admin_user_toggle_status, admin_user_change_role,
    admin_articles, admin_article_delete, admin_orders, admin_notifications,
    admin_notification_mark_read, admin_stats
)

urlpatterns = [
    # Pages publiques
    path('', home, name='home'),  # Page d'accueil

    # Dashboard vendeur
    path('dashboard/', seller_dashboard, name='seller_dashboard'),
    path('dashboard/article/<int:article_id>/edit/', edit_article, name='edit_article'),
    path('dashboard/article/<int:article_id>/delete/', delete_article, name='delete_article'),
    path('dashboard/order/<int:order_id>/', order_detail, name='order_detail'),

    # Dashboard admin
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', admin_users, name='admin_users'),
    path('admin-dashboard/users/<int:user_id>/toggle-status/', admin_user_toggle_status, name='admin_user_toggle_status'),
    path('admin-dashboard/users/<int:user_id>/change-role/', admin_user_change_role, name='admin_user_change_role'),
    path('admin-dashboard/articles/', admin_articles, name='admin_articles'),
    path('admin-dashboard/articles/<int:article_id>/delete/', admin_article_delete, name='admin_article_delete'),
    path('admin-dashboard/orders/', admin_orders, name='admin_orders'),
    path('admin-dashboard/notifications/', admin_notifications, name='admin_notifications'),
    path('admin-dashboard/notifications/<int:notification_id>/mark-read/', admin_notification_mark_read, name='admin_notification_mark_read'),
    path('admin-dashboard/stats/', admin_stats, name='admin_stats'),
]
