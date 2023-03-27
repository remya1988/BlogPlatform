"""BlogProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from blogapi.views import (UserModelViewsetView,BlogModelView,CommentModelView,AdminCommentView,
                           AdminBlogRetrieveDeleteView,AdminBlogListView,AdminUserCreateView,LogoutView)
router =  DefaultRouter()
router.register("blog/user/account",UserModelViewsetView,basename="signup")
router.register("blog/CRUD",BlogModelView,basename="blog")
router.register("blog/comment",CommentModelView,basename="comment")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/user/login',TokenObtainPairView.as_view()),
    path('blog/user/token/refresh',TokenRefreshView.as_view()),
    path('blog/user/logout',LogoutView.as_view()),

    # Admin APIS
    path("blog/admin/comment/list/<int:id>",AdminCommentView.as_view()),
    path("blog/admin/blog/retrieve-delete/<int:id>",AdminBlogRetrieveDeleteView.as_view()),
    path("blog/admin/list-allblogs",AdminBlogListView.as_view()),
    path("blog/admin/super-user",AdminUserCreateView.as_view()),
]+router.urls