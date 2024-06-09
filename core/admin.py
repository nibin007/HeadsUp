from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount,Likedby,Comment,DiaryModel,ReportModel,Suicidal

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Likedby)
admin.site.register(Comment)
admin.site.register(DiaryModel)
admin.site.register(ReportModel)
admin.site.register(Suicidal)
