from django.shortcuts import render,redirect,get_object_or_404,HttpResponse, Http404, HttpResponseRedirect, reverse
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import User, UserFollowing
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import JsonResponse
# Create your views here.

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    context = {
            "form" : form
        }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        birthday = form.cleaned_data.get("birthday")
        avatar = form.cleaned_data.get("avatar")
        info = form.cleaned_data.get('info')
        web_page = form.cleaned_data.get('web_page')

        registeredUser = User(username = username,birthday=birthday,avatar=avatar,info=info,web_page=web_page, email = email)
        registeredUser.set_password(password)
        registeredUser.save()
        login(request, registeredUser)
                
        messages.success(request,"Başarılı Bir Şekilde Kayıt Oldunuz.")
        return redirect("index")
    return render(request,"register.html",context)
        
def loginUser(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(username = username)
        if len(user) != 1:
            messages.info(request,"User does not exist.")
            return redirect("index")
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.info(request,"Password doesn't match.")
                return redirect("index")
        messages.success(request,"Giriş Başarılı")
        login(request,user)
        return redirect("index")
    
    return render(request,'login.html',{'form':form})

def logoutUser(request):
    logout(request)
    messages.success(request,"You are logout succesfully")
    return redirect("index")


@login_required(login_url = "index")
def userPanel(request,username):
    if (not request.user.is_authenticated) and (not request.user.username == username):
        raise Http404

    user = get_object_or_404(User, username=username)
    form = UserUpdateForm(data=request.POST or None, files = request.FILES or None, instance=user)

    if form.is_valid():
        updatedUser = form.save(commit=False)
        for data in form.changed_data:
            if data == 'password' and data == 'confirm':
                continue
            updatedUser.data = form.cleaned_data.get(data)
        updatedUser.set_password(form.cleaned_data.get('password'))
        updatedUser.save()
        login(request, updatedUser)
        
        return HttpResponseRedirect(reverse('view_profile', kwargs={'username':username}))
    return render(request, 'edit_profile.html',{'form':form})

    """user = get_object_or_404(User, username=username)
    if request.user.is_authenticated and not (request.user.username == username):
        raise Http404
    if request.method == "POST":

        if request.FILES.get('avatar'):
            user.avatar.delete()
            user.avatar = request.FILES.get('avatar')

        if request.POST.get('avatar-clear'):
            user.avatar.delete()

        user.birthday = request.POST.get('birthday')
        user.email = request.POST.get('email')

        if request.POST.get('password') and request.POST.get('confirm'):
            if request.POST.get('password') == request.POST.get('confirm'):
                user.set_password(request.POST.get('password'))
            else:
                messages.warning(request,'Password do not match!', 'danger')
                return render(request,'userPanel.html')
        user.save()
        messages.success(request,'Your profile successfully updated!')
        return redirect('index')"""
    return render(request, 'userPanel.html',{'username':username})

def view_replies(request,username):
    
    user = User.objects.prefetch_related('comment').get(username=username)
    comments = user.comment.union()

    page = request.GET.get('page',1)
    paginator = Paginator(comments,10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request,'user_profile_replies.html',{'user':user,'comments':comments})
        
def view_likes(request,username):

    user = User.objects.prefetch_related('likes').get(username=username)
    likes = user.likes.union()

    page = request.GET.get('page',1)
    paginator = Paginator(likes,10)
    try:
        likes = paginator.page(page)
    except PageNotAnInteger:
        likes = paginator.page(1)
    except EmptyPage:
        likes = paginator.page(paginator.num_pages)

    return render(request,'user_profile_likes.html',{'user':user,'likes':likes})


def follow(request):
    if request.is_ajax():
        target_user_id = request.GET.get('follow')
        target_user_id = int(target_user_id)
        target_user = User.objects.get(id = target_user_id)
        try:
            UserFollowing.objects.create(user_id = request.user, following_user_id = target_user)
        except IntegrityError:
            return JsonResponse({"success":False}, status=406)
        return JsonResponse({"succes":True}, status=200)
    else:
        return JsonResponse({"success":False}, status=400)

def unfollow(request):
    if request.is_ajax():
        target_user_id = request.GET.get('unfollow')
        target_user_id = int(target_user_id)
        target_user = User.objects.get(id=target_user_id)
        
        unf = UserFollowing.objects.get(user_id = request.user, following_user_id = target_user)
        unf.delete()
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)