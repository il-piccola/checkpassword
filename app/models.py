from django.db import models
from django.utils import timezone
import os
import datetime
from .settings import MEDIA_ROOT

class Member(models.Model) :
    mail = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)

def getuploadpath(instance, filename) :
    newname = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_') + filename
    return os.path.join('csv', newname)

class Csv(models.Model) :
    csv = models.FileField(upload_to=getuploadpath)
    time = models.DateTimeField(default=timezone.now)

    def getpath(self) :
        return os.path.join(MEDIA_ROOT, self.csv.path)
