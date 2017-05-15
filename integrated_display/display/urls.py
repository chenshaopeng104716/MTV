from django.conf.urls import url,include
from django.contrib import admin
from display import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.platform, name='platform'),
    url(r'^$', views.login, name='login'),
    url(r'^channel/$',views.channel,name='channel'),
    url(r'^program/$',views.program,name='program'),
    url(r'^testindex/$',views.testindex,name='testindex'),
    url(r'^Fsearch/$', views.Fsearch, name='Fsearch'),
    url(r'^getprogramid/$', views.getprogramid, name='getprogramid'),
     url(r'^platform/$', views.platform, name='platform'),
      url(r'^logout/$', views.logout, name='logout'),
]