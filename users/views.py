from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import User


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée"""
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Rediriger selon le rôle de l'utilisateur
        if self.request.user.role == 'seller':
            return reverse_lazy('seller_dashboard')
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, f'Bienvenue {form.get_user().first_name or form.get_user().username} !')
        return super().form_valid(form)


class CustomRegisterView(CreateView):
    """Vue d'inscription personnalisée"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.'
        )
        return response


def custom_logout_view(request):
    """Vue de déconnexion personnalisée"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('home')


@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'users/profile.html', context)
