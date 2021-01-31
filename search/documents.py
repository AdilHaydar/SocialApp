from django_elasticsearch_dsl import Document, Index, fields
from Post.models import Post, File, Like, TagPost, Comment, Tag, Location
from user.models import User




#relationship'ler için https://django-elasticsearch-dsl.readthedocs.io/en/latest/fields.html

tags = Index('tags')
@tags.doc_type
class TagDocument(Document):
	post = fields.ObjectField(properties = {
		'id' : fields.IntegerField(),
		'statement' : fields.TextField(),
		'file' : fields.ObjectField(properties={
			'file' : fields.FileField()
		}),
		'created_date' : fields.DateField(),
		'user' : fields.ObjectField(properties={
			'username' : fields.TextField(),
			'avatar' : fields.FileField(),
		})
	})

	tag = fields.ObjectField(properties = {
		'title' : fields.TextField()
	})

	class Django:
		model = TagPost

		fields = [
			'title',
		]
	#burada hata var. çözemezsem nedtedfield ile sanırım oluyordu o şekilde Tag'dan gelip tagpost'u ve onun postunu almaya çalış.
	related_models = [Post, Tag]

posts = Index('posts')
@posts.doc_type
class PostDocument(Document):
	user = fields.ObjectField(properties = {
		'username' : fields.TextField(),
		'avatar' : fields.FileField(),
		})

	file = fields.ObjectField(properties = {
		'file' : fields.FileField()
	})

	location = fields.ObjectField(properties = {
		'city' : fields.TextField(),
		'country' : fields.TextField()
	})
	
	"""def prepare_location(self, instance):
		results = instance.location
		try:
			return {
				"longtitude" : results["longtitude"],
				"latitude" : results["latitude"],
			}
		except TypeError:
			return {"longtitude":None,"latitude":None}"""
		

	class Django:
		model = Post

		fields = [
			'id',
			'statement',
			'created_date',
		]

	related_models = [User, File, Location]


user = Index('users')

@user.doc_type
class UserDocument(Document):

	post = fields.ObjectField(properties = {
		'id' : fields.IntegerField(),
		'statement' : fields.TextField(),
		'location' : fields.ObjectField(properties = {
			'city' : fields.TextField(),
			'country' : fields.TextField(),
		}),
		
		'file' : fields.ObjectField(properties={
			'file' : fields.FileField()
		}),
		'created_date' : fields.DateField(),
	})
	class Django:
		model = User

		fields = [
			'id',
			'username',
			'birthday',
			'avatar',
			'info',
			'web_page',
			'active',
			'timestamp',
		]

	related_models = [Post]

#bu alanda yapılan değişikliler sonrası 'python manage.py search_index --rebuild' komutunu çalıştır.

#views.py dosyasında ki videodan baktım ve hatalı kısımları https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html
#adresinden düzelttim.


#fields içerisine vermediğimiz şeyleri bize getirmiyor, mesela id değeri created date vs getirmiyoruz yazmazsak fields içerisine.
