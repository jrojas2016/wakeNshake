"""wakeNshake URL Configuration

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
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from MusicAlarm import views as MusicAlarmViews
from oauth import views as OauthViews
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin URL
    url(r'^admin/', admin.site.urls),

    # OAuth URLs
    #url(r'^', include('django.contrib.auth.urls')),
    url(r'^oauth2callback/calendar', OauthViews.oauth2callback_calendar, name = 'oauth2callback_calendar'),
    url(r'^oauth2callback/spotify', OauthViews.oauth2callback_spotify, name = 'oauth2callback_spotify'),

    # MusicAlarm URLs
    url(r'^$', MusicAlarmViews.homeview, name = 'homeview'),

    # Login URLs
    url(r'^login/spotify', MusicAlarmViews.spotify_login, name='spotify_login'),
    url(r'^login/calendar', MusicAlarmViews.calendar_login, name='calendar_login'),

    # Dashboard URLs
    url(r'^dashboard', MusicAlarmViews.dashboard, name='dashboard'),
    
    #built in login_tool
    # url(r'^user_login', auth_views.login, {'template_name': 'user_login.html'}, name='user_login'),
    # url(r'^adduser', OauthViews.adduser, name='adduser')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

