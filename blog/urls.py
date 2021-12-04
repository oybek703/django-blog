from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<slug:slug>', views.post_details, name='post-details'),
    path('read-later', views.read_later, name='read-later')
]
