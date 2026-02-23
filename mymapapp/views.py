from django.shortcuts import render, redirect
from django.db.models import Q
from . import models
from . import forms
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import re






def site_list(request):
    q_word = request.GET.get('query')
 
    if q_word:#検索したらタイトルと説明に検索ワードが含まれているか調べ合致したものを出力する
        queryset = models.Site.objects.filter(Q(title__icontains=q_word) | Q(explanation__icontains=q_word))
        queryset =queryset.order_by('-created_at')[:30]
        top = False
    else:#そうでなかったら普通に出力
        queryset = models.Site.objects.order_by('-created_at')[:4]
        #queryset = models.Site.objects.annotate(num_like=Count('l_liked_u')).order_by('-num_like')[:6]
        top = True


    context = {
        'top':top,
        'site_list':queryset,
        
    }
    return render(request,  'site_list.html', context)




@login_required
def site_create(request):
    map = None
    form = forms.SiteCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        
        # ユーザー入力を取得
        map_input = request.POST.get('map_url', '')

        if map_input:
            # 事実に基づく詳細: Google My MapsのマップID(mid)は、英数字、ハイフン、アンダースコアで構成されます。
            # iframeタグ全体が入力されても、URLだけが入力されても、midの値だけを厳密に抽出します。
            match = re.search(r'mid=([a-zA-Z0-9_-]+)', map_input)
            
            if match:
                mid_value = match.group(1)
            else:
                # midが見つからない、または不正な文字が含まれている場合はエラー
                html = loader.render_to_string('error.html')
                return HttpResponse(html)

            # MAPオブジェクトの作成
            map = models.Map.objects.create()
            
            # 既存のモデル構造に合わせる場合、id2にmidを保存すると推測します。
            # id1やid3は固定のパス情報を保持しているだけなので、固定値で問題ありません。
            map.id1 = 'd/u/0/'
            map.id2 = mid_value  # 抽出した安全なIDのみを保存
            map.id3 = '2E312F'
            
        else:
            # 入力がなかった場合のデフォルト処理
            map = models.Map.objects.create()
            map.id1 = 'd/u/0/'
            map.id2 = '1mduMhKdecqOZ05N6Rc9v-eQoCz_ndx8'
            map.id3 = '2E312F'

        # オブジェクト作成、保存、マップ保存
        object = form.save()
        object.member.add(request.user)
        if request.FILES.get('icon_image', False): 
            object.icon_image = request.FILES['icon_image']
        object.save()
        
        map.site = models.Site.objects.get(id=object.id)
        map.save()

        html = loader.render_to_string('create_success.html')
        return HttpResponse(html)

    context = {
        'form':form
    }
    return render(request, 'site_create.html', context)



import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from . import models
from . import forms

@login_required
def site_update(request, sitepk):
    # 対象のSiteオブジェクトを取得
    site = models.Site.objects.get(pk=sitepk)
    map = None
    form = forms.SiteCreateForm(request.POST or None, instance=site)

    if request.method == 'POST' and form.is_valid():
        map_input = request.POST.get('map_url', '')

        if map_input:
            # 入力文字列から「mid=」に続く安全な文字（英数字、ハイフン、アンダースコア）のみを抽出
            match = re.search(r'mid=([a-zA-Z0-9_-]+)', map_input)
            
            if match:
                mid_value = match.group(1)
            else:
                # 抽出できない、または不正な形式の場合はエラーを返す
                html = loader.render_to_string('error.html')
                return HttpResponse(html)

            # 既存のMAPオブジェクトがあれば取得、なければ新規作成
            if site.s_to_m.all():
                map = site.s_to_m.all()[0]
            else:
                map = models.Map.objects.create()

            # 抽出したmidを保存し、前後のIDは固定値を設定
            map.id1 = 'd/u/0/'
            map.id2 = mid_value
            map.id3 = '2E312F'
            
        else:
            # map_urlの入力がなかった場合、既存のマップがあればデフォルト値にリセットする
            if site.s_to_m.all():
                map = site.s_to_m.all()[0]
                map.id1 = 'd/u/0/'
                map.id2 = '1mduMhKdecqOZ05N6Rc9v-eQoCz_ndx8'
                map.id3 = '2E312F'

        # オブジェクトの更新内容を保存
        object = form.save()
        if request.FILES.get('icon_image', False): 
            object.icon_image = request.FILES['icon_image']
        object.save()
        
        # mapが存在する場合、Siteと紐付けて保存
        if map:
            map.site = models.Site.objects.get(id=object.id)
            map.save()

        # 成功ページへ遷移
        html = loader.render_to_string('create_success.html')
        return HttpResponse(html)

    # サイト更新ページを出力（GETリクエスト時など）
    context = {
        'form': form,
        'sitepk': sitepk,
    }
    return render(request, 'site_update.html', context)








@login_required
def site_delete(request, sitepk):
    site = models.Site.objects.get(pk=sitepk)

    if request.method == 'POST':
        site.delete()
        return redirect('main_app:site_list')

    context = {
        'site':site,
    }
    return render(request, 'site_delete.html', context)





