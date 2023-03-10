"""EPMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
import master_app.views as av

urlpatterns = [
    path('', av.index),
    path('LoginOrg', av.org_login),
    path('LoginUser', av.user_login),
    path('org_index', av.org_index),
    path('user_index', av.user_index),
    path('SignUpOrg', av.org_register),
    path('logout', av.logout),
    path('org_change_password', av.org_change_password),
    path('user_change_password', av.user_change_password),
    path('create-emp',av.add_emp),
    path('read-emp',av.read_emp),
    path('view-emp/<int:eid>', av.view_emp),
    path('update-emp/<int:eid>', av.update_emp),
    path('del-emp/<int:eid>', av.del_emp),
    #path('admin/', admin.site.urls)
]

