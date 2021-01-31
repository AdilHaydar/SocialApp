from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from search.documents import PostDocument, UserDocument, TagDocument
from django.contrib import messages
from user.models import User
# Create your views here.

def search(request):

	q = request.GET.get('q')
	searchq = request.GET.get('searchq')
	if q:
		if searchq == 'userq':
			users = UserDocument.search().query("match",username=q)

			if (len(list(users)) == 0):
				messages.warning(request,'Results not found','danger')

			return render(request,'search_user.html',{'users':users,'searchValue':q})

		if searchq == 'tagq':
			tags = TagDocument.search().query("match",title=q)

			if (len(list(tags)) == 0):
				messages.warning(request,'Results not found','danger')

			return render(request,'search_tag.html',{'tags':tags,'searchValue':q})
			
		posts = PostDocument.search().query("match", statement=q)
		if (len(list(posts)) == 0):
			messages.warning(request,'Results not found!','danger')
		#posts = posts.to_queryset()
	else:
		posts = ''
	return render(request, 'search.html',{'posts':posts,'searchValue' : q})

def view_profile(request,username):
	user = UserDocument.search().query("match",username=username)

	try:
		user = list(user)[0]
	except IndexError:
		return HttpResponse('<h3>User not found</h3>')
	posts = user.post

	page = request.GET.get('page',1)
	paginator = Paginator(posts,10)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'user_profile.html',{'users':user,'posts':posts})

	#user'da relatedobject manager is not iterable hatası alıyorum .to_queryset() bunu kullandığımda.
	#sanırım bunun nedeni userdocument içerisinde objectfield çağırdığımdan kaynaklanıyor.


#https://www.youtube.com/watch?v=cXYVE28igkE
#to_queryset yaparak normal django querysetine çeviriyorum yoksa user bilgisine vs ulaşamıyorum.
#onlara nasıl ulaşabileceğimi bulamadım. BULDUM, user da post'u, post'da file'ı çekebiliyorum.

