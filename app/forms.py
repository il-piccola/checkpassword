from django import forms
from django.forms import ModelForm
from .models import *

class MemberForm(forms.ModelForm) :
    PREFECTURES = (
        ("北海道","北海道"),
        ("青森県","青森県"),
        ("岩手県","岩手県"),
        ("宮城県","宮城県"),
        ("秋田県","秋田県"),
        ("山形県","山形県"),
        ("福島県","福島県"),
        ("茨城県","茨城県"),
        ("栃木県","栃木県"),
        ("群馬県","群馬県"),
        ("埼玉県","埼玉県"),
        ("千葉県","千葉県"),
        ("東京都","東京都"),
        ("神奈川県","神奈川県"),
        ("新潟県","新潟県"),
        ("富山県","富山県"),
        ("石川県","石川県"),
        ("福井県","福井県"),
        ("山梨県","山梨県"),
        ("長野県","長野県"),
        ("岐阜県","岐阜県"),
        ("静岡県","静岡県"),
        ("愛知県","愛知県"),
        ("三重県","三重県"),
        ("滋賀県","滋賀県"),
        ("京都府","京都府"),
        ("大阪府","大阪府"),
        ("兵庫県","兵庫県"),
        ("奈良県","奈良県"),
        ("和歌山県","和歌山県"),
        ("鳥取県","鳥取県"),
        ("島根県","島根県"),
        ("岡山県","岡山県"),
        ("広島県","広島県"),
        ("山口県","山口県"),
        ("徳島県","徳島県"),
        ("香川県","香川県"),
        ("愛媛県","愛媛県"),
        ("高知県","高知県"),
        ("福岡県","福岡県"),
        ("佐賀県","佐賀県"),
        ("長崎県","長崎県"),
        ("熊本県","熊本県"),
        ("大分県","大分県"),
        ("宮崎県","宮崎県"),
        ("鹿児島県","鹿児島県"),
        ("沖縄県","沖縄県"),
        ("海外","海外"),
    )
    SCALE = (
        ("医師一人の診療所", "医師一人の診療所"),
        ("医師数人の診療所", "医師数人の診療所"),
        ("数十床クラスの病院", "数十床クラスの病院"),
        ("それ以上の大規模病院", "それ以上の大規模病院"),
    )
    name = forms.CharField(label="氏名", widget=forms.TextInput(attrs={'class':'form-control'}))
    kana = forms.CharField(label="氏名(カナ)", widget=forms.TextInput(attrs={'class':'form-control'}))
    tel1 = forms.CharField(label="個人電話番号", max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    mail = forms.CharField(label="メールアドレス", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="パスワード", min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    organization = forms.CharField(label="勤務先", widget=forms.TextInput(attrs={'class':'form-control'}))
    position = forms.CharField(label="資格、役職", widget=forms.TextInput(attrs={'class':'form-control'}))
    tel2 = forms.CharField(label="勤務先電話番号", max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}))
    prefectures = forms.ChoiceField(label="都道府県", widget=forms.Select(attrs={'class':'form-control'}), choices=PREFECTURES)
    scale = forms.ChoiceField(label="規模", widget=forms.Select(attrs={'class':'form-control'}), choices=SCALE)
    others = forms.CharField(label="その他", widget=forms.Textarea(attrs={'class':'form-control', 'cols':'80', 'rows':'10'}))
    class Meta :
        model = Member
        fields = ['name', 'kana', 'tel1', 'mail', 'password', 'organization', 'position', 'tel2', 'prefectures', 'scale', 'others', ]

class ScheduleForm(forms.Form) :
    date1 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel1 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    date2 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel2 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    date3 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place3 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel3 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time3 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position3 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    date4 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place4 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel4 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time4 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position4 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    date5 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place5 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel5 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time5 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position5 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    date6 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place6 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel6 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time6 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position6 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    date7 = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}), input_formats=['%m月%d日(%a)'], required=False)
    place7 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    tel7 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'pattern':'^[0-9]+$'}), required=False)
    time7 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    position7 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

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
