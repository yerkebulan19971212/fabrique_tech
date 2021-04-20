"""fabraca_tech URL Configuration

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
import debug_toolbar
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework_swagger.views import get_swagger_view

from polls.views import (PassPollView, PollModelViewSet, QuestionModelViewSet,
                         UserPassedPollView)

schema_view = get_swagger_view(title='Pastebin API')

router = DefaultRouter()
router.register(r'polls', PollModelViewSet)
router.register(r'questions', QuestionModelViewSet)


urlpatterns = [
    path('api/v1/login/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('api/v1/', include((router.urls, 'api_v1'), namespace='api_v1')),
    path('api/v1/pass-poll/', PassPollView.as_view(), name='pass_pool'),
    path(
        'api/v1/user-passed-poll/<int:user_id>/', UserPassedPollView.as_view(),
        name='user_pass_pool'
    ),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    url(r'^$', schema_view)

]
