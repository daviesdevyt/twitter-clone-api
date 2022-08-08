from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile, User, Post, Comment
from .serializer import CommentSerializer, ProfileSerializer, UserSerializer, PostSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import os

# Regular functions
def delete_pic(pic):
    try:
        if not pic.path.endswith("\default.png"):
            os.remove(pic.path)
    except:pass

# Auth
@api_view(["POST"])
def signup(request):
    try:
        if request.data.get("id"):
            del request.data['id']
        user = User.objects.create_user(username=request.data.get("username"), password=request.data.get("password"), email=request.data.get("email")) # Takes in username, email, password
        profile = Profile(user=user, name=request.data.get("fullname")) # Create profile details like full name, bio and picture
        if request.FILES.get('image'):
            profile.profilepic = request.FILES.get('image')
        if request.data.get("bio"):
            profile.bio = request.data.get("bio")
        profile.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except Exception as e:
        return Response(f"Error while saving {e}")


@api_view(["POST"])
def login_user(request):
    print(request.data)
    user = authenticate(**request.data)
    if user:
        login(request, user)
        return Response("Logged in")
    else:
        return Response('Invalid credentials')

@api_view(["GET"])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response("Logged out")
    else:
        return Response('No user is logged in')

# Profile
@api_view(["GET"])
def get_user_profile(request, username):
    serializer = ProfileSerializer(User.objects.get(username=username).profile)
    return Response(serializer.data)

@login_required
@api_view(["POST"])
def set_profile_pic(request):
    delete_pic(request.user.profile.profilepic)
    try:
        request.user.profile.profilepic = request.data['image']
        request.user.profile.save()
        return Response("Saved profile picture")
    except Exception as e:
        Response(f"Error saving image {e}")

@login_required
@api_view(["POST"])
def update_profile(request):
    profile = request.user.profile # Update profile details like full name, bio and picture
    data = request.data
    try:
        fullname, bio, image = data.get("fullname"), data.get('bio'), data.get("image")
        if fullname: profile.name = fullname
        if image: profile.profilepic = image
        if bio: profile.bio = bio
        profile.save()
        return(ProfileSerializer(profile).data)
    except Exception as e:
        return Response(f"Error while saving {e}")

@login_required
@api_view(["GET"])
def delete_profile_pic(request):
    delete_pic(request.user.profile.profilepic)
    request.user.profile.profilepic = "uploads/users/default.png"
    request.user.profile.save()
    return Response("Removed profile picture")

@api_view(["GET"])
def get_profile_pic(request, username):
    return Response(ProfileSerializer(User.objects.get(username=username).profile).data.get("profilepic"))


# Posts
@login_required
@api_view(["POST"])
def create_post(request):
    try:
        post = Post.objects.create(text=request.data.get("text"), user=request.user, image=request.FILES.get("image"))
        return Response(PostSerializer(post).data)
    except Exception as e:
        return Response(f"Error while saving {e}")

@login_required
@api_view(["GET"])
def delete_post(request):
    try:
        post = Post.objects.filter(user=request.user).filter(id=request.GET.post_id).first()
        post.delete()
        return Response("Post Deleted")
    except Exception as e:
        return Response(f"Error while deleting {e}")


@api_view(["GET"])
def all_user_posts(request, username):
    serializer = PostSerializer(Post.objects.filter(user=User.objects.get(username=username)).order_by('-timestamp'), many=True)
    return Response(serializer.data)

@login_required
@api_view(["GET"])
def delete_user(request):
    if request.user.is_superuser:
        if request.GET.username:
            user = User.objects.get(username=request.GET.username)
            if user:
                user.delete()
            else:
                return Response("User was not found")
        else:
            request.user.delete()
        return Response("Deleted user")
    request.user.delete()
    logout(request)
    return Response("Deleted user")

@login_required
@api_view(["POST"])
def add_comment(request):
    try:
        comment = Comment.objects.create(text=request.data.get('text'), image=request.data.get('image'), post=Post.objects.get(id=request.data.get('post')), user=request.user)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    except Exception as e:
        return Response(f"Error while adding comment {e}")

@login_required
@api_view(["GET"])
def delete_comment(request):
    try:
        comment = Comment.objects.filter(user=request.user).filter(id=request.GET.id)
        if comment:
            comment.delete()
            return Response("Comment deleted")
        else:
            return Response("Comment was not found")
    except Exception as e:
        return Response(f"Error while adding comment {e}")


# Admin stuff
@api_view(["GET"])
def view_all_posts(request):
    serializer = PostSerializer(Post.objects.all(), many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_users(request):
    serializer = UserSerializer(User.objects.all(), many=True)
    return Response(serializer.data)