from logging import PlaceHolder
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.core.exceptions import ValidationError

from users.models.user_model import ProfileUser


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,  widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite seu nome aqui'
            }
        ))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite seu sobrenome aqui'
            }
        ))
    username = forms.CharField(max_length=120, required=True, widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite seu usuário aqui'
            }
        ))
    email = forms.EmailField(max_length=120, required=True, widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite seu email aqui'
            }
        ))
    password1 = forms.CharField(max_length=120, required=True, widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite sua senha aqui'
            }
        ))
    password2 = forms.CharField(max_length=120, required=True, widget=forms.TextInput(
            attrs={
                'class':'finput-group input-group-outline mb-3','placeholder': 'Confirme sua senha'
            }
        ))
    
        
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
        

    def clean_email(self):
        email  = self.cleaned_data['email']
        if User.objects.filter(email=email ).exists():
            raise ValidationError("O email {} já está em uso" .format(email))
        return email 

    def clean(self):
        super(SignUpForm, self).clean()
        if ('first_name' in self.cleaned_data 
                        and 'last_name' in self.cleaned_data 
                        and 'password1' in self.cleaned_data 
                        and 'password2' in self.cleaned_data):
            first_name = self.cleaned_data ['first_name']
            last_name = self.cleaned_data ['last_name']
            password1 = self.cleaned_data ['password1']
            password2 = self.cleaned_data ['password2']
            
            if not first_name:
                raise forms.ValidationError( "Primeiro nome necessário !!")
            elif len(first_name) < 4:
                raise forms.ValidationError('O nome deve ter 4 caracteres ou mais')
            elif not last_name:
                raise forms.ValidationError('Sobrenome obrigatório')
            elif len(last_name) < 4:
                raise forms.ValidationError('O sobrenome deve ter 4 caracteres ou mais')
            elif not password1:
                raise forms.ValidationError('Sua senha é obrigatória')
            elif len(password1) < 6:
                raise forms.ValidationError('A senha não pode conter menos que 6 digitos')
            elif password1 != password2:
                raise forms.ValidationError('As senhas digitadãos são diferentes')


class ProfileUserForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DatePickerInput(format="%d/%m/%Y"), label="Nascimento: 30/12/2000")
    class Meta:
        model = ProfileUser
        fields = [
            'idade',
            'cidade',
            'endereco',
            'numero_casa',
            'contato',
            'data_nascimento',
            'imagem_perfil',
        ]