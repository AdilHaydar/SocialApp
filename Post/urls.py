from django.urls import path
from . import views

urlpatterns = [
	path('view/<int:id>',views.view_post,name="view_post"),
	path('create_post_ajax/',views.create_post_ajax,name="create_post_ajax"),
	path('create_comment_ajax/',views.create_comment_ajax,name="create_comment_ajax"),
	path('like/',views.like_post,name="like_post"),
	path('unlike/',views.unlike_post,name="unlike_post"),
]
