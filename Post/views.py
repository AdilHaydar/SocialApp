from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from .models import Post, File, Tag, Comment, TagPost, Like, Location
from .forms import PostForm, FileForm, TagForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.models import User
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
import json
import base64
import os
from django.db.models import Q
import geoip2.database
from geoip2.errors import AddressNotFoundError
# Create your views here.

@login_required(login_url = 'user:login')
def index(request):
	posts = Post.objects.select_related('user').filter(Q(user__followers__user_id = request.user.id)|Q(user = request.user.id))
	page = request.GET.get('page',1)
	paginator = Paginator(posts,10)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,'posts.html',{'posts':posts})

@login_required(login_url='user:login')
def view_post(request,id):
	post = Post.objects.select_related('user').get(id = id)
	return render(request,'view_post.html',{'post':post})

@login_required(login_url = 'user:login')
def create_post_ajax(request):
	if request.method == "POST" and request.is_ajax():
		if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('user:login'))

		if request.POST.get('statement'):
			reader = geoip2.database.Reader('GeoLite2-City.mmdb')
			try:
				response = reader.city(request.META.get('REMOTE_ADDR'))

				location = Location.objects.create(city = response.city.name, country = response.country.name, coordinates = {'latitude':response.location.latitude,'longitude':response.location.longitude})

			except AddressNotFoundError:
				location = None

			post = Post.objects.create(user = request.user, statement = request.POST.get('statement'), location = location)
		else:
			return JsonResponse({"success":False}, status=406)

		if request.POST.get('files'):
			files = json.loads(request.POST.get('files'))['files']

			for file in files:
				
				file_data = file
				format, filestr = file_data.split(';base64,')
				ext = format.split('/')[-1]
				data = ContentFile(base64.b64decode(filestr), name='temp.'+ext)
				file = File.objects.create(post = post, file = data)
				
		if request.POST.get('tags'):
			tags = json.loads(request.POST.get('tags'))['tags']

			for tag in tags:
				TagPost.objects.create(title=tag,post = post, tag = TagForm.clean_title(title=tag))

		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)

@login_required(login_url = 'user:login')
def create_comment_ajax(request):
	if request.method == "POST" and request.is_ajax():
		post_id = request.POST.get('post_id')
		post_id = int(post_id)
		post = Post.objects.get(id = post_id)

		if request.POST.get('statement'):
			Comment.objects.create(post = post, statement = request.POST.get('statement'), user = request.user)
		else:
			return JsonResponse({"success":False}, status=406)
		return JsonResponse({"success":True}, status=200)
	return JsonResponse({"success":False}, status=400)

@login_required(login_url = 'user:login')
def like_post(request):
	if request.is_ajax():
		post_id = int(request.GET.get('post_id'))
		post = Post.objects.get(id = post_id)
		authUser = request.user
		try:
			Like.objects.create(user = authUser, post = post)
		except IntegrityError:
			return JsonResponse({"success":False}, status=406)
		return JsonResponse({"success":True}, status=200)
	else:
		return JsonResponse({"success":False}, status=400)

@login_required(login_url = "user:login")
def unlike_post(request):
	if request.is_ajax():
		post_id = int(request.GET.get('post_id'))
		post = Post.objects.get(id = post_id)
		authUser = request.user
		like = Like.objects.get(post=post, user=authUser)
		like.delete()
		return JsonResponse({"success":True}, status = 200)
	return JsonResponse({"success":False}, status=400)



#https://stackoverflow.com/questions/39576174/save-base64-image-in-django-file-field
#buradan base64'ü fotoyu çevirmeyi yap çünkü FileReader() ile js kullanarak yüklenen fotoyu ekranda göstermek için bize fotonun base64 kodunu veriyor.
#Yapıldı !!!




#https://stackoverflow.com/questions/58552487/how-to-calculate-video-length-and-thumbnail-of-video-in-django
#video uzunluğunu bu linkteki yöntem ile kontrol edebilirim fakat orada söylenenin aksine
#VideoClipFile değil VideoFileClip kullanmalıyım çünkü diğeri yok.


#Infinite scroll için kaynaklar:
#https://dev.to/coderasha/infinite-scroll-with-django-d0a
#https://github.com/raszidzie/infinite-scroll/blob/master/templates/posts.html
#https://simpleisbetterthancomplex.com/tutorial/2017/03/13/how-to-create-infinite-scroll-with-django.html
#infinite scroll için js kodunu ilk linkten aldım ve daha sonra infinite-container class'lı divi diğer col'lu divlerden ayırdım
#o şekilde düzgünce çalıştı.