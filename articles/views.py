from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Article
from .forms import ArticleForm


@login_required
def create_article(request):
    """Vue pour créer un nouvel article"""
    # Vérifier que l'utilisateur est un vendeur
    if request.user.role != 'seller':
        messages.error(request, 'Seuls les vendeurs peuvent créer des articles.')
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.seller = request.user  # Associer l'article au vendeur connecté
            article.save()
            messages.success(
                request,
                f'Votre article "{article.title}" a été publié avec succès !'
            )
            return redirect('seller_dashboard')
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'page_title': 'Publier un nouvel article'
    }
    return render(request, 'articles/create_article.html', context)


@login_required
def edit_article(request, article_id):
    """Vue pour modifier un article existant"""
    article = get_object_or_404(Article, id=article_id)

    # Vérifier que l'utilisateur est le propriétaire de l'article
    if article.seller != request.user:
        raise Http404("Article non trouvé")

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Votre article "{article.title}" a été mis à jour avec succès !'
            )
            return redirect('seller_dashboard')
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
        'page_title': f'Modifier "{article.title}"'
    }
    return render(request, 'articles/edit_article.html', context)


@login_required
def delete_article(request, article_id):
    """Vue pour supprimer un article"""
    article = get_object_or_404(Article, id=article_id)

    # Vérifier que l'utilisateur est le propriétaire de l'article
    if article.seller != request.user:
        raise Http404("Article non trouvé")

    if request.method == 'POST':
        article_title = article.title
        article.delete()
        messages.success(
            request,
            f'L\'article "{article_title}" a été supprimé avec succès.'
        )
        return redirect('seller_dashboard')

    context = {
        'article': article,
        'page_title': f'Supprimer "{article.title}"'
    }
    return render(request, 'articles/delete_article.html', context)


def article_detail(request, article_id):
    """Vue pour afficher le détail d'un article"""
    article = get_object_or_404(Article, id=article_id)

    context = {
        'article': article,
        'page_title': article.title
    }
    return render(request, 'articles/article_detail.html', context)
