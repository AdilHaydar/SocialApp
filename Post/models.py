from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
def upload_to(instance,filename):
	username = instance.post.user.username
	return '%s/%s/%s'%('PostsFiles',username,filename)

class Location(models.Model):
	
	city = models.CharField(max_length = 30, blank=True, null=True, default='')
	country = models.CharField(max_length = 60, blank=True, null=True, default='')
	coordinates = JSONField(blank=True, null=True,default=dict)

	def __str__(self):
		return '/'.join([self.city,self.country])

class CommonField(models.Model):
	statement = models.TextField(null=False, blank=False)
	created_date = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)

	class Meta:
		abstract = True

class Post(CommonField):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name = 'post')
	location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL,related_name='post')

	class Meta:
		ordering = ['-created_date']


class Comment(CommonField):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name = 'comment')
	post = models.ForeignKey(to=Post, on_delete=models.CASCADE,related_name="comment")

	class Meta:
		ordering = ['created_date']


class File(models.Model):
	post = models.ForeignKey(to=Post, on_delete=models.CASCADE,related_name='file')
	file = models.FileField(upload_to=upload_to, null=True, blank=True)

class Tag(models.Model):
	title = models.CharField(max_length=120, unique = True)

	def __str__(self):
		return self.title
		
class TagPost(models.Model):
	post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='tag')
	tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE, related_name='post')
	title = models.CharField(max_length=120, null = False, blank = False)

	def __str__(self):
		return self.tag.title

class Like(models.Model):
	user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name = 'likes')
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username +" Liked "+ str(self.post.id)

	class Meta:
		constraints = [ models.UniqueConstraint(fields=['user','post'],  name="unique_like")]

		ordering = ["-created_date"]

