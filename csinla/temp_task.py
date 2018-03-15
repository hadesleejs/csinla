# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csinla.settings")
    import django
    django.setup()
    import datetime
    import pytz
    import django.utils.timezone as timezone
    from csinla_posts.models import Post,PostMessage,Rentpicture
    from SSO.models import IPViewResult,ViewItem
    from django.utils.timezone import localtime

    rentpicture_list=Rentpicture.objects.filter(post__is_top=True,post__belong_to=u'二手车',post__expire_date__gte = timezone.now())
    for pic in rentpicture_list:
        print pic.id
        try:
            pic.save()
        except Exception as e:
            print e


    
    # for viewitem in ViewItem.objects.all():
    #     viewitem.save()
    # for ipviewresult in IPViewResult.objects.all():
    #     create_date=ipviewresult.create_date
    #     today_begin=datetime.datetime(create_date.year, create_date.month, create_date.day, 0, 0, 0, 0, tzinfo=pytz.timezone('America/Los_Angeles'))
    #     collect_list=PostMessage.objects.filter(message_type='COLLECT',post__belong_to=ipviewresult.view_type,create_time__range=(today_begin,today_begin+datetime.timedelta(days=1)))
    #     ipviewresult.collect_count=collect_list.count()
    #     print ipviewresult.collect_count
    #     ipviewresult.save()


    # for user in Profile.objects.filter(email__startswith='csinla_'):
    #     print user.email
    #     user.first_name=u'系统用户'
    #     user.save()
    # from django.contrib.auth.hashers import make_password
    # email='csinla_car@163.com'
    # username='csinla_car'
    # password=make_password('csinla_123')
    # school='csinla'
    # student_id='1's
    # phone='1'
    # join_ip='127.0.0.1'
    # Profile.objects.crea
    # for i in range(16,36):te(email=email,username=username,is_active=True,password=password,school=school,student_id=student_id,phone=phone,join_ip=join_ip)

    #     email='csinla_%s@163.com' % i
    #     username='csinla_%s' % i
    #     password=make_password('csinla_123')
    #     school='csinla'
    #     student_id=str(i)
    #     phone=str(i)
    #     join_ip='127.0.0.1'
    #     Profile.objects.create(email=email,username=username,is_active=True,password=password,school=school,student_id=student_id,phone=phone,join_ip=join_ip)
        
    # from operations.models import UserFavorite
    # from django_comments.models import Comment
    # from csinla_posts.models import PostMessage,Post
    # for favorite in UserFavorite.objects.all():
    #     try:
    #         postmessage=PostMessage.objects.get(message_type='COLLECT',post_id=favorite.fav_id,creator=favorite.user)
    #         if not postmessage.is_valid:
    #             postmessage.is_valid=True
    #             postmessage.save()
    #     except PostMessage.DoesNotExist:
    #         try:
    #             post=Post.objects.get(id=favorite.fav_id)
    #             PostMessage.objects.create(message_type='COLLECT',post=post,creator=favorite.user)
    #         except Post.DoesNotExist:
    #             print u'id为【%s】的post不存在' % favorite.fav_id

    # for comment in Comment.objects.all():
    #     try:
    #         postmessage=PostMessage.objects.get(message_type='REPLY',post_id=comment.object_pk,creator_id=comment.user_id,content_text=comment.comment)
    #         if not postmessage.is_valid:
    #             postmessage.is_valid=True
    #             postmessage.save() 
    #     except PostMessage.DoesNotExist:
    #         try:
    #             post=Post.objects.get(id=comment.object_pk)
    #             PostMessage.objects.create(message_type='REPLY',post_id=comment.object_pk,creator_id=comment.user_id,content_text=comment.comment)
    #         except Post.DoesNotExist:
    #             print u'id为【%s】的post不存在' % favorite.fav_id

    # import csv
    # from csinla_curricular.models import Curricular
    # for curricular in Curricular.objects.all():
    #     subject=curricular.subject
    #     subject=' '.join(subject.split())
    #     curricular.subject=subject
    #     curricular.save()
        
    # change_array=[
    #     {
    #         'real_name':'Earth Science',
    #         'wrong_array':['ASTRON','GEOG'],
    #     },
    #     {
    #         'real_name':'Communication',
    #         'wrong_array':['Communicatio','FILM'],
    #     },
    #     {
    #         'real_name':'Computer Science and Information Systems',
    #         'wrong_array':['Computer Scie','Computer Science and InformationSystems'],
    #     },
    #     {
    #         'real_name':'Design Technology',
    #         'wrong_array':['Design Techno',],
    #     },
    #     {
    #         'real_name':'Disabled Students Center',
    #         'wrong_array':['Disabled Stud',],
    #     },
    #     {
    #         'real_name':'Health Sciences',
    #         'wrong_array':['Health Science'],
    #     },
    #     {
    #         'real_name':'Philosophy and Social Sciences',
    #         'wrong_array':['Philosophy an','Philosophy andSocial Sciences'],
    #     },
    #     {
    #         'real_name':'Modern Languages and Cultures',
    #         'wrong_array':['Modern Langu'],
    #     },
    #     {
    #         'real_name':'Photography and Fashion',
    #         'wrong_array':['Photography a'],
    #     },
    #     {
    #         'real_name':'Physical Science',
    #         'wrong_array':['Physical Scienc','physical Science'],
    #     },
    #     {
    #         'real_name':'Kinesiology',
    #         'wrong_array':['KIN PE'],
    #     },
    # ]
    # for change_item in change_array:
    #     Curricular.objects.filter(department__in=change_item['wrong_array']).update(department=change_item['real_name'])
    

