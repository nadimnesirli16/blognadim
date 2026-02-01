from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q 
from .models import Category, Post, Author, Comment, PostLike
from django.contrib.auth.decorators import login_required #bunu elave etmisen setr kimi

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:9]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:9]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post=get_object_or_404(Post,slug=slug)
    post = Post.objects.get(slug = slug)
    post.views_count +=1
    post.save()
    post.save(update_fields=['views_count'])
    latest = Post.objects.order_by('-timestamp')[:9]
    comments=post.comments.filter(active=True)
    if request.method == 'POST':
        if request.user.is_authenticated:
            content=request.POST.get('content')
            if content:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    content=content,
                )
                return redirect(request.path) #bunuda elave etdik
    context = {
        'post': post,
        'latest': latest,
        'comments': comments #elave eledik
    }
    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)
#like
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = PostLike.objects.get_or_create(user=request.user, post=post )

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))



