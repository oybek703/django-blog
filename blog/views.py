from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from django.http import HttpResponseRedirect
from .models import Post
from django.urls import reverse


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
        stored_posts = request.session.get('stored_posts') or []
        context['comment_form'] = comment_form
        context['is_saved_for_later'] = post.id in stored_posts
        return render(request, 'blog/post-detail.html', context)


def read_later(request):
    if request.method == 'GET':
        stored_posts = request.session.get('stored_posts')
        if stored_posts is None or len(stored_posts) == 0:
            stored_posts = []
        stored_posts = Post.objects.filter(id__in=stored_posts)
        context = {
            'posts': stored_posts,
            'has_posts': len(stored_posts) != 0
        }
        return render(request, 'blog/stored-posts.html', context)
    else:
        stored_posts = request.session.get('stored_posts')
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST['post_id'])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session['stored_posts'] = stored_posts
        return HttpResponseRedirect(reverse('index'))
