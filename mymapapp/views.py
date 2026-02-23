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


    if request.method == 'POST' and form.is_valid():#POSTがきたとき
        if request.POST.get('map_url', False):#map_urlがあるとき要件チェック、マップ作製
            iframe_code = request.POST['map_url']

            pattern1 = r'<iframe src="(.*?)"'
            match = re.search(pattern1, iframe_code)
            if match:
                url = match.group(1)
            else:
                html = loader.render_to_string('error.html')
                return HttpResponse(html)

            pattern2 = r'https://www\.google\.com/maps/(.*?)embed\?mid'
            pattern3 = r'embed\?mid=(.*?)&ehbc='
            pattern4 = r'&ehbc=(.*?)$'
            match2 = re.search(pattern2, url)
            match3 = re.search(pattern3, url)
            match4 = re.search(pattern4, url)

            #不正がないかチェック
            if '<' in match2.group(1) or '>' in match2.group(1) or ' ' in match2.group(1) or '\\' in match2.group(1):
                html = loader.render_to_string('error.html')
                return HttpResponse(html)
            if '<' in match3.group(1) or '>' in match3.group(1) or ' ' in match3.group(1) or '\\' in match3.group(1):
                html = loader.render_to_string('error.html')
                return HttpResponse(html)
            if '<' in match4.group(1) or '>' in match4.group(1) or ' ' in match4.group(1) or '\\' in match4.group(1):
                html = loader.render_to_string('error.html')
                return HttpResponse(html)

            #MAP作成
            map = models.Map.objects.create()

            if match2:
                map.id1 = match2.group(1)
            if match3:
                map.id2 = match3.group(1)
            if match4:
                map.id3 = match4.group(1)
        else:
            map = models.Map.objects.create()
            map.id1 = 'd/u/0/'
            map.id2 = '1mduMhKdecqOZ05N6Rc9v-eQoCz_ndx8'
            map.id3 = '2E312F'



        #オブジェクト作成、保存、マップ保存
        object = form.save()
        object.member.add(request.user)
        if request.FILES.get('icon_image',False): object.icon_image= request.FILES['icon_image']
        object.save()
        map.site = models.Site.objects.get(id=object.id)
        map.save()

        #ページ移動
        html = loader.render_to_string('create_success.html')
        return HttpResponse(html)
    

    context = {
        'form':form
    }
    return render(request, 'site_create.html', context)


@login_required
def site_update(request, sitepk):
    site = models.Site.objects.get(pk=sitepk)
    map = None
    form = forms.SiteCreateForm(request.POST or None, instance=site)


    if request.method == 'POST' and form.is_valid():#POSTがきたとき
        if request.POST.get('map_url', False):#map_urlがあるとき要件チェック、マップ作製
            iframe_code = request.POST['map_url']

            pattern1 = r'<iframe src="(.*?)"'
            match = re.search(pattern1, iframe_code)
            if match:
                url = match.group(1)
            else:
                html = loader.render_to_string('error.html')
                return HttpResponse(html)

            pattern2 = r'https://www\.google\.com/maps/(.*?)embed\?mid'
            pattern3 = r'embed\?mid=(.*?)&ehbc='
            pattern4 = r'&ehbc=(.*?)$'
            match2 = re.search(pattern2, url)
            match3 = re.search(pattern3, url)
            match4 = re.search(pattern4, url)

            #不正がないかチェック
            if '<' in match2.group(1) or '>' in match2.group(1) or ' ' in match2.group(1) or '\\' in match2.group(1):
                html = loader.render_to_string('error.html')
                return HttpResponse(html)
            if '<' in match3.group(1) or '>' in match3.group(1) or ' ' in match3.group(1) or '\\' in match3.group(1):
                html = loader.render_to_string('error.html')
                return HttpResponse(html)
            if '<' in match4.group(1) or '>' in match4.group(1) or ' ' in match4.group(1) or '\\' in match4.group(1):
                html = loader.render_to_string('error.html')
                return HttpResponse(html)

            #MAP作成
            if site.s_to_m.all():
                map = site.s_to_m.all()[0]
            else:
                map = models.Map.objects.create()

            if match2:
                map.id1 = match2.group(1)
            if match3:
                map.id2 = match3.group(1)
            if match4:
                map.id3 = match4.group(1)
        else:
            if site.s_to_m.all():
                map = site.s_to_m.all()[0]
                map.id1 = 'd/u/0/'
                map.id2 = '1mduMhKdecqOZ05N6Rc9v-eQoCz_ndx8'
                map.id3 = '2E312F'

        #オブジェクト作成、保存、マップ保存
        object = form.save()
        if request.FILES.get('icon_image',False): object.icon_image= request.FILES['icon_image']
        object.save()
        if map:
            map.site = models.Site.objects.get(id=object.id)
            map.save()

        #ページ移動
        html = loader.render_to_string('create_success.html')
        return HttpResponse(html)


    #サイト作成ページへ
    context = {
        'form': form,
        'sitepk':sitepk,
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
        if request.method == 'POST' and form.is_valid:
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
        if request.method == 'POST' and form.is_valid:
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
    