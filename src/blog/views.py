from django.shortcuts import render, get_object_or_404

from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from .forms import EmailPostForm

from django.core.mail import send_mail


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
    sent = False
    if request.method == 'POST':
        # Форма была отправлена...
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы прошли проверку...
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url)
            subject = '{} ({}) recommends you reading " {}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'garrip91@yandex.ru', [cd['to']])
            sent = True
            # ...отправить письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})