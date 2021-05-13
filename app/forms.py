from django import forms
from django.forms import ModelForm
from .models import *

class MemberForm(forms.ModelForm) :
    name = forms.CharField(label="氏名", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="氏名(カナ)", widget=forms.TextInput(attrs={'class':'form-control'}))
    mail = forms.CharField(label="メールアドレス", widget=forms.EmailInput(attrs={'class':'form-control'}))
    tel1 = forms.CharField(label="電話番号", max_length=11, widget=forms.NumberInput(attrs={'class':'form-control'}))
    tel2 = forms.CharField(label="電話番号(個人)", max_length=11, required=False, widget=forms.NumberInput(attrs={'class':'form-control'}))
    organization = forms.CharField(label="勤務先", widget=forms.TextInput(attrs={'class':'form-control'}))
    position = forms.CharField(label="役職", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="パスワード", min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Member
        fields = ['name', 'kana', 'mail', 'tel1', 'tel2', 'organization', 'position', 'password', ]

class LoginForm(forms.ModelForm) :
    mail = forms.CharField(label="メールアドレス", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta :
        model = Member
        fields = ['mail', 'password', ]

class UploadForm(forms.ModelForm) :
    class Meta :
        model = Csv
        fields = ['csv', ]

class SearchForm(forms.Form) :
    search = forms.CharField(label="検索", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    order = forms.ChoiceField(label="ソート"
        , choices=(('date', '日時'), ('kana', '氏名(カナ)'), ('mail', 'メールアドレス'), ('approval', '承認'))
        , widget=forms.Select(attrs={'class':'form-control'}))
    reverse = forms.ChoiceField(label="", choices=(('on', '降順'), ('off', '昇順'))
        , widget=forms.Select(attrs={'class':'form-control'}))
