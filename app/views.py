from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from cryptography.fernet import Fernet
import os
import csv
import base64
from .settings import KEYSTR, REMAIN_CSV
from .models import *
from .forms import *

def login(request) :
    params = {
        'title' : 'Login',
        'msg' : '',
        'form' : MemberForm(),
    }
    if (request.method != 'POST') :
        return render(request, 'login.html', params)
    obj = Member()
    form = MemberForm(data=request.POST, instance=obj)
    if form.is_valid() :
        data = Member.objects.filter(mail=request.POST['mail'])
        if data.count() <= 0 :
            params['msg'] = '未登録のメールアドレスです'
        else :
            item = data.first()
            key = base64.urlsafe_b64encode(KEYSTR.encode())
            token = item.password.encode()
            password = str(Fernet(key).decrypt(token).decode())
            if password != request.POST['password'] :
                params['msg'] = 'パスワードが正しくありません'
            else :
                return redirect('http://www.yahoo.co.jp')
    else :
        params['msg'] = '入力に誤りがあります'
    params['form'] = form
    return render(request, 'login.html', params)

def listmember(request) :
    data = Member.objects.all().order_by('time').reverse()
    params = {
        'title' : 'User List',
        'data' : data,
        'form' : SearchForm(),
    }
    if (request.method != 'POST') :
        return render(request, 'listmember.html', params)
    if len(request.POST['search']) > 0 :
        data = Member.objects.filter(mail__icontains=request.POST['search']).reverse()
    if request.POST['order'] == 'mail' :
        data = data.order_by('mail')
    if request.POST['reverse'] == 'off' :
        data = data.reverse()
    form = SearchForm(data=request.POST)
    params['data'] = data
    params['form'] = form
    return render(request, 'listmember.html', params)

def addmember(request) :
    params = {
        'title' : 'New User',
        'msg' : '',
        'form' : MemberForm(),
    }
    if (request.method != 'POST') :
        return render(request, 'addmember.html', params)
    obj = Member()
    form = MemberForm(data=request.POST, instance=obj)
    if form.is_valid() :
        datalist = Member.objects.filter(mail=request.POST['mail'])
        if datalist.count() > 0 :
            params['msg'] = '登録済みのメールアドレスです'
        elif request.POST['password'] != request.POST['chkpass'] :
            params['msg'] = 'パスワードが一致しません'
        else :
            request.session['mail'] = request.POST['mail']
            request.session['password'] = request.POST['password']
            return redirect(to='addconfirm')
    else :
        params['msg'] = '入力に誤りがあります'
    params['form'] = form
    return render(request, 'addmember.html', params)

def addconfirm(request) :
    mail = request.session['mail']
    password = request.session['password']
    if (request.method == 'POST') :
        member = Member(mail=mail, password=encodepassword(password))
        member.save()
        request.session.clear()
        return redirect(to='listmember')
    data = Member(mail=mail, password=password)
    params = {
        'title' : 'Regist User',
        'msg' : '以下のユーザを登録します',
        'data' : data,
    }
    return render(request, 'addconfirm.html', params)

def editmember(request, num) :
    obj = Member.objects.get(id=num)
    form = MemberForm(instance=obj)
    form.fields['mail'].widget.attrs['readonly'] = 'readonly'
    params = {
        'title' : 'Update User',
        'msg' : 'ユーザのパスワードを変更します',
        'form' : form,
        'id' : obj.id,
    }
    if (request.method != 'POST') :
        return render(request, 'editmember.html', params)
    if request.POST['password'] != request.POST['chkpass'] :
        params['msg'] = 'パスワードが一致しません'
    else :
        password = encodepassword(request.POST['password'])
        member = Member(id=obj.id, mail=obj.mail, password=password)
        member.save()
        return redirect(to='listmember')
    return render(request, 'editmember.html', params)

def delmember(request, num) :
    obj = Member.objects.get(id=num)
    if (request.method == 'POST') :
        obj.delete()
        return redirect(to='listmember')
    params = {
        'title' : 'Delete User',
        'msg' : '以下のユーザを削除します',
        'data' : obj,
    }
    return render(request, 'delmember.html', params)

def addfromcsv(request) :
    params = {
        'title' : 'Upload CSV',
        'msg' : 'CSVファイルからユーザを追加します',
        'form' : UploadForm(),
    }
    if (request.method == 'POST') :
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid() :
            if csvregist(form) :
                return redirect(to='listmember')
            else :
                params['msg'] = 'CSVファイルが読み込めません'
    return render(request, 'addfromcsv.html', params)

def encodepassword(password) :
    key = base64.urlsafe_b64encode(KEYSTR.encode())
    token = Fernet(key).encrypt(password.encode())
    return str(token.decode())

def csvregist(form) :
    form.save()
    path = form.instance.getpath()
    if not os.path.exists(path) :
        return False
    with open(path, 'r') as f :
        reader = csv.reader(f)
        for line in reader :
            if len(line) != 2 :
                continue
            datalist = Member.objects.filter(mail=line[0])
            if datalist.count() > 0 :
                for data in datalist :
                    data.delete()
            member = Member(mail=line[0], password=encodepassword(line[1]))
            member.save()
    datalist = Csv.objects.all()
    num = len(datalist)
    for i in range(num-REMAIN_CSV) :
        datalist[i].delete()
    return True
