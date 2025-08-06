
from articles.models import Article
from articles.forms import ArticleSearchForm
from orders.models import Order
from notifications.models import Notification
from users.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django import forms

def home(request):
    """Page d'accueil avec recherche et filtres"""
    form = ArticleSearchForm(request.GET or None)
    articles = Article.objects.all()

    # Appliquer les filtres si le formulaire est valide
    if form.is_valid():
        # Recherche textuelle
        search = form.cleaned_data.get('search')
        if search:
            articles = articles.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        # Filtre par vendeur
        seller = form.cleaned_data.get('seller')
        if seller:
            articles = articles.filter(seller=seller)

        # Filtre par gamme de prix prédéfinie
        price_range = form.cleaned_data.get('price_range')
        if price_range:
            if price_range == '0-50':
                articles = articles.filter(price__lt=50)
            elif price_range == '50-100':
                articles = articles.filter(price__gte=50, price__lt=100)
            elif price_range == '100-250':
                articles = articles.filter(price__gte=100, price__lt=250)
            elif price_range == '250-500':
                articles = articles.filter(price__gte=250, price__lt=500)
            elif price_range == '500-1000':
                articles = articles.filter(price__gte=500, price__lt=1000)
            elif price_range == '1000+':
                articles = articles.filter(price__gte=1000)

        # Filtre par prix personnalisé
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if min_price:
            articles = articles.filter(price__gte=min_price)
        if max_price:
            articles = articles.filter(price__lte=max_price)

        # Tri
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            articles = articles.order_by(sort_by)
        else:
            articles = articles.order_by('-created_at')
    else:
        # Par défaut, trier par date de création décroissante
        articles = articles.order_by('-created_at')

    # Pagination
    paginator = Paginator(articles, 12)  # 12 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistiques pour l'affichage
    total_articles = articles.count()

    context = {
        'form': form,
        'page_obj': page_obj,
        'articles': page_obj,  # Pour compatibilité avec le template existant
        'total_articles': total_articles,
        'page_title': 'Bienvenue sur Articlo',
        'has_filters': any([
            form.cleaned_data.get('search') if form.is_valid() else False,
            form.cleaned_data.get('seller') if form.is_valid() else False,
            form.cleaned_data.get('price_range') if form.is_valid() else False,
            form.cleaned_data.get('min_price') if form.is_valid() else False,
            form.cleaned_data.get('max_price') if form.is_valid() else False,
        ]) if form.is_valid() else False
    }
    return render(request, 'dashboard/home.html', context)

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

@login_required
def order_detail(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id, seller=user)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'dashboard/order_detail.html', {'order': order, 'form': form})
@login_required
def delete_article(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id, seller=user)
    if request.method == 'POST':
        article.delete()
        return redirect('seller_dashboard')
    return render(request, 'dashboard/confirm_delete_article.html', {'article': article})

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'price', 'images']

@login_required
def edit_article(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id, seller=user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'dashboard/edit_article.html', {'form': form, 'article': article})

@login_required
def seller_dashboard(request):
    user = request.user
    if user.role != 'seller':
        return render(request, 'dashboard/not_authorized.html')
    articles = Article.objects.filter(seller=user)
    orders = Order.objects.filter(seller=user)
    notifications = Notification.objects.filter(recipient=user).order_by('-created_at')[:10]
    stats = {
        'articles_count': articles.count(),
        'orders_count': orders.count(),
        'orders_pending': orders.filter(status='pending').count(),
        'orders_confirmed': orders.filter(status='confirmed').count(),
    }
    context = {
        'articles': articles,
        'orders': orders,
        'notifications': notifications,
        'stats': stats,
    }
    return render(request, 'dashboard/seller_dashboard.html', context)


# ============================================================================
# VUES ADMIN
# ============================================================================

