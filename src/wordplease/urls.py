"""wordplease URL Configuration

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
from rest_framework.compat import include
from rest_framework.routers import DefaultRouter

from blogs.api_rest.api import BlogsAPI, PostViewSet
from blogs.views import posts_list, blogs_list, user_posts_list, user_post_detail, NewPostView
from login.api_rest.api import UserViewSet
from login.views import LoginView, logout, SignupView

router = DefaultRouter()
router.register("users", UserViewSet, base_name="users_api")
router.register("posts", PostViewSet, base_name="posts_api")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # blogs
    url(r'^$', posts_list, name='posts_list'),
    url(r'^blogs/$', blogs_list, name='blogs_list'),
    url(r'^blogs/(?P<username>[0-9a-zA-Z]+)/$', user_posts_list, name="user_posts_list"),
    url(r'^blogs/(?P<username>[0-9a-zA-Z]+)/(?P<post_pk>[0-9]+)$', user_post_detail, name="user_post_detail"),
    url(r'^new-post$', NewPostView.as_view(), name="new_post"),
    # login
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^signup$', SignupView.as_view(), name='signup'),

    # api de usuarios y posts
    url(r'^api/1.0/', include(router.urls)),
    # api de blogs
    url(r'^api/1.0/blogs/$', BlogsAPI.as_view(), name='blogs_api'),
    # api de posts
    url(r'^api/1.0/blogs/(?P<username>[0-9a-zA-Z]+)/$', PostViewSet.as_view({'get': 'list'}), name='user_posts_list_api')
]
