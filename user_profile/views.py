from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.models import User

from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm
)
from .decorators import  (
    not_logged_in_required
)
from .models import Follow,User
from notification.models import Notificaiton

#for mail sending and verifying..........
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
UserModel = get_user_model()


@never_cache
@not_logged_in_required
def login_user(request):
    if request.method=="POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password= password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.warning(request, 'Invalid Username or Password!')
        else:
            messages.warning(request, 'Invalid Username or Password!')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})
"""
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Wrong credentials")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)
    """


def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')


@never_cache
@not_logged_in_required
def register_user(request):
    

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('account.html',{
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail=form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[send_mail])
            email.send()
            messages.success(request,'Successfully created account')
            
            messages.info(request, "Activate Your Account from the Mail You Provided")
            return redirect('login')
        
    form = UserRegistrationForm()

    context = {
        "form": form
    }
    return render(request, 'registration.html', context)


def activate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, "Your account is activated now, you can log in now")
        return redirect('login')
    else:
        messages.warning(request,"Activation link is invalid")
        return redirect('register_user')

"""
from .forms import SignUpForm
def registration(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm
    return render(request, 'signup.html',{'form':form})
"""


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'profile.html', context)


@login_required
def change_profile_picture(request):
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            
            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_image = image
            user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('profile')


def view_user_information(request, username):
    account = get_object_or_404(User, username=username)
    following = False
    muted = None

    if request.user.is_authenticated:
        
        if request.user.id == account.id:
            return redirect("profile")

        followers = account.followers.filter(
        followed_by__id=request.user.id
        )
        if followers.exists():
            following = True
    
    if following:
        queryset = followers.first()
        if queryset.muted:
            muted = True
        else:
            muted = False

    context = {
        "account": account,
        "following": following,
        "muted": muted
    }
    return render(request, "user_information.html", context)


@login_required(login_url = "login")
def follow_or_unfollow_user(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    followed_by = get_object_or_404(User, id=request.user.id)

    follow, created = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        follow.delete()

    return redirect("view_user_information", username=followed.username)


@login_required(login_url='login')
def user_notifications(request):
    notifications = Notificaiton.objects.filter(
        user=request.user,
        is_seen=False
    )

    for notification in notifications:
        notification.is_seen = True
        notification.save()
        
    return render(request, 'notifications.html')


@login_required(login_url='login')
def mute_or_unmute_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    follower = get_object_or_404(User, pk=request.user.pk)
    instance = get_object_or_404(
        Follow,
        followed=user,
        followed_by=follower
    )

    if instance.muted:
        instance.muted = False
        instance.save()

    else:
        instance.muted = True
        instance.save()

    return redirect('view_user_information', username=user.username)

