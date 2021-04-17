from django import forms
from django.forms import ModelForm
from .models import *

class MemberForm(forms.ModelForm) :
    mail = forms.CharField(label="EMail", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Member
        fields = ['mail', 'password', ]

class UploadForm(forms.ModelForm) :
    class Meta :
        model = Csv
        fields = ['csv', ]

class SearchForm(forms.Form) :
    search = forms.CharField(label="検索", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    order = forms.ChoiceField(label="ソート", choices=(('date', 'Date'), ('mail', 'EMail')))
    reverse = forms.ChoiceField(label="", choices=(('on', '降順'), ('off', '昇順')))
