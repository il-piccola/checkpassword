from django.db import models
from django.utils import timezone
import os
import datetime
from .settings import MEDIA_ROOT

class Member(models.Model) :
    name = models.CharField(max_length=200, default='')
    kana = models.CharField(max_length=200, default='')
    tel1 = models.CharField(max_length=11, default='')
    mail = models.EmailField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    organization = models.CharField(max_length=200, default='')
    position = models.CharField(max_length=200, default='')
    tel2 = models.CharField(max_length=11, default='')
    prefectures = models.CharField(max_length=8, default='')
    scale = models.CharField(max_length=50, default='')
    others = models.TextField(max_length=10000, default='')
    time = models.DateTimeField(default=timezone.now)
    approval = models.BooleanField(default=False)

def getuploadpath(instance, filename) :
    newname = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_') + filename
    return os.path.join('csv', newname)

class Csv(models.Model) :
    csv = models.FileField(upload_to=getuploadpath)
    time = models.DateTimeField(default=timezone.now)

    def getpath(self) :
        return os.path.join(MEDIA_ROOT, self.csv.path)
