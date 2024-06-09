from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('guest', views.guest, name='guest'),
    path('search', views.search, name='search'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('like-post', views.like_post, name='like-post'),
    path('like-post2', views.like_post2, name='like-post2'),
    path('comment-post', views.add_comment, name='comment-post'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('meeting', views.videocall, name='meeting'),
    path('join', views.join_room, name='join'),
    #path('articles', views.articles, name='articles'),
    path('diary', views.entry, name='diary'),
    path('delete-suicidal', views.delete_suicidal, name='delete_suicidal'),
    path('show', views.show, name='show'),
    path('submitreport', views.submitreport, name='submitreport'),
    path('show/<int:diary_id>', views.detail, name='detail'),
    path('logout', views.logout, name='logout'),
]