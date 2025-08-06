from django import forms
from .models import Article
from users.models import User


class ArticleForm(forms.ModelForm):
    """Formulaire de création et modification d'articles"""
    
    class Meta:
        model = Article
        fields = ['title', 'description', 'price', 'images']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: iPhone 14 Pro Max 256GB',
                'maxlength': 255
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez votre article en détail (état, caractéristiques, etc.)',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'images': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Titre de l\'article',
            'description': 'Description détaillée',
            'price': 'Prix (€)',
            'images': 'Image de l\'article'
        }
        help_texts = {
            'title': 'Donnez un titre accrocheur à votre article',
            'description': 'Plus votre description est détaillée, plus vous avez de chances de vendre',
            'price': 'Prix en euros (ex: 299.99)',
            'images': 'Ajoutez une belle photo de votre article (JPG, PNG)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre tous les champs obligatoires sauf l'image
        for field_name, field in self.fields.items():
            if field_name != 'images':
                field.required = True
            
            # Ajouter des classes CSS supplémentaires
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' mb-2'

    def clean_price(self):
        """Validation personnalisée pour le prix"""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Le prix doit être supérieur à 0")
        if price is not None and price > 999999.99:
            raise forms.ValidationError("Le prix ne peut pas dépasser 999,999.99 €")
        return price

    def clean_title(self):
        """Validation personnalisée pour le titre"""
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 5:
            raise forms.ValidationError("Le titre doit contenir au moins 5 caractères")
        return title.strip() if title else title

    def clean_description(self):
        """Validation personnalisée pour la description"""
        description = self.cleaned_data.get('description')
        if description and len(description.strip()) < 20:
            raise forms.ValidationError("La description doit contenir au moins 20 caractères")
        return description.strip() if description else description


class ArticleSearchForm(forms.Form):
    """Formulaire de recherche et filtrage des articles"""

    # Choix pour le tri
    SORT_CHOICES = [
        ('', 'Tri par défaut'),
        ('-created_at', 'Plus récents'),
        ('created_at', 'Plus anciens'),
        ('price', 'Prix croissant'),
        ('-price', 'Prix décroissant'),
        ('title', 'Nom A-Z'),
        ('-title', 'Nom Z-A'),
    ]

    # Choix pour les gammes de prix
    PRICE_RANGES = [
        ('', 'Tous les prix'),
        ('0-50', 'Moins de 50€'),
        ('50-100', '50€ - 100€'),
        ('100-250', '100€ - 250€'),
        ('250-500', '250€ - 500€'),
        ('500-1000', '500€ - 1000€'),
        ('1000+', 'Plus de 1000€'),
    ]

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un article...',
            'autocomplete': 'off'
        }),
        label='Recherche'
    )

    seller = forms.ModelChoiceField(
        queryset=User.objects.filter(role='seller').order_by('username'),
        required=False,
        empty_label='Tous les vendeurs',
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Vendeur'
    )

    price_range = forms.ChoiceField(
        choices=PRICE_RANGES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Gamme de prix'
    )

    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix min',
            'step': '0.01'
        }),
        label='Prix minimum'
    )

    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix max',
            'step': '0.01'
        }),
        label='Prix maximum'
    )

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Trier par'
    )

    def clean(self):
        """Validation croisée des champs"""
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        # Vérifier que le prix min n'est pas supérieur au prix max
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError("Le prix minimum ne peut pas être supérieur au prix maximum")

        return cleaned_data
