from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post
# Create your views here.


def post_create(request):
    return HttpResponse("<h1>Create</h1>")


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance,
        "title": "Detail"
    }

    return render(request, "post_detail.html", context)


def post_list(request):

    object_list = Post.objects.all()
    if request.user.is_authenticated():

        context = {
            "object_list": object_list,
            "title": "My Post List"
        }
    else:
        context = {
            "object_list": object_list,
            "title": "List"
        }
    return render(request, "index.html", context)
    # return HttpResponse("<h1>List</h1>")


def post_update(request):
    return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
