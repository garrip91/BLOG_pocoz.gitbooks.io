from django.shortcuts import render, get_object_or_404

from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from .forms import EmailPostForm


# Create your views here.
# def post_list(request):
    # # posts = Post.objects.all()
    # object_list = Post.objects.all()
    # paginator = Paginator(object_list, 3) # по 3 поста на каждой странице
    # page = request.GET.get('page')
    # try:
        # posts = paginator.page(page)
    # except PageNotAnInteger:
        # posts = paginator.page(1)
    # except EmptyPage:
        # posts = paginator.page(paginator.num_pages)
    # return render(request,
                  # 'blog/post/list.html',
                  # {'page': page,
                  # 'posts': posts})
class PostListView(ListView):
    
    # queryset = Post.objects.all()
    # context_object_name = 'posts'
    # paginate_by = 3
    # template_name = 'blog/post/list.html'
    model = Post
    context_object_name = 'object_list'
    template_name = 'blog/post/list.html'
    paginate_by = 3
    
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
    
    
def post_share(request, post_id):
    # Получаем пост по id:
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # Форма была отправлена...
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы прошли проверку...
            cd = form.cleaned_data
            # ...отправить письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})