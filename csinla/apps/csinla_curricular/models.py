# _*_ encoding: utf-8 _*_

from datetime import datetime
import django.utils.timezone as timezone

from django.db import models

from csinla_accounts.models import Profile


class Curricular(models.Model):
	year=models.IntegerField(u'YEAR',default=0)
	semester=models.CharField(u'Semester',max_length=64,default='')
	department=models.CharField(u'Department',max_length=64,default='')
	subject=models.CharField(u'Subject',max_length=64,default='')
	# course=models.CharField(u'Course',max_length=64,default='')
	instructor=models.CharField(u'Instructor',max_length=64,default='')
	sign_a=models.IntegerField('A',default=0)
	sign_b=models.IntegerField('B',default=0)
	sign_c=models.IntegerField('C',default=0)
	sign_d=models.IntegerField('D',default=0)
	sign_f=models.IntegerField('F',default=0)
	sign_ip=models.IntegerField('IP',default=0)
	sign_ix=models.IntegerField('IX',default=0)
	sign_np=models.IntegerField('NP',default=0)
	sign_p=models.IntegerField('P',default=0)
	sign_w=models.IntegerField('W',default=0)
	sign_rd=models.IntegerField('RD',default=0)
	sign_total=models.IntegerField('Total',default=0)

	@property
	def to_dict(self):
		return {
			'id': self.id,
			'year': self.year,
			'semester':self.semester,
			'department':self.department,
			'subject':self.subject,
			'instructor':self.instructor,
			'sign_a':self.sign_a,
			'sign_b':self.sign_b,
			'sign_c':self.sign_c,
			'sign_d':self.sign_d,
			'sign_f':self.sign_f,
			'sign_ip':self.sign_ip,
			'sign_ix':self.sign_ix,
			'sign_np':self.sign_np,
			'sign_p':self.sign_p,
			'sign_w':self.sign_w,
			'sign_rd':self.sign_rd,
			'sign_total':self.sign_total,
		}

		
class SearchRecord(models.Model):
	create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
	creator=models.ForeignKey(Profile,verbose_name=u'创建者')
	search_str=models.CharField(u'搜索条件',max_length=512,default='')
		
