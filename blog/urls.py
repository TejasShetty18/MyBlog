from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.StartingPageView.as_view(),name= "starting_page"),
    path("posts", views.AllPostsView.as_view(), name="posts_page"),
    path("post/<slug:slug>", views.SinglePostView.as_view(), name="post_details_page"), # /posts/my-first-post
    path("read-later",views.ReadLaterView.as_view(), name="read_later")
]