from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
from .models import Post
# Create your views here.


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # messages success
        messages.success(request, "Succesfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance,
        "title": "Detail"
    }

    return render(request, "post_detail.html", context)


def post_list(request):

    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)  # Show 25 object_list per page
    page_request_var = "emily"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "page_request_var": page_request_var,
        "object_list": queryset,
        "title": "My Post List"
    }
    return render(request, "post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(
            request, "<a href='#'>Item</a> Saved.", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Succesfully deleted")
    return redirect("posts:list")
