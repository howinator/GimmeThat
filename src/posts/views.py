import logging

from urllib.parse import quote_plus

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from contact.views import contact_us

from .forms import PostForm
from .models import Post, Category
# Create your views here.

logger = logging.getLogger(__name__)


def post_create(request):
    """ View to create a new post.

    This view is used to create a new post and re-direct the user to
    the URL for the new post.
    """
    # We can't let people creat a post if they don't have the correct
    # permissions
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
    form = PostForm(request.POST or None, request.FILES or None)
    # process the form if it's valid
    if form.is_valid():
        instance = form.save(commit=False)
        # we should save who is posting
        instance.user = request.user
        instance.save()
        # messages success
        messages.success(request, "Succesfully created")
        # the model for a post has the absolute url which we re-direct to
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }

    return render(request, "posts/pages/post_form.html", context)


def post_detail(request, slug=None):
    """ View displayes the actual post."""
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "instance": instance,
        "title": "Detail",
    }

    return render(request, "posts/pages/post_detail.html", context)


def post_list(request):

    contact_form = contact_us(request)

    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)  # Show 25 object_list per page
    page_request_var = "page"
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
        "title": "Emily's GimmeThat Blog",
        "contact_form": contact_form,
        "debug": settings.DEBUG
    }

    return render(request, "posts/pages/post_list.html", context)


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
    # For testing mail stuff
#    if not settings.DEBUG:
#        send_mail('this is a test', 'someone visited post_list',
#                  'howiethebot@gmail.com', ['hben592@gmail.com'],
#                  fail_silently=False)
    return render(request, "posts/pages/post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Succesfully deleted")
    return redirect("posts:list")


def post_category(request, category=None):

    # little hack to show under construction when not debugging
    # REMOVE when done
    context = {}
    if not settings.DEBUG:
        return render(request, "posts/pages/construction.html", context)
    posts_category = Category.objects.get(slug=category)
    queryset_list = Post.objects.filter(category=posts_category)
    context = {
        "object_list": queryset_list,
        "category": category
    }
    return render(request, "posts/pages/post_category_list.html", context)
