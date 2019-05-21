from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt
from .models import Image, Comment, Profile, Contact
from .forms import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    '''
    view function to display landing page
    '''
    current_user = request.user
    profile=Profile.get_profile(current_user)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.main_user = current_user
            profile.save()
        return redirect('profile')
    else:
        form = UpdateProfileForm()

    return render(request, 'index.html',{"form":form})

@login_required(login_url='/accounts/login/')
def home(request):
    '''
    view function to feeds page
    '''

    return render(request, 'home.html')

@login_required(login_url='/accounts/login/')
def image(request):
    '''
    view function to upload image page
    '''

    current_user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            user_profile = Profile.get_profile(current_user)
            image.main_user = current_user
            image.profile = user_profile
            image.save()
        return redirect('profile')
    else:
        form = UploadImageForm()

    return render(request, 'image.html', {"form":form})

@login_required(login_url="/accounts/login/")
def profile(request):
    title = request.user.username
    try:
        current_user=request.user.id
        photos=Image.objects.filter(main_user=current_user)
        profile=Profile.get_profile(current_user)
        current_user = request.user
        profile=Profile.get_profile(current_user)

        if request.method=='POST':
            form=UpdateProfileForm(request.POST,request.FILES )
            if form.is_valid():
                profile=form.save(commit=False)
                Profile.objects.filter(main_user=current_user).update(bio=bio,profile_pic=profile_pic)
            return redirect("profile")
        else:

            form=UpdateProfileForm()

    except Exception as e:
        raise Http404()

    return render(request,"profile.html",{'profile':profile, "title":title, "photos":photos,"form":form})

@login_required(login_url='/accounts/login/')
def update(request):
    current_user = request.user
    profile=Profile.get_profile(current_user)

    if request.method=='POST':
        form=UpdateProfileForm(request.POST,request.FILES )
        if form.is_valid():
            profile=form.save(commit=False)
            bio=form.cleaned_data['bio']
            profile_pic=form.cleaned_data['profile_pic']
            update=Profile.objects.filter(main_user=current_user).update(bio=bio,profile_pic=profile_pic)
            profile.main_user=current_user
            profile.save(update)
        return redirect("profile")
    else:

        form=UpdateProfileForm()

        return render(request,"update.html",{"form":form})

@login_required(login_url='/accounts/login/')
def comment(request,image_id):
    try:
        image=Image.objects.filter(id=image_id).all()
        comment=Comments.objects.filter(image=image_id).all()
    except Exception as e:
        raise  Http404()

    image=Image.objects.filter(id=image_id).all()

    if request.method=='POST':
        current_user=request.user
        image=request.POST.get("id","")
        form=CommentForm(request.POST)
        if form.is_valid:
            comments=form.save(commit=False)
            comments.main_user=current_user
            comments.image= image
            comments.save()
            return redirect('comment',image_id)
    else:
        form=CommentForm()
    return render(request,"comment.html",{"images":image,'form':form,"comments":comment,"count":count,"forms":forms})

@login_required(login_url='/accounts/login/')
def search(request):
    if 'user' in request.GET and request.GET['user']:
        name=request.GET.get("user")
        users=Profile.search_users(name)
        message=f'{name}'

        return render(request,'search.html',{'message':message,'users':users,"name":name})
    else:
        message="You did not search any user please input a user name"
        return render(request,"search.html",{"message":message})


@login_required(login_url='/accounts/login/')
def otherprofile(request,user_id):
    try:
        user = User.objects.get(id = user_id)
        profile=Profile.get_profile(user)
        photos=Image.objects.filter(main_user=user)
    except Exception as e:
        raise Http404()

    current_user = request.user
    if request.method == 'POST':
        form = FollowForm(request.POST, request.FILES)
        if form.is_valid():
            follower=form.save(commit=False)
            follower.user_to= profile.user
            follower.user_from=current_user

            follower.save()
            return redirect('otherProfile.html')

    else:
        form=FollowForm()
    return render(request,"otherProfile.html",{"user":user,'profile':profile,"photos":photos,"form":form})