def site_detail(request, sitepk):
    
    site = models.Site.objects.get(pk=sitepk)
    if site.s_to_m.all():
        map = site.s_to_m.all()[0]
    else:
        map = False
    
    if request.user.u_to_like.all():
        like_flag = True if site in request.user.u_to_like.all()[0].site.all() else False
    else:
        like_flag = False
    
    print(like_flag)

    context = {
        'like_flag':like_flag,
        'sitepk':sitepk,
        'site':site,
        'map':map,
    }
    return render(request, 'site_detail.html', context)





@login_required
def content_create(request, sitepk, genreNum, insertNum):
    site=models.Site.objects.get(pk=sitepk)

    if(genreNum==0):
        form = forms.ContentCreateForm0(request.POST or None)
    elif(genreNum==1):
        form = forms.ContentCreateForm1(request.POST or None)
    elif(genreNum==2):
        form = forms.ContentCreateForm2(request.POST or None)
    else:
        print('error!!')

    if(genreNum==0 or genreNum==1 or genreNum==2):
        if request.method == 'POST' and form.is_valid():
            content = form.save()
            content.site = site
            content.genre_number = genreNum
            content.save()
            content.insert(insertNum) 
        
            html = loader.render_to_string('create_success.html')
            return HttpResponse(html)

    else:
        print('error!!')


    context = {
        'form':form,
    }
    
    return render(request, 'content_create.html', context)







@login_required
def lastcontent_create(request, sitepk, genreNum):
    site=models.Site.objects.get(pk=sitepk)

    if(genreNum==0):
        form = forms.ContentCreateForm0(request.POST or None)
    elif(genreNum==1):
        form = forms.ContentCreateForm1(request.POST or None)
    elif(genreNum==2):
        form = forms.ContentCreateForm2(request.POST or None)
    else:
        print('error!!')

    if(genreNum==0 or genreNum==1 or genreNum==2):
        if request.method == 'POST' and form.is_valid:
            content = form.save()
            content.site = site
            content.genre_number = genreNum
            content.save()
            content.add() 
        
            html = loader.render_to_string('create_success.html')
            return HttpResponse(html)
    
    else:
        print('error!!')


    context = {
        'form':form,
    }
    
    return render(request, 'content_create.html', context)





@login_required
def content_delete(request, contentpk):
    content = models.Content.objects.get(pk=contentpk)

    if request.method == 'POST':
        content.delete_from_list(contentpk)
        html = loader.render_to_string('historyback3.html')
        return HttpResponse(html)

    context = {
        'content':content,
    }
    return render(request, 'site_delete.html', context)





@login_required
def content_update(request, contentpk, genreNum):
    content=models.Content.objects.get(pk=contentpk)

    if(genreNum==0):
        form = forms.ContentCreateForm0(request.POST or None, instance=content)
    elif(genreNum==1):
        form = forms.ContentCreateForm1(request.POST or None, instance=content)
    elif(genreNum==2):
        form = forms.ContentCreateForm2(request.POST or None, instance=content)
    else:
        print('error!!')

    if(genreNum==0 or genreNum==1 or genreNum==2):
        if request.method == 'POST' and form.is_valid():
            content = form.save()
            content.save()
        
            html = loader.render_to_string('create_success.html')
            return HttpResponse(html)
    
    else:
        print('error!!')


    context = {
        'form':form,
        'content':content,
    }
    
    return render(request, 'content_update.html', context)






@login_required
def userdetail(request):
    user = request.user
    q_word = request.GET.get('query')
 
    if q_word:#検索したらタイトルと説明に検索ワードが含まれているか調べ合致したものを出力する
        site_list = models.Site.objects.filter(Q(title__icontains=q_word) | Q(explanation__icontains=q_word))
        site_list = site_list.filter(member=user)
        site_list = site_list.order_by('-created_at')[:8]
        if models.LiketoSite.objects.filter(user=user):
            liked_list = models.LiketoSite.objects.filter(user=user)[0].site.all()
            liked_list = liked_list.filter(Q(title__icontains=q_word) | Q(explanation__icontains=q_word))
            liked_list = liked_list.order_by('-created_at')[:8]
        else:
            liked_list = None
    else:#そうでなかったら普通に出力
        site_list = models.Site.objects.filter(member=user)
        site_list = site_list.order_by('-created_at')[:8]
        if models.LiketoSite.objects.filter(user=user):
            liked_list = models.LiketoSite.objects.filter(user=user)[0].site.all()
            liked_list = liked_list.order_by('-created_at')[:8]
        else:
            liked_list = None

    context = {
        'site_list': site_list,
        'liked_list': liked_list,
    }
    return render(request, 'user_detail.html', context)








@login_required
def liketosite(request, sitepk):
    user = request.user
    site = models.Site.objects.get(pk=sitepk)
    if not models.LiketoSite.objects.filter(user=user):
        like_to_site = models.LiketoSite.objects.create(user=user)
    else:
        like_to_site = models.LiketoSite.objects.get(user=user)
    
    if site in like_to_site.site.all():
        like_to_site.site.remove(site)
    else:
        like_to_site.site.add(site)
    return render(request, 'like_success.html')




def func(request):
    print(123)
    