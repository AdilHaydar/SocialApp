"""SocialApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from Post import views
from django.conf.urls.static import static
from django.conf import settings
from search import views as search_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('post/',include(('Post.urls','Post'),namespace='post')),
    path('user/',include(('user.urls','user'),namespace='user')),
    path('search/',search_views.search, name='search'),
    path('<str:username>/',search_views.view_profile,name='view_profile'),
    path('<str:username>/replies/',user_views.view_replies,name="view_replies"),
    path('<str:username>/likes/',user_views.view_likes,name='view_likes'),
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
