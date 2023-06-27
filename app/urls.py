"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from app import settings

admin.site.site_header = 'HayotYuliEducation - Администрация'
admin.site.site_title = 'HayotYuliEducation - Администрация'
admin.site.index_title = 'HayotYuliEducation - Администрация'

urlpatterns = [
                  path('', RedirectView.as_view(url="/tasks-manager/home")),
                  path('admin/', admin.site.urls),
                  path('tasks-manager/', include("tasksManager.urls")),
                  path('authentication/', include("authentication.urls")),
                  re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  re_path(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
