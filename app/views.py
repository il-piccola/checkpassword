from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.core.mail import send_mail
from cryptography.fernet import Fernet
import os
import csv
import base64
import datetime
from .settings import KEYSTR, REMAIN_CSV, MAILADDRESS, MAILSUBJECT, EMAIL_HOST_USER
from .models import *
from .forms import *

def login(request) :
    params = {
        'title' : 'Login',
        'msg' : '',
        'form' : LoginForm(),
    }
    if 'msg' in request.session :
        params['msg'] = request.session['msg']
        request.session.clear()
    if (request.method != 'POST') :
        return render(request, 'login.html', params)
    obj = Member()
    form = LoginForm(data=request.POST, instance=obj)
    if form.is_valid() :
        data = Member.objects.filter(mail=request.POST['mail'])
        if data.count() <= 0 :
            params['msg'] = '未登録のメールアドレスです'
        else :
            item = data.first()
            if item.approval == False :
                params['msg'] = 'こちらからの電話確認後にユーザ認証されるまでお待ちください'
            else :
                if decodepassword(item.password) != request.POST['password'] :
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
        data = Member.objects.filter(
            Q(kana__icontains=request.POST['search']) | Q(mail__icontains=request.POST['search'])
        )
    if request.POST['order'] == 'kana' :
        data = data.order_by('kana')
    elif request.POST['order'] == 'mail' :
        data = data.order_by('mail')
    elif request.POST['order'] == 'approval' :
        data = data.order_by('approval')
    if request.POST['reverse'] == 'off' :
        data = data.reverse()
    form = SearchForm(data=request.POST)
    params['data'] = data
    params['form'] = form
    return render(request, 'listmember.html', params)

def addmember(request) :
    params = {
        'title' : 'Registration',
        'msg' : '',
        'form' : MemberForm(),
    }
    if (request.method != 'POST') :
        params['msg'] = 'ユーザ登録申し込み後にこちらから確認の電話をさせていただきます'
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
            request.session['name'] = request.POST['name']
            request.session['kana'] = request.POST['kana']
            request.session['tel1'] = request.POST['tel1']
            request.session['mail'] = request.POST['mail']
            request.session['password'] = request.POST['password']
            request.session['organization'] = request.POST['organization']
            request.session['position'] = request.POST['position']
            request.session['tel2'] = request.POST['tel2']
            request.session['prefectures'] = request.POST['prefectures']
            request.session['scale'] = request.POST['scale']
            request.session['others'] = request.POST['others']
            return redirect(to='addschedule')
    elif len(request.POST['password']) < 6 :
        params['msg'] = 'パスワードは6文字以上にしてください'
    else :
        params['msg'] = '入力に誤りがあります'
    params['form'] = form
    return render(request, 'addmember.html', params)

def addschedule(request) :
    params = {
        'title' : 'Schedule',
        'msg' : '',
        'form' : ScheduleForm(),
    }
    if (request.method != 'POST') :
        params['msg'] = '明後日より一週間の予定を記入してください(日曜日　祝日は不要です)'
        return render(request, 'addschedule.html', params)
    date = ["--", "--", "--", "--", "--", "--", "--"]
    place = ["--", "--", "--", "--", "--", "--", "--"]
    tel = ["--", "--", "--", "--", "--", "--", "--"]
    time = ["--", "--", "--", "--", "--", "--", "--"]
    position = ["--", "--", "--", "--", "--", "--", "--"]
    for i in range(7) :
        if request.POST['date'+str(i+1)] != "" :
            pday = datetime.datetime.strptime(request.POST['date'+str(i+1)], "%Y-%m-%d")
            # date[i] = convertweekday(datetime.datetime.strftime(pday, "%m月%d日(%a)"))
            date[i] = datetime.datetime.strftime(pday, "%m/%d(%a)")
            # date[i] = request.POST['date'+str(i+1)]
        if request.POST['place'+str(i+1)] != "" :
            place[i] = request.POST['place'+str(i+1)]
        if request.POST['tel'+str(i+1)] != "" :
            tel[i] = request.POST['tel'+str(i+1)]
        if request.POST['time'+str(i+1)] != "" :
            time[i] = request.POST['time'+str(i+1)]
        if request.POST['position'+str(i+1)] != "" :
            position[i] = request.POST['position'+str(i+1)]
    request.session['date'] = date
    request.session['place'] = place
    request.session['tel'] = tel
    request.session['time'] = time
    request.session['post'] = position
    return redirect(to='addconfirm')

