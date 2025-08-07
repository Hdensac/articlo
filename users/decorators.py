from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def seller_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est un vendeur"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'seller':
            messages.error(request, 'Accès refusé. Cette page est réservée aux vendeurs.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est admin"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, 'Accès refusé. Cette page est réservée aux administrateurs.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def client_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est un client (peut passer des commandes)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'seller':
            messages.error(
                request, 
                'Les vendeurs ne peuvent pas passer de commandes. '
                'Vous pouvez gérer vos articles et commandes depuis votre tableau de bord vendeur.'
            )
            return redirect('seller_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def not_seller_required(view_func):
    """Décorateur pour empêcher les vendeurs d'accéder à certaines vues"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'seller':
            return redirect('orders:seller_restriction')
        return view_func(request, *args, **kwargs)
    return wrapper
