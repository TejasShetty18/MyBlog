from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from datetime import date
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views import View

from .models import Post
from . forms import CommentForm


# all_posts = [
#     {
#         "slug": "hike-in-the-mountain",
#         "image":"mountains.jpg",
#         "author":"Tejas",
#         "date" :date(2023,7,13),
#         "title":"Mountain Hiking",
#         "excert":"there's nothing like the views you get when hiking in the Mountain and I want even prepared for what happened whilst Iwas enjoying the views",
#         "content":"good evening"
#     },
#     {
#         "slug": "i-love-coding",
#         "image":"coding.jpg",
#         "author":"Tejas",
#         "date" :date(2023,7,13),
#         "title":"Programming is greate",
#         "excert":"there's nothing like the views you get when hiking in the Mountain and I want even prepared for what happened whilst Iwas enjoying the views",
#         "content":"good evening"
#     },
#     {
#         "slug": "traking",
#         "image":"woods.jpg",
#         "author":"Tejas",
#         "date" :date(2023,7,13),
#         "title":"Mountain traking",
#         "excert":"there's nothing like the views you get when hiking in the Mountain and I want even prepared for what happened whilst Iwas enjoying the views",
#         "content":"good evening"
#     }
# ]

# def get_date(posts):
#     return posts['date']

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name="posts"

    def get_queryset(self):
      queryset = super().get_queryset()
      data = queryset[:3]
      return data
    

    
class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name="all_post"



class SinglePostView(View):
   template_name = "blog/post-details.html"
   model = Post

   def is_stored_post(self,request,post_id):
      stored_post = request.session.get("stored_post")
      if stored_post is not None:
          is_saved_for_later = post_id in stored_post
      else:
          is_saved_for_later = False
         
      return is_saved_for_later

   def get(self,request,slug):
      post = Post.objects.get(slug=slug)
     
      context={
         "post": post,
         "post_tags": post.tags.all(),
         "comment_form":CommentForm(),
         "comments":post.comments.all().order_by("-id"),
         "saved_for_later":self.is_stored_post(request, post.id)
      }
      return render(request, "blog/post-details.html",context)
   
   def post(self,request,slug):
      comment_form = CommentForm(request.POST)
      post = Post.objects.get(slug=slug)

      if comment_form.is_valid():
         comment = comment_form.save(commit=False)
         comment.post = post
         comment.save()

         return HttpResponseRedirect(reverse("post_details_page", args=[slug])) 

      
      context = {
         "post": post,
         "post_tags": post.tags.all(),
         "comment_form": comment_form,
         "comments":post.comments.all().order_by("-id"),
         "saved_for_later":self.is_stored_post(request, post.id)
      }
      return render(request,"blog/post-details.html",context)   

class ReadLaterView(View):
      def get(self,request):
           stored_post = request.session.get("stored_post")

           context = {}

           if stored_post is None or len(stored_post) == 0:
               context["posts"] = []
               context["has_posts"] = False
           else:
               posts = Post.objects.filter(id__in=stored_post)
               context["posts"] = posts 
               context["has_posts"] = True

           return render(request, "blog/stored-post.html", context)


      def post(self,request):
         stored_post = request.session.get("stored_post")

         if stored_post is None:
              stored_post = []

         post_id = int(request.POST["post_id"])

         if post_id not in stored_post:
             stored_post.append(post_id)
         else:
             stored_post.remove(post_id)

         request.session["stored_post"] = stored_post

         return HttpResponseRedirect("/blog")
      

#    def get_context_data(self, **kwargs):
#       context =  super().get_context_data(**kwargs)
#       context["post_tags"] = self.object.tags.all()
#       context["comment_form"] = CommentForm
#       return context


# def starting_page(request):
#     latest_post = Post.objects.all().order_by("-date")[:3]    # it fetches the top 3 latest posts
#     # sorted_post=sorted(all_posts, key= get_date)
#     # latest_post=sorted_post[-3:]
#     return render(request, "blog/index.html", {
#         "posts" : latest_post
#     })

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html",{
#         "all_post":all_posts
#     })


# def post_details(request, slug):
#    identified_post = get_object_or_404(Post, slug=slug)
#    return render(request,"blog/post-details.html", {
#       "post": identified_post,
#       "post_tags": identified_post.tags.all()
#     })
