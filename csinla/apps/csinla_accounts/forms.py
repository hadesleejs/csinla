# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from .models import *
from django import forms
from captcha.fields import CaptchaField
from csinla_posts.models import Post


class UserForm(forms.ModelForm):

    password2 = forms.CharField(
        required = True,
        label = u"确认密码",
        error_messages = {'required': u'请再输入密码'},
        widget = forms.PasswordInput(
            attrs = {
                'placeholder':u"确认密码",
            }
        ),
    )

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError(u"两次输入的密码不一样")      
        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'password','is_active']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': '请输入用户名'}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': '输入邮箱地址'}
            ),
            'password': forms.PasswordInput(
                attrs={'placeholder': '请输入密码'}
            ),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        # exclude = ['user']
        # widgets = {'reg_type': forms.HiddenInput()}
        fields = ['self_intro', 'school']
        
        widgets = {
            'school': forms.TextInput(
                attrs={'initial': 'None', 'required': False, 'placeholder': '请输入所在学校'}
            ),

            'self_intro': forms.TextInput(
                attrs={'placeholder': '介绍一下您的公司吧'}
            ),
        }

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class ResetForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class EmailResetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})

    def clean(self):
        cleaned_data = super(EmailResetForm, self).clean()
        email = cleaned_data.get("email")

        is_email_exist = Profile.objects.filter(email=email).exists()

        if not is_email_exist:  
            self.add_error('email', u"邮件未注册!")


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=15)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    repeat_password = forms.CharField(required=True, min_length=5)
    school = forms.CharField(required=True)
    student_id = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        phone = cleaned_data.get("phone")

        is_email_exist = Profile.objects.filter(email=email).exists()
        is_name_exist = Profile.objects.filter(username=username).exists()

        if is_email_exist:  
            self.add_error('email', u"该邮件已被注册, 请重新注册")
        if is_name_exist:
            self.add_error('username', u"此用户名已占用")
        if password != repeat_password:
            self.add_error('repeat_password', u"密码不一致, 请重新注册")
        try:
            int(phone)
        except:
            self.add_error('phone', u"请输入数字")
     

class FuncFeedbackFrom(forms.ModelForm):

    class Meta:
        model = FuncFeedback
        fields = '__all__'


class AccountFeedbackFrom(forms.ModelForm):

    class Meta:
        model = AccountFeedback
        fields = '__all__'


class ExperFeedbackFrom(forms.ModelForm):

    class Meta:
        model = ExperFeedback
        fields = '__all__'


class OtherFeedbackFrom(forms.ModelForm):

    class Meta:
        model = OtherFeedback
        fields = '__all__'


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['username', 'weixin', 'gender', 'birth_date', 'phone', 'student_id', 'school']


class CreateContactInfoForm(forms.ModelForm):
    """docstring for CreateContactInfoForm"""
    class Meta:
        model = ContactInfo
        fields = ['email', 'message']    

class CreateCarfaxForm(forms.ModelForm):
    """docstring for CreateContactInfoForm"""
    class Meta:
        model = Carfax
        fields = ['vin', 'name','email','wechat']    


class ApplyPickupForm(forms.ModelForm):
    # 新生接机申请资料
    class Meta:
        model = ApplyForPickup
        fields = ['name','sex','wx','phone','major','email','baggage','flight'
            ,'departure','departure_type','landing','landing_type','address',
                  'img2','contactor','contacts_phone','remark','img1','belong']


class CommentForm(forms.ModelForm):
    # 新生评论
    class Meta:
        model = NewStudentComment
        fields = ['comments']


class NewStudentSubmissionForm(forms.ModelForm):
    # 新生投稿
    class Meta:
        model = NewStudentSubmission
        fields = ['title','content','url']


class UserFeedbackForm(forms.ModelForm):
    """
    用户反馈
    """
    class Meta:
        model = Feedback
        fields = ['title','phone','content','content_detail']


class UserCenterInfoForm(forms.ModelForm):
    """
	账户安全修改资料
	"""

    class Meta:
        model = Profile
        fields = ['username', 'school', 'student_id','gender','weixin','phone']
