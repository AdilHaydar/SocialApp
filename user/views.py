from django.shortcuts import render,redirect,get_object_or_404,HttpResponse, Http404, HttpResponseRedirect, reverse
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import User
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission
from urllib.parse import urlencode
from django.conf import settings
from .decorators import allowed_perms
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
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")
        phone = form.cleaned_data.get("phone")
        picture = form.cleaned_data.get("picture")
        gender = form.cleaned_data.get('gender')

        group = Group.objects.get(name=settings.DEFAULT_GROUP)

        registeredUser = User(username = username,name = name, gender=gender,picture=picture ,surname = surname, phone = phone , email = email)
        registeredUser.set_password(password)
        registeredUser.group = group
        registeredUser.save()
        login(request, registeredUser)

        messages.success(request,'Registered successfully')
        return redirect(reverse('user-view', kwargs={'username':request.user.username}))
    if form.errors:
        messages.warning(request,form.errors,'danger')
    print(form.errors)
    return render(request,"back_end/user/register_sablon2.html",context)
        
def loginUser(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(username = username)
        if len(user) != 1:
            messages.info(request,"User does not exist.")
            return render(request,'back_end/user/login_sablon.html',{'form':form})
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.info(request,"Password doesn't match.")
                return render(request,'back_end/user/login_sablon.html',{'form':form})
        messages.success(request,"Giriş Başarılı")
        login(request,user)
        return redirect('eytpanelv1')
        #return redirect(reverse('view', kwargs={'username':request.user.username}))
    
    return render(request,'back_end/user/login_sablon.html',{'form':form})

def logoutUser(request):
    logout(request)
    messages.success(request,"You are logout succesfully")
    return redirect('login')


@login_required(login_url = "index")
def change_user(request,username):
    if (not request.user.is_authenticated) and (not request.user.username == username):
        raise Http404

    user = get_object_or_404(User, username=username)
    form = UserUpdateForm(data=request.POST or None, files = request.FILES or None, instance=user)

    if form.is_valid():
        updatedUser = form.save(commit=False)
        for data in form.changed_data:
            updatedUser.data = form.cleaned_data.get(data)
        
        updatedUser.set_password(form.cleaned_data.get('password'))
        updatedUser.save()
        login(request, updatedUser)
        
        return redirect(reverse('user-view', kwargs={'username':request.user.username}))
    return render(request, 'back_end/user/edit.html',{'form':form})

@login_required(login_url = "user:login")
def view_user(request,username):
    if request.user.is_authenticated:
        if request.user.username == username:

            return render(request,'back_end/user/view.html')
        
    return HttpResponse('<b>Sayfayı Görüntülemek İçin Yetkiniz Yok</b>')

@allowed_perms('view_permission')
def view_permission(request):
    permissions = Permission.objects.all()
    groups = Group.objects.all()

    context = {
        'perms' : permissions,
        'groups' : groups,
        'apps' : settings.APPS,
    }
    if request.GET.get('groups'):
        context['selected_group'] = Group.objects.get(id=request.GET.get('groups'))
    
    
    return render(request,'back_end/permission/perms.html',context)

@allowed_perms('change_permission')
def change_permission(request,pk):
    if request.POST.get('perms'):
        perms = request.POST.getlist('perms')
        perms = list(map(int, perms))

        group = Group.objects.get(id=pk)
        group_perms = group.permissions.values_list('id', flat=True)

        for perm in perms:
            if perm in group_perms:
                continue
            else:
                group.permissions.add(perm)

        removed_perms = set(group_perms).difference(set(perms))
        
        for perm in removed_perms:
            group.permissions.remove(perm)

        base_url = reverse('set-perm')
        query_string = urlencode({'groups':group.id})
        url = f"{base_url}?{query_string}"

    return redirect(url)

@allowed_perms('add_group')
def add_group(request):
    groups = Group.objects.all()

    context = {'groups':groups,'default_group':settings.DEFAULT_GROUP}

    if request.method == "POST":
        if request.POST.get('group'):
            name = request.POST.get('group')
            if name == settings.DEFAULT_GROUP:
                raise Exception(f'The group name is assigned by default and cannot be given to another group (Incorrect name is {settings.DEFAULT_GROUP})')
            Group.objects.create(name=name)

        if request.POST.getlist('delete'):
            group_ids = request.POST.getlist('delete')

            for id in group_ids:
                delete_group = Group.objects.get(id=id)

                if delete_group.user.count() != 0:
                    default_group = Group.objects.get(name=settings.DEFAULT_GROUP)

                    for user in delete_group.user.all():
                        user.group = default_group
                        user.save()

                if delete_group.name == 'Default':
                    continue
                #TODO
                #Yeni group eklediğinde bu gruba default adı verilmesin.
                delete_group.delete()

        return redirect('add-group')
    return render(request,'back_end/group/add.html',context)

@allowed_perms('delete_group')
def remove_group(request):
    if request.POST.getlist('delete'):
        group_ids = request.POST.getlist('delete')
        for id in group_ids:
            Group.objects.get(id=id).delete()

    return redirect('add-group')

@allowed_perms('change_group')
def change_group(request):
    groups = Group.objects.all()

    context = {
        'groups':groups,
    }

    if request.GET.get('username'):
        username = request.GET.get('username')
        users = User.objects.filter(username__icontains = username)
        context['users'] = users
    
    username = request.GET.get('username')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_name = request.POST.get('groups')

        base_url = reverse('change-group')
        query_string = urlencode({'username':username})
        url = f"{base_url}?{query_string}"

        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)

        user.group = group
        user.save()

        return redirect(url)

    return render(request,'back_end/group/change.html',context)

@allowed_perms('view_group')
def show_group_members(request, name):
    group_members = Group.objects.prefetch_related('user').get(name=name).user.all()

    return render(request,'back_end/group/show_group_members.html',{'group_members':group_members})

@allowed_perms('change_user')
def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_superuser:
        if not request.user.is_superuser:
            messages.warning(request,'You cant edit SUPERUSER','danger')
            return redirect(reverse('user-view', kwargs={'username':request.user.username}))
    form = UserUpdateForm(data=request.POST or None, files = request.FILES or None, instance=user)

    if form.is_valid():

        updatedUser = form.save(commit=False)

        for data in form.changed_data:
            updatedUser.data = form.cleaned_data.get(data)

        updatedUser.set_password(form.cleaned_data.get('password'))
        updatedUser.admin = form.cleaned_data.get('admin')

        updatedUser.save()
        messages.success(request,'Process Successfully Completed')

        return redirect(reverse('view-other-user', kwargs={'username':username}))

    if form.errors:
        messages.warning(request,form.errors,"danger")

    return render(request, 'back_end/user/edit.html',{'form':form})
    

@allowed_perms('view_user')
def view_other_user(request, username):

    user = User.objects.get(username=username)

    return render(request,'back_end/user/view_other_user.html',{'user':user})

    