def addconfirm(request) :
    name = request.session['name']
    kana = request.session['kana']
    tel1 = request.session['tel1']
    mail = request.session['mail']
    password = request.session['password']
    organization = request.session['organization']
    position = request.session['position']
    tel2 = request.session['tel2']
    prefectures = request.session['prefectures']
    scale = request.session['scale']
    others = request.session['others']
    date = request.session['date']
    place = request.session['place']
    tel = request.session['tel']
    time = request.session['time']
    post = request.session['post']
    if (request.method == 'POST') :
        member = Member(name=name, kana=kana, tel1=tel1, mail=mail, password=encodepassword(password)
            , organization=organization, position=position, tel2=tel2, prefectures=prefectures
            , scale=scale, others=others)
        sendapplicationmail(member, date, place, tel, time, post)
        member.save()
        request.session.clear()
        request.session['msg'] = 'ユーザ登録の申し込みを受け付けました。こちらからの電話確認をお待ちください。'
        return redirect(to='login')
    data = Member(name=name, kana=kana, tel1=tel1, mail=mail, password=password
        , organization=organization, position=position, tel2=tel2, prefectures=prefectures
        , scale=scale, others=others)
    params = {
        'title' : 'Confirmation',
        'msg' : '以下の通りユーザ登録を申し込みます',
        'data' : data,
        'date' : date,
        'place' : place,
        'tel' : tel,
        'time' : time,
        'post' : post,
    }
    return render(request, 'addconfirm.html', params)

def addapproval(request, num) :
    member = Member.objects.get(id=num)
    if (request.method == 'POST') :
        member.time = datetime.datetime.now()
        member.approval = True
        member.save()
        return redirect(to='listmember')
    params = {
        'title' : 'Approval',
        'msg' : '以下のユーザ登録を承認します',
        'data' : member,
        'password' : decodepassword(member.password),
    }
    return render(request, 'addapproval.html', params)

def editmember(request, num) :
    obj = Member.objects.get(id=num)
    if (request.method != 'POST') :
        form = MemberForm(instance=obj)
        form.fields['mail'].widget.attrs['readonly'] = 'readonly'
        params = {
            'title' : 'Update',
            'msg' : 'ユーザ情報を変更します',
            'form' : form,
            'id' : obj.id,
            'password' : decodepassword(obj.password),
        }
        return render(request, 'editmember.html', params)
    request.session['id'] = num
    request.session['name'] = request.POST['name']
    request.session['kana'] = request.POST['kana']
    request.session['tel1'] = request.POST['tel1']
    request.session['organization'] = request.POST['organization']
    request.session['position'] = request.POST['position']
    request.session['tel2'] = request.POST['tel2']
    request.session['prefectures'] = request.POST['prefectures']
    request.session['scale'] = request.POST['scale']
    request.session['others'] = request.POST['others']
    return redirect(to='editconfirm')

def editconfirm(request) :
    obj = Member.objects.get(id=request.session['id'])
    name = request.session['name']
    kana = request.session['kana']
    tel1 = request.session['tel1']
    organization = request.session['organization']
    position = request.session['position']
    tel2 = request.session['tel2']
    prefectures = request.session['prefectures']
    scale = request.session['scale']
    others = request.session['others']
    member = Member(id=obj.id, name=name, kana=kana, tel1=tel1, mail=obj.mail, password=obj.password
        , organization=organization, position=position, tel2=tel2, prefectures=prefectures
        , scale=scale, others=others, approval=obj.approval)
    if (request.method == 'POST') :
        member.save()
        request.session.clear()
        return redirect(to='listmember')
    params = {
        'title' : 'Confirmation',
        'msg' : '以下の通りユーザ情報を更新します',
        'data' : member,
        'password' : decodepassword(obj.password),
    }
    return render(request, 'editconfirm.html', params)

def delmember(request, num) :
    obj = Member.objects.get(id=num)
    if (request.method == 'POST') :
        obj.delete()
        return redirect(to='listmember')
    params = {
        'title' : 'Delete',
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

def decodepassword(passtoken) :
    key = base64.urlsafe_b64encode(KEYSTR.encode())
    token = passtoken.encode()
    return str(Fernet(key).decrypt(token).decode())

def convertweekday(txt) :
    txt = txt.replace("Mon", "月")
    txt = txt.replace("Tue", "火")
    txt = txt.replace("Wed", "水")
    txt = txt.replace("Thu", "木")
    txt = txt.replace("Fri", "金")
    txt = txt.replace("Sat", "土")
    txt = txt.replace("Sun", "日")
    return txt

def sendapplicationmail(member, date, place, tel, time, post) :
    txt = "【個人情報】\r\n"
    txt += "氏名：" + member.name + "\r\n"
    txt += "氏名(カナ)：" + member.kana + "\r\n"
    txt += "個人電話番号：" + member.tel1 + "\r\n"
    txt += "メールアドレス：" + member.mail + "\r\n"
    txt += "パスワード：" + decodepassword(member.password) + "\r\n\r\n"
    txt += "【勤務先情報】\r\n"
    txt += "勤務先：" + member.organization + "\r\n"
    txt += "資格、役職：" + member.position + "\r\n"
    txt += "勤務先電話番号：" + member.tel2 + "\r\n"
    txt += "都道府県：" + member.prefectures + "\r\n"
    txt += "規模：" + member.scale + "\r\n"
    txt += "その他：\r\n" + member.others + "\r\n\r\n"
    txt += "【明後日より一週間の予定】\r\n"
    txt += "月日,場所,電話番号,電話が許される時間,電話を取った方に伝える貴方の立場\r\n"
    for i in range(7) :
        txt += date[i] + "," + place[i] + "," + tel[i] + "," + time[i] + "," + post[i] + "\r\n"
    send_mail(MAILSUBJECT, txt, EMAIL_HOST_USER, [MAILADDRESS])

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
