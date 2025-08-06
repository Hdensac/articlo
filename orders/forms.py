from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Formulaire de commande pour les clients"""
    
    class Meta:
        model = Order
        fields = ['client_name', 'client_phone', 'client_email', 'message']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
                'required': True
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+33123456789',
                'required': True
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message optionnel (questions, précisions, etc.)',
                'rows': 4
            })
        }
        labels = {
            'client_name': 'Votre nom complet',
            'client_phone': 'Numéro de téléphone',
            'client_email': 'Adresse email',
            'message': 'Message (optionnel)'
        }
        help_texts = {
            'client_name': 'Nom et prénom pour la commande',
            'client_phone': 'Numéro pour vous contacter (WhatsApp de préférence)',
            'client_email': 'Email pour recevoir la confirmation (optionnel)',
            'message': 'Ajoutez des questions ou précisions sur votre commande'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre certains champs obligatoires
        self.fields['client_name'].required = True
        self.fields['client_phone'].required = True
        self.fields['client_email'].required = False
        self.fields['message'].required = False

    def clean_client_name(self):
        """Validation du nom client"""
        name = self.cleaned_data.get('client_name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères")
        return name.strip() if name else name

    def clean_client_phone(self):
        """Validation du numéro de téléphone"""
        phone = self.cleaned_data.get('client_phone')
        if phone:
            # Supprimer les espaces et caractères spéciaux
            phone = ''.join(filter(str.isdigit, phone.replace('+', '+')))
            
            # Vérifier la longueur
            if len(phone.replace('+', '')) < 8:
                raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres")
            
            # Ajouter le + si pas présent et commence par un code pays
            if not phone.startswith('+') and len(phone) > 9:
                phone = '+' + phone
                
        return phone

    def clean_client_email(self):
        """Validation de l'email (optionnel)"""
        email = self.cleaned_data.get('client_email')
        if email:
            email = email.strip().lower()
            # Validation basique supplémentaire si nécessaire
            if '@' not in email or '.' not in email.split('@')[1]:
                raise forms.ValidationError("Veuillez entrer une adresse email valide")
        return email


class OrderStatusForm(forms.ModelForm):
    """Formulaire pour que les vendeurs modifient le statut des commandes"""
    
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'status': 'Statut de la commande'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les choix de statut avec des couleurs
        self.fields['status'].widget.attrs.update({
            'class': 'form-control status-select'
        })
