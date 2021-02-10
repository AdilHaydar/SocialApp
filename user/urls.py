from django.urls import path
from . import views



urlpatterns = [
    path('login/',views.loginUser,name = "login"),
    path('register/',views.register,name = "register"),
    path('logout/',views.logoutUser,name = "logout"),
    path('edit/<str:username>',views.change_user,name="user-edit"),
    path('view/<str:username>',views.view_user,name="user-view"),
    path('set-perm/',views.view_permission,name = "set-perm"),
    path('add-delete-perm/<int:pk>',views.change_permission,name='add-delete-perm'),
    path('add-group/',views.add_group,name='add-group'),
    path('change-group/',views.change_group,name='change-group'),
    path('remove-group/',views.remove_group,name='remove-group'),
    path('show-group-members/<str:name>',views.show_group_members,name='show-group-members'),
    path('edit-user/<str:username>',views.edit_user,name='edit-user'),
    path('view-other-user/<str:username>',views.view_other_user,name='view-other-user')
    
]
