from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount,Likedby,Comment,DiaryModel,ReportModel
from itertools import chain
from .forms import AddForm
from datetime import datetime
import random
import uuid
from django.http import HttpResponse,JsonResponse
# Create your views here.

@login_required(login_url='signin')
def index(request):  
   
    liked_posts = Post.objects.filter(likedby=request.user)
    total_entries=DiaryModel.objects.filter(user=request.user)
    total=len(total_entries)
    user_object = User.objects.get(username=request.user.username)
    user_following_list = []
    feed = []
    user_profile = Profile.objects.get(user=user_object)
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        
        feed.append(feed_lists)

    if len(user_following_list)>0:
  
        ourlist=Post.objects.filter(user=request.user.username)      
        feed.append(ourlist)   
        
       
                  
        feed_list = list(chain(*feed))
        
        #liked_usernames = [user_profile.username for user_profile in feed_list.likedby.all()]
        #print(liked_usernames)
      
    else:
   
        feed_lists=Post.objects.all()
        feed.append(feed_lists)
        feed_list = list(chain(*feed))
  
   
    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
   # print(user_following_all)


    return render(request,'index.html',{'liked_posts': liked_posts,'user_following_all':user_following_all, 'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4],'totalentry':total}, )

@login_required(login_url='signin')
def submitreport(request):
       if request.method =='POST':
        reason=request.POST['reason']
        idd=request.POST['id']
        print(idd)
        post=Post.objects.get(id=idd)
        print(post)
        ReportModel.objects.create(user=request.user,reason=reason,post=post)
        return redirect('/')


def add_comment(request):
    #post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        #print(req) 
        idd = request.POST.get('post_id', 'None') 
        print(idd)
       # request_getdata = request.POST.get('comment', 'None') 
        #print(request_getdata)
        print(idd)
        post = Post.objects.get(id=idd)
                
        content = request.POST.get('comment')
        comment = Comment.objects.create(user=request.user, content=content)
        post.comments.add(comment)

        data={
            'id':idd,
            'comment':content,
            'username':request.user.username,
            'time'    :comment.created_at
            
        }
        return JsonResponse(data=data)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
  
  
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


def guest(request):
         my_cookie_value = request.COOKIES.get('unique_id', 'defaultt')
         print(my_cookie_value)
         if my_cookie_value == 'defaultt':  
              
              unique_id=uuid.uuid4()
              response=redirect('guest')
              response.set_cookie(key='unique_id',value=unique_id)
            
              return response
         else:
             idd=request.COOKIES['unique_id']
             return render(request,'index.html',{'idd':idd[-5:]})
       
          
        
 


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('/')
    return render(request, 'setting.html', {'user_profile': user_profile})



@login_required(login_url='signin')
def profile(request, pk):
   # allposts=Post.objects.filter(user=pk)
    #print(allposts)
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        messages.info(request, 'post uploaded')
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post2(request):
    username = request.user.username
    user_model = User.objects.get(username=username)            
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    if request.user in post.likedby.all():
            post.likedby.remove(request.user)
            post.no_of_likes = post.no_of_likes-1
            post.save()
            data={
            'data':'unliked'
        }
            return JsonResponse(data=data)
            
    else:
        # User hasn't liked the post, so like it
        post.likedby.add(request.user)
        post.no_of_likes = post.no_of_likes+1
        post.save()
                    
                       
        data={
            'data':'liked'
        }
        return JsonResponse(data=data)






@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    user_model = User.objects.get(username=username)            
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()       
        #by=Likedby.objects.create(username=username)
        by2= Likedby.objects.filter(username=username).first()
        if by2 == None:
            by=Likedby.objects.create(username=username)
            by.save()
            post.no_of_likes = post.no_of_likes+1
            post.likedby.add(by)
            print("hhh",post.likedby.all())
            post.save()
        else:
            post.no_of_likes = post.no_of_likes+1
            post.likedby.add(by2)
            print('ffff',post.likedby)
            print("fff",post.likedby.all())
            post.save()
            
            
        
        data={
            'data':'liked'
        }
        return JsonResponse(data=data)
    else:
        user_profile=Likedby.objects.filter(username=username).first()
        userr=Likedby.objects.all()
        
        print("all-:", post.likedby.all())

        post.likedby.remove(user_profile)
        
        print("After removal:", post.likedby.all())
        
        
        post.no_of_likes = post.no_of_likes-1
        like_filter.delete()
        post.save()
        data={
            'data':'unliked'
        }
        return JsonResponse(data=data)

@login_required(login_url='signin')
def dashboard(request):
    return render(request,'dashboard.html')



@login_required(login_url='signin')
def videocall(request):
    return render(request,'webk.html')

@login_required(login_url='signin')
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')

@login_required(login_url='signin')
def articles(request):
    return render(request,'pod.html')

@login_required(login_url='signin')
def entry(request):
    form = AddForm(request.POST or None)
    if request.method =='POST':
        if form.is_valid():
            note = request.POST['note']
            content = request.POST['content']
            posted_date = datetime.now()
            todays_diary = DiaryModel()
            todays_diary.user=request.user
            todays_diary.note = note
            todays_diary.posted_date = posted_date
            todays_diary.content = content
            todays_diary.save()
            return redirect('diary')

    return render(request,'add.html',{ 'title': 'Add your thoughts','detailtitle':True,'subtitle': 'Add what you feel and we\'ll store it for you.', 'add_highlight': True, 'addform': form})


@login_required(login_url='signin')
def show(request):
    diaries=DiaryModel.objects.filter(user=request.user).order_by('posted_date')
   # diaries = DiaryModel.objects.order_by('posted_date')
    icon = True if len(diaries) == 0 else None

    return render(request,'show.html', {'show_highlight': True, 'title': 'All of your Thoughts','subtitle': 'It\'s all you\'ve written.','detailtitle':True,'diaries': reversed(diaries),'icon': icon})

def detail(request, diary_id):
    diary = get_object_or_404(DiaryModel, pk=diary_id)

    return render( request, 'detail.html',{'show_highlight': True,'title': diary.note,'subtitle': diary.posted_date, 'diary': diary })

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')