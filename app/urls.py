"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('listmember/', views.listmember, name='listmember'),
    path('addmember/', views.addmember, name='addmember'),
    path('addconfirm/', views.addconfirm, name='addconfirm'),
    path('addapproval/<int:num>', views.addapproval, name='addapproval'),
    path('editmember/<int:num>', views.editmember, name='editmember'),
    path('editconfirm/', views.editconfirm, name='editconfirm'),
    path('delmember/<int:num>', views.delmember, name='delmember'),
    path('addfromcsv/', views.addfromcsv, name='addfromcsv'),
    path('login/', views.login, name='login'),
]
