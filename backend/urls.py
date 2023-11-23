"""
URL configuration for backend project.

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from main_app import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'registration', views.UserRegistrationView)
router.register(r'create_bookclub', views.BookClubViewSet)
router.register(r'bookclubs', views.BookClubViewSet, basename='bookclubs')
router.register(r'bookclubs/<int:pk>', views.BookClubViewSet)
router.register(r'bookclubs/<int:pk>/update_bookclub', views.BookClubViewSet)
router.register(r'bookclubs/<int:pk>/join', views.BookClubViewSet)
router.register(r'bookclubs/<int:pk>/leave', views.BookClubViewSet)
router.register(r'bookclubs/<int:pk>/delete_bookclub', views.BookClubViewSet)
router.register(r'bookclubs/<int:pk>/comments', views.BookClubViewSet)
router.register(r'bookclubs/<int:pk>/add_comment', views.BookClubViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

