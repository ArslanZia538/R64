"""R64Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from R64app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    #path('dashboard/hisab_kitab', views.hisab_kitab, name="hisab_kitab"),
    path('dashboard/single_entry', views.single_entry, name="single_entry"),
    path('dashboard/dashboardR', views.dashboardR, name="dashboardR"),
    path('dashboard/selectUser', views.selectUser, name="selectUser"),
    path('dashboard/changepassword', views.changepassword, name="changepassword"),
    path('dashboard/history', views.history, name="history"),
    path('dashboard/history/dashboardR', views.dashboardR, name="dashboardR"),
    path('dashboard/changepassword/dashboardR', views.dashboardR, name="dashboardR"),
    path('dashboard/selectbulkUser', views.selectbulkUser, name="selectbulkUser"),
    path('dashboard/selectbulkUser/bulkentry', views.bulkentry, name="bulkentry"),
    path('dashboard/selectbulkUser/dashboardR', views.dashboardR, name="dashboardR"),
    path('dashboard/selectUser/hisab_kitab', views.hisab_kitab, name="hisab_kitab"),
    path('dashboard/selectUser/dashboardR', views.dashboardR, name="dashboardR"),
    path('dashboard/selectUser/hisab_kitab/markpaid/<int:key_id>', views.markpaid, name='markpaid'),
    path('dashboard/selectUser/hisab_kitab/mark_all_paid/<str:user2>', views.mark_all_paid, name='mark_all_paid'),
    path('dashboard/logout/', views.logout, name="logout"),

]
