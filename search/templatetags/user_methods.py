from django import template
from user.models import User, UserFollowing
from Post.models import Post

register = template.Library()

@register.filter(name='get_image_or_default')
def get_image_or_default(user,avatar):
    if avatar:
        return avatar
    else:
        user = User.objects.get(username = user.username)
        return user.get_image_or_default

    #elasticsearch de modelin fonksiyonlarına ulaşamdığım için ve bu methoda ulaşmam gerektiği için bunu kullanıyorum.
    #aslında buna gerek olmadan elasticsearch'ün views.py dosyasında user değişkeninin to_queryset gibi bir fonku vardı o fonk ile normal django querysi getirerek yapabilirim ama ben elasticsearch'ün kendi return ettiği veri tipinden caymak istemedim.
@register.filter(name="get_like_count")
def get_like_count(postId):
    postId = int(postId)
    post = Post.objects.get(id = postId)
    return post.likes.count()

@register.filter(name="get_comment_count")
def get_comment_count(postId):
    postId = int(postId)
    post = Post.objects.get(id = postId)
    return post.comment.count()


@register.filter(name='follow_or_unfollow')
def follow_or_unfollow(authUser, userId):

    followings = UserFollowing.objects.filter(user_id = authUser)
    followings = followings.values_list('following_user_id',flat=True)
    
    if authUser.id == userId:
        return None
    if userId in followings:
        return True
    else:
        return False

