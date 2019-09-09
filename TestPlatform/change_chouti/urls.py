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
    #-----***----- 后台
    url(r'^admin/', admin.site.urls),

    #-----***----- 登录、注册、退出登录
    url(r'^check_code/$', account.check_code),
    url(r'^send_msg/$', account.send_msg),
    url(r'^register/$', account.register),
    url(r'^login/$', account.login),
    url(r'^logout/$', account.logout),

    #-----***----- 测试论坛
    url(r'^index/([0-9]*)', home.testForum),
    url(r'^comment/$', account.comment),
    url(r'^favor/$', account.favor),
    url(r'^upload_image/$', account.uploadImage),

    #-----***----- 性能测试
    url(r'^performance/$', home.testPerformance),
    url(r'^per_data_store/$', account.per_data_store),
    url(r'^per_data_extract/$', account.per_data_extract),
    url(r'^per_data_clear/$', account.per_data_clear),
    url(r'^servers_info_extract/$', account.servers_info_extract),

    # -----***----- 测试报告
    url(r'^report/([0-9]*)', home.testReport),
    url(r'^modal_info/$', account.modal_info),
    url(r'^update_item/$', account.update_item),
    url(r'^creat_report/$', account.creat_report),
    url(r'^creat_excel/$', account.creat_excel),
    url(r'^word_download/$', account.word_download, name='word_download'),
    url(r'^excel_download/$', account.excel_download, name='excel_download'),
    url(r'^upload_customFile/$', account.custom_file_upload),

    # -----***----- 自动化测试
    url(r'^auto/$',home.testauto),

]
