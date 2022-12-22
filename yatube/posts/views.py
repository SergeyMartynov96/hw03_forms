from .models import Group, Post, User
from .forms import PostForm
from .utils import paginator

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


QUAN_POST: int = 10


def index(request):
    """Возвращает пользователю HTML-код из шаблона index.html"""
    post_list = Post.objects.select_related(
        'author',
        'group'
    )
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Возвращает пользователю HTML-код из шаблона group_list.html"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related(
        'author'
    )
    page_obj = paginator(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Возвращает пользователю HTML-код из шаблона profile.html"""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = paginator(request, post_list)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Возвращает пользователю HTML-код из шаблона post_detail.html"""
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Возвращает пользователю HTML-код из шаблона create_post.html"""
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    return render(request, "posts/create_post.html", {'form': form})


def post_edit(request, post_id):
    """Возвращает пользователю HTML-код из шаблона post_detail.html"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': True, 'post': post})
