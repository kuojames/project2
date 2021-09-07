from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from myapp import models, forms

# Create your views here.

# CBV
class PostListView(ListView): 
    queryset = models.Post.published.all()
    context_object_name = 'posts' # 把查詢的結果命名為posts，默認是object_list
    paginate_by = 3
    template_name = 'blog/post/list.html'


# FBV
def post_list(request, tag_slug=None):
    object_list = models.Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page') # 因為在pagination.html中寫了?page=...所以page變成傳遞參數
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)        
    return render(request, 'blog/post/list.html', locals())

def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, 
                                slug=post, status='published', 
                                publish__year=year, 
                                publish__month=month, 
                                publish__day=day)
    post_tags_id = post.tags.values_list('id', flat=True) # 取得該篇post所有的tag
    similar_posts = models.Post.published.filter(tags__in=post_tags_id).exclude(id=post.id) # 取得所有相關tag的發文，但不含本篇
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # similar_posts.annotate(same_tags=Count('tags')) 意思是: 讓有相關的post計算自己自身的tag，假設A本身有4個tags那A的same_tags=4
    # 之後再和tags數、publish排順序

    comments = post.comments.filter(activate=True) #post.comments.filter(activte=True) = models.Comment.objects.filter(post=post, activate=True)                            
    new_comment = None # 這是新留言的，comments是之前的留言
    if request.method == 'POST':
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = forms.CommentForm()

    return render(request, 'blog/post/detail.html', locals())

def post_share(request, post_id):
    post = get_object_or_404(models.Post, id=post_id, status='published') # 有去向資料庫要資料
    sent = False
    if request.method == 'POST':
        form = forms.EmailPostFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data # 取出資料 資料以字典儲存
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} ， {cd['name']} comments: {cd['comments']}"
            send_mail(subject, message, 's1071531@gm.pu.edu.tw', [cd['to']])
            sent = True
    else:
        form = forms.EmailPostFrom()
    return render(request, 'blog/post/share.html', locals())

def post_search(request):
    form = forms.SearchForm()
    query = None
    results = []
    if 'query' in request.GET: # query會在Http的報文是因為forms.py定義查詢欄較query
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = models.Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
            # 查詢文章title，body的column，這兩個是自訂義 
    return render(request, 'blog/post/search.html', locals())
    # ?query=查詢資料，所以查詢後網址的變化，(查詢資料)就是輸入的資料      
