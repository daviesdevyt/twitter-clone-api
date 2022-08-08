from django.urls import path
from . import views
urlpatterns = [
    path("auth/", views.auth),
    path("index/<str:username>", views.profile)
]