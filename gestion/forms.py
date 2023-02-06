# users/forms.py
from django import forms
from django.core.validators import RegexValidator
from gestion.models import ProducStoct, Product, Unite, Direction, Services, FriendWork

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
    

class ProductForm(forms.ModelForm):
    code = forms.CharField(
         label='Code',min_length=1, max_length=10,
          validators=[RegexValidator(r'^A[A-Z0-9]*$',
          message="Lettre majuscule et chiffre autorisé 12 caracteres")],
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'code'})
      )
    name = forms.CharField(
        label='nom produit', min_length=2, max_length=100,
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nom produit'})
      )
    
    class Meta:
        model = Product
        fields = '__all__'
        
        
    
class StockForm(forms.ModelForm):
    class Meta:
        model = ProducStoct
        fields = '__all__'
        
        
        