from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # 템플릿은 모델명_list.html 이 자동  생성
    # 매개변수 모델명_list : post_list
class PostDetail(DetailView):
    model = Post
    # 템플릿은 모델명_detail.html 이 자동  생성
    # 매개변수 모델명 : post

#def index(request):
#    posts = Post.objects.all().order_by('-pk')
#
#    return render(request, 'blog/index.html', {'posts': posts})

#def single_post_page(request, pk):
#    post = Post.objects.get(pk=pk)
#    return render(request, 'blog/single_post_page.html', {'post': post})