from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Group, Post, User
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


QUAN_POST: int = 10


def index(request):
    """Возвращает пользователю HTML-код из шаблона index.html"""
    post_list = Post.objects.select_related(
        'author',
        'group'
    )
    paginator = Paginator(post_list, QUAN_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    paginator = Paginator(post_list, QUAN_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Возвращает пользователю HTML-код из шаблона profile.html"""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, "posts/create_post.html", {'form': form})
    form = PostForm()
    return render(request, "posts/create_post.html", {'form': form})


def post_edit(request, post_id):
    """Возвращает пользователю HTML-код из шаблона post_detail.html"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect(
            'posts:post_detail', post_id
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': True, 'post': post})
