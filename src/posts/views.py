from urllib.parse import quote_plus

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
from .models import Post
# Create your views here.


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # messages success
        messages.success(request, "Succesfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "instance": instance,
        "title": "Detail",
        "share_string": share_string,
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
        "title": "Emily's GimmeThat Blog"
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
    instance = get_object_or_404(Post, slug=slug)
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


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Succesfully deleted")
    return redirect("posts:list")


def post_category(request, category=None):
    return render("Under construction")
