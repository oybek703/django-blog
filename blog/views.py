from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from django.http import HttpResponseRedirect
from .models import Comment, Post


def index(request):
    featured_posts = Post.objects.all().order_by('-date')[:3]
    context = {
        'posts': featured_posts
    }
    return render(request, 'blog/index.html', context)


def posts(request):
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts
    }
    return render(request, 'blog/posts.html', context)


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
        'post_tags': post.tags.all(),
        'post_comments': post.comments.all().order_by('-id')
    }
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path)
        else:
            context['comment_form'] = comment_form
            return render(request, 'blog/post-detail.html', context)
    else:
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        return render(request, 'blog/post-detail.html', context)
