"""mentor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from profiles import views
from profiles import urls as profiles_urls
from django.contrib.auth.views import login
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^$', views.HomeIndexView.as_view(), name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login, {'template_name': 'profiles/login.html',
                             'redirect_field_name': 'index',
                             }, name="login"),
    url(r'^logout/$', views.UserLogoutView.as_view(), name="logout"),
    url(r'^profiles/', include(profiles_urls)),
    url(r'^signup/$', views.UserSignUpView.as_view(), name="signup"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

