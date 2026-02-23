from django.db import models
from django.conf import settings

class Site(models.Model):
        title = models.CharField('タイトル', max_length=32)
        explanation = models.TextField('文',blank=True, null=True)
        map_url = models.TextField('MAPソースコード',blank=True, null=True)
        member = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True)
        created_at = models.DateTimeField('作成日', auto_now=True)
        icon_image = models.ImageField('アイコン画像' ,blank=True, null=True)



        def get_contents(self):
                content_list = self.s_to_c.all()
                if(content_list.count() <=0 ):
                        return []
                content_order_list = []#正しい順番通りにコンテンツが入ったリスト
                a_content = content_list[0]#とりあえず一つ持ってくる
                content_order_list.append(a_content)
                preNum = a_content.pre_number
                nextNum = a_content.next_number

                safeflag = 0
                while not preNum is None:
                        safeflag += 1
                        pre_content = Content.objects.get(pk=preNum)
                        content_order_list.insert(0, pre_content)
                        preNum = pre_content.pre_number
                        if safeflag>100:
                                break
                safeflag = 0
                while not nextNum is None:
                        safeflag += 1
                        next_content = Content.objects.get(pk=nextNum)
                        content_order_list.append( next_content)
                        nextNum = next_content.next_number
                        if safeflag>100:
                                break
                
                return content_order_list



        def get_member(self):
                pass

        def delete_member(self, pk):
                pass

        def __str__(self):
                return self.title
        

class Map(models.Model):
        site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True,verbose_name='saito',unique=True, related_name='s_to_m')
        id1 = models.CharField('id1', max_length=100,blank=True, null=True)
        id2 = models.CharField('id1', max_length=100,blank=True, null=True)
        id3 = models.CharField('id1', max_length=100,blank=True, null=True)

        def __str__(self):
                return self.site



class Content(models.Model):
        site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True,verbose_name='saito', related_name='s_to_c')

        genre_number =  models.IntegerField('ジャンル番号',blank=True, null=True)
        ver =  models.IntegerField('バージョン番号',blank=True, null=True, default=0)

        title = models.CharField('タイトル', blank=True, null=True, max_length=34)

        text1 = models.TextField('文1',blank=True, null=True)
        text2 = models.TextField('文2',blank=True, null=True)
        text3 = models.TextField('文3',blank=True, null=True)
        text4 = models.TextField('文4',blank=True, null=True)


        pre_number = models.IntegerField('前に置かれるコンテンツ番号',blank=True, null=True, default=None)
        next_number = models.IntegerField('後ろに置かれるコンテンツ番号',blank=True, null=True, default=None)
        created_at = models.DateTimeField('作成日', auto_now=True)



        def insert(self, num):
                focus_content = Content.objects.get(pk=num)
                self.pre_number = focus_content.pre_number
                self.next_number = num
                focus_content.pre_number = self.pk
                focus_content.save()
                self.save()

        def add(self):
                content_list = self.site.s_to_c.all().difference(Content.objects.filter(pk=self.pk))
                if(content_list.count() <=0 ):
                        self.pre_number = None
                        self.prnext_number = None
                        self.save()
                        return []

                content_order_list = []#正しい順番通りにコンテンツが入ったリスト
                a_content = content_list[0]#とりあえず一つ持ってくる
                content_order_list.append(a_content)
                preNum = a_content.pre_number
                nextNum = a_content.next_number

                safeflag = 0
                while not preNum is None:
                        safeflag += 1
                        pre_content = Content.objects.get(pk=preNum)
                        content_order_list.insert(0, pre_content)
                        preNum = pre_content.pre_number
                        if safeflag>1000:
                                break
                safeflag = 0
                while not nextNum is None:
                        safeflag += 1
                        next_content = Content.objects.get(pk=nextNum)
                        content_order_list.append( next_content)
                        nextNum = next_content.next_number
                        if safeflag>1000:
                                break

                focus_content = content_order_list[-1]
                focus_content.next_number = self.pk
                self.pre_number = focus_content.pk
                focus_content.save()
                self.save()

        def delete_from_list(self, contentpk):
                focus_content = Content.objects.get(pk=contentpk)
                pre_pk = focus_content.pre_number
                next_pk = focus_content.next_number

                if not pre_pk is None:#pre_pkがあったら
                        pre_content = Content.objects.get(pk=pre_pk)
                        pre_content.next_number = focus_content.next_number
                        pre_content.save()
                if not next_pk is None:#next_pkがあったら
                        next_content = Content.objects.get(pk=next_pk)
                        next_content.pre_number = focus_content.pre_number
                        next_content.save()
                focus_content.delete()



        def get_site_url(self):
                pass


        def get_article_url(self):
                pass

        def __str__(self):
                return self.site.title


class LiketoSite(models.Model):
        site = models.ManyToManyField(Site, blank=True, null=True,verbose_name='saito',related_name='s_to_like')
        user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, blank=True, unique=True, related_name='u_to_like')












