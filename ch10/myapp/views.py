from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapp import form, models
from django.http import HttpResponse

# Create your views here.


def home(request):
    
    if request.user.is_authenticated: # 這裡注意user是request自帶的方法，request.user適用於驗證使用者是否登入的機制，我猜auth.login(request, user2)
                                      # 成功後會去request.user設置現在登入的使用者
        username = request.user.username
    messages.get_messages(request)
    
    # 分頁
    all_polls = models.Poll.objects.all().order_by('created_at')
    paginator = Paginator(all_polls, 2)  # 2個項目一分頁，type大概是list型態吧 ，[ [obj1，obj2], .... ] (我猜)
    p = request.GET.get('p') # 再分頁中網址會有 ?p=2，代表這是分頁2的物件，這個網址是由 paginator = Paginator(all_polls, 2)自動產生的
    try:
        polls = paginator.page(p) # 取得分頁物件
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)
    
    return render(request, 'Home.html', locals())


'''
def index(request):
    all_polls = models.Poll.objects.all().order_by('-created_at')
    paginator = Paginator(all_polls, 5) # 5個一分頁
    p = request.GET.get('p')
    try:
        polls = paginator.page(p)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page
    return render(request, 'Home.html', locals())
'''

def login(request):
    if request.method == 'POST':
        login_form = form.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip() # 這個username是因為form.login_form裡ID的變數叫username
            login_password = request.POST['password']
            user2 = auth.authenticate(username=login_name, password=login_password) # 和資料庫驗證，這裡的username、password是Django User的自備屬性
            if user2 is not None:
               if user2.is_active:
                   auth.login(request, user2) # 把user這個物件存進seesion
                   messages.add_message(request, messages.SUCCESS, '登入成功')
                   return redirect('/home')
               else:
                   messages.add_message(request, messages.WARNING, '帳號尚未激活')
            else:
                messages.add_message(request, messages.WARNING, '登入失敗')
        else:
            messages.add_message(request, messages.INFO, '輸入有問題')
    else:
        login_form = form.LoginForm()
    return render(request, 'login.html', locals())

@login_required(login_url='/login/')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.add_message(request, messages.INFO, '登出了')
    return redirect('/home')

@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username # 從session取得username
    user = auth.models.User.objects.get(username=username) #存資料庫取得username的資訊
    try:
        profile = models.Profile.objects.get(user=user)
    except:
        profile = models.Profile(user=user)

    if request.method == 'POST':
        profile_form = form.ProfileForm(request.POST, instance=profile) # instance作為收尋的關鍵字
        if profile_form.is_valid():
            messages.add_message(request, messages.INFO, '資料已儲存')
            profile_form.save()
            return redirect('/userinfo')
        else:
            messages.add_message(request, messages.INFO, '表格有誤')
    else:
        profile_form = form.ProfileForm()
    return render(request, 'userinfo.html', locals())

@login_required(login_url='/login/')
def vote_item(request): # 顯示所有投票項目
    try:
        username = request.user.username
        issues = models.Poll.objects.all()
    except :
        pass
    return render(request, 'vote_item.html', locals())

@login_required(login_url='/login/')
def voting(request, poll_id=None, item_id=None):
    try:
        username = request.user.username
        issue = models.Poll.objects.get(id=poll_id)
        items = models.Poll_item.objects.filter(poll=issue).order_by('-vote_number')
        if item_id is not None:
            pollitem = models.Poll_item.objects.get(poll=issue, id=item_id)
            pollitem.vote_number = pollitem.vote_number + 1
            pollitem.save()
    except:
        pass
    return render(request, 'voting.html', locals())

@login_required(login_url='/login/')
def govote(request):
    if request.method == 'GET' and request.is_ajax():
        pollitemid = request.GET.get('pollitemid') # request.GET是取得URL並把它存成網址，get(key)回傳value
        try:
            pollitem = models.Poll_item.objects.get(id=pollitemid)
            pollitem.vote_number = pollitem.vote_number + 1
            pollitem.save()
            votes = pollitem.vote_number
        except:
            votes = 0
    else:
        votes = 0
    return HttpResponse(votes)            

def test(request):
    return render(request, 'listen_test.html', locals())


