def admin_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'admin':
            messages.error(request, 'Accès refusé. Vous devez être administrateur.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Dashboard principal pour les administrateurs"""
    # Statistiques générales
    total_users = User.objects.count()
    total_sellers = User.objects.filter(role='seller').count()
    total_clients = User.objects.filter(role='client').count()
    total_articles = Article.objects.count()
    total_orders = Order.objects.count()

    # Statistiques des 30 derniers jours
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users_30d = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    new_articles_30d = Article.objects.filter(created_at__gte=thirty_days_ago).count()
    new_orders_30d = Order.objects.filter(created_at__gte=thirty_days_ago).count()

    # Statistiques des commandes par statut
    orders_pending = Order.objects.filter(status='pending').count()
    orders_confirmed = Order.objects.filter(status='confirmed').count()
    orders_cancelled = Order.objects.filter(status='cancelled').count()

    # Top vendeurs (par nombre d'articles)
    top_sellers = User.objects.filter(role='seller').annotate(
        articles_count=Count('articles')
    ).order_by('-articles_count')[:5]

    # Articles récents
    recent_articles = Article.objects.select_related('seller').order_by('-created_at')[:5]

    # Commandes récentes
    recent_orders = Order.objects.select_related('article', 'seller').order_by('-created_at')[:5]

    # Notifications non lues
    unread_notifications = Notification.objects.filter(is_read=False).count()

    context = {
        'stats': {
            'total_users': total_users,
            'total_sellers': total_sellers,
            'total_clients': total_clients,
            'total_articles': total_articles,
            'total_orders': total_orders,
            'new_users_30d': new_users_30d,
            'new_articles_30d': new_articles_30d,
            'new_orders_30d': new_orders_30d,
            'orders_pending': orders_pending,
            'orders_confirmed': orders_confirmed,
            'orders_cancelled': orders_cancelled,
            'unread_notifications': unread_notifications,
        },
        'top_sellers': top_sellers,
        'recent_articles': recent_articles,
        'recent_orders': recent_orders,
        'page_title': 'Dashboard Administrateur'
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@admin_required
def admin_users(request):
    """Gestion des utilisateurs"""
    # Filtres
    role_filter = request.GET.get('role', '')
    search = request.GET.get('search', '')

    users = User.objects.all()

    if role_filter:
        users = users.filter(role=role_filter)

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    users = users.order_by('-date_joined')

    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'users': page_obj,
        'role_filter': role_filter,
        'search': search,
        'page_title': 'Gestion des utilisateurs'
    }

    return render(request, 'dashboard/admin_users.html', context)


@admin_required
def admin_user_toggle_status(request, user_id):
    """Activer/désactiver un utilisateur"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()

        status = "activé" if user.is_active else "désactivé"
        messages.success(request, f'L\'utilisateur {user.username} a été {status}.')

    return redirect('admin_users')


@admin_required
def admin_user_change_role(request, user_id):
    """Changer le rôle d'un utilisateur"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['admin', 'seller', 'client']:
            old_role = user.get_role_display()
            user.role = new_role
            user.save()

            new_role_display = user.get_role_display()
            messages.success(
                request,
                f'Le rôle de {user.username} a été changé de {old_role} à {new_role_display}.'
            )
        else:
            messages.error(request, 'Rôle invalide.')

    return redirect('admin_users')


@admin_required
def admin_articles(request):
    """Gestion des articles"""
    # Filtres
    seller_filter = request.GET.get('seller', '')
    search = request.GET.get('search', '')

    articles = Article.objects.select_related('seller').all()

    if seller_filter:
        articles = articles.filter(seller_id=seller_filter)

    if search:
        articles = articles.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    articles = articles.order_by('-created_at')

    # Pagination
    paginator = Paginator(articles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Liste des vendeurs pour le filtre
    sellers = User.objects.filter(role='seller').order_by('username')

    context = {
        'page_obj': page_obj,
        'articles': page_obj,
        'sellers': sellers,
        'seller_filter': seller_filter,
        'search': search,
        'page_title': 'Gestion des articles'
    }

    return render(request, 'dashboard/admin_articles.html', context)


@admin_required
def admin_article_delete(request, article_id):
    """Supprimer un article (admin)"""
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f'L\'article "{title}" a été supprimé.')
        return redirect('admin_articles')

    context = {
        'article': article,
        'page_title': f'Supprimer l\'article "{article.title}"'
    }

    return render(request, 'dashboard/admin_article_delete.html', context)


@admin_required
def admin_orders(request):
    """Gestion des commandes"""
    # Filtres
    status_filter = request.GET.get('status', '')
    seller_filter = request.GET.get('seller', '')
    search = request.GET.get('search', '')

    orders = Order.objects.select_related('article', 'seller').all()

    if status_filter:
        orders = orders.filter(status=status_filter)

    if seller_filter:
        orders = orders.filter(seller_id=seller_filter)

    if search:
        orders = orders.filter(
            Q(client_name__icontains=search) |
            Q(client_phone__icontains=search) |
            Q(client_email__icontains=search) |
            Q(article__title__icontains=search)
        )

    orders = orders.order_by('-created_at')

    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Listes pour les filtres
    sellers = User.objects.filter(role='seller').order_by('username')
    status_choices = Order.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'orders': page_obj,
        'sellers': sellers,
        'status_choices': status_choices,
        'status_filter': status_filter,
        'seller_filter': seller_filter,
        'search': search,
        'page_title': 'Gestion des commandes'
    }

    return render(request, 'dashboard/admin_orders.html', context)


@admin_required
def admin_notifications(request):
    """Gestion des notifications"""
    notifications = Notification.objects.select_related('recipient').order_by('-created_at')

    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'notifications': page_obj,
        'page_title': 'Gestion des notifications'
    }

    return render(request, 'dashboard/admin_notifications.html', context)


@admin_required
def admin_notification_mark_read(request, notification_id):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(Notification, id=notification_id)

    if request.method == 'POST':
        notification.is_read = True
        notification.save()
        messages.success(request, 'Notification marquée comme lue.')

    return redirect('admin_notifications')


@admin_required
def admin_stats(request):
    """Statistiques détaillées"""
    # Statistiques par période
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    stats = {
        'users': {
            'total': User.objects.count(),
            'week': User.objects.filter(date_joined__date__gte=week_ago).count(),
            'month': User.objects.filter(date_joined__date__gte=month_ago).count(),
            'by_role': {
                'admin': User.objects.filter(role='admin').count(),
                'seller': User.objects.filter(role='seller').count(),
                'client': User.objects.filter(role='client').count(),
            }
        },
        'articles': {
            'total': Article.objects.count(),
            'week': Article.objects.filter(created_at__date__gte=week_ago).count(),
            'month': Article.objects.filter(created_at__date__gte=month_ago).count(),
        },
        'orders': {
            'total': Order.objects.count(),
            'week': Order.objects.filter(created_at__date__gte=week_ago).count(),
            'month': Order.objects.filter(created_at__date__gte=month_ago).count(),
            'by_status': {
                'pending': Order.objects.filter(status='pending').count(),
                'confirmed': Order.objects.filter(status='confirmed').count(),
                'cancelled': Order.objects.filter(status='cancelled').count(),
            }
        }
    }

    # Top vendeurs
    top_sellers = User.objects.filter(role='seller').annotate(
        articles_count=Count('articles'),
        orders_count=Count('received_orders')
    ).order_by('-articles_count', '-orders_count')[:10]

    context = {
        'stats': stats,
        'top_sellers': top_sellers,
        'page_title': 'Statistiques détaillées'
    }

    return render(request, 'dashboard/admin_stats.html', context)
