from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("signup/", views.signup),
    path("login/", views.login_user),
    path("logout/", views.logout_user),
    
    # Profile
    path("profile/<str:username>", views.get_user_profile),
    path("setprofilepic/", views.set_profile_pic),
    path("deleteprofilepic/", views.delete_profile_pic),
    path("getprofilepic/<str:username>", views.get_profile_pic),
    path("updateprofile/", views.update_profile),
    path("deleteuser/", views.delete_user),

    # Posts
    path("createpost/", views.create_post),
    path("userposts/<str:username>", views.all_user_posts),
    path("deletepost/", views.delete_post),

    # Admin stuff (unnecessary)
    path("", views.get_all_users),
    path("viewallposts/", views.view_all_posts),
]
