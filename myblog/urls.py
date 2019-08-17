from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import handler404,url
from blog import views         #+ 
from django.views.static import serve
#导入静态文件模块
from django.conf import settings
#导入配置文件里的文件上传配置

urlpatterns = [
    path('admin/', admin.site.urls),#管理后台
    path('', views.index, name='index'),#网站首页
    path('list-<int:lid>.html', views.list, name='list'),#列表页
    path('show-<int:sid>.html', views.show, name='show'),#内容页
    path('tag/<tag>', views.tag, name='tags'),#标签列表页
    path('s/', views.search, name='search'),#搜索列表页
    path('about/', views.about, name='about'),#联系我们单页
    path('application/', views.application, name='application'),#python应用
    path('ueditor/', include('DjangoUeditor.urls')),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('^add_comment/$', views.add_comment, name='add_comment'),
    re_path('^baidu_hot_data/$', views.baidu_hot_data, name='baidu_hot_data'),
    re_path('^robot_chat/$', views.robot_chat, name='robot_chat'),
    re_path('^get_contents/$', views.scapy_contents, name='scapy_contents'),
]
# handler404 = views.page_not_found