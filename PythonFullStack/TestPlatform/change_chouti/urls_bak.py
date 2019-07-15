"""chouti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web.views import home,account

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^index/$', home.index),
    # url(r'^fetch_comment/$', home.fetch_comment),
    # url(r'^comment/$', home.comment),
    # url(r'^favor/$', home.favor),
    # url(r'^upload_image/$', home.upload_image),
    url(r'^check_code/$', account.check_code),
    url(r'^send_msg/$', account.send_msg),
    url(r'^register/$', account.register),
    url(r'^login/$', account.login),
    url(r'^logout/$', account.logout),
    url(r'^comment/$',account.comment),
    url(r'^favor/$',account.favor),
    url(r'^upload_image/$',account.uploadImage),

    # url(r'^add_comment/$', home.add_comment),
    # url(r'^show/$', home.show),
    # url(r'^test_upload/$', home.test_upload),

    url(r'^performance/$',home.testPerformance),
    url(r'^index/([0-9]*)', home.testForum),
    url(r'^report/([0-9]*)', home.testReport),
    url(r'^modal_info/$', account.modal_info),
    url(r'^update_item/$', account.update_item),

    url(r'^creat_report/$', account.creat_report),
    url(r'^creat_excel/$', account.creat_excel),

    url(r'^word_download/$', account.word_download,name='word_download'),
    url(r'^excel_download/$', account.excel_download,name='excel_download'),
    url(r'^upload_customFile/$',account.custom_file_upload),
    # url(r'^excel_upload/$', account.excel_file_upload,name='excel_upload'),

    url(r'^per_data_store/$',account.per_data_store),
    url(r'^per_data_extract/$',account.per_data_extract),
    url(r'^per_data_clear/$',account.per_data_clear),
    url(r'^servers_info_extract/$',account.servers_info_extract),
]
