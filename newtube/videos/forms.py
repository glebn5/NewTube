# forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя из аргументов
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Введите ваш комментарий'
        
        
        # Если пользователь не авторизован, делаем поле недоступным для ввода
        if not user.is_authenticated:
            self.fields['text'].widget.attrs['disabled'] = 'disabled'
            self.fields['text'].widget.attrs['placeholder'] = 'Вы должны войти, чтобы оставить комментарий'  

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')
    name_channel = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'name_channel', 'email', 'password1', 'password2')