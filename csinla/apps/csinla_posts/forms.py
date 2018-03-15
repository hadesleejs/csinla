#_*_coding:utf-8_*_
from .models import *
from django import forms
from csinla_accounts.models import CustomizedCar
from django.core.exceptions import NON_FIELD_ERRORS

class CreatePictureForm(forms.Form):
    post = models.ForeignKey(Post)
    image = forms.ImageField(required=False)


class CreateRentForm(forms.ModelForm):

    class Meta:
        model = Rent
        fields = ['author','title', 'fee', 'district', 'share', 'house_type','rent_begins','room_type',
                  'contactor', 'content', 'phone', 'weixin', 'pet', 'smoke', 'parking','rent_ends',
                  'driving_time_toschool_hour', 'transit_time_toschool_hour','gender_require',
                  'address', 'district_other', 'house_type_other', 'room_type_other', 'expire_date',
                  'transit_time_toschool_minute', 'driving_time_toschool_minute']
    def __init__(self, *args, **kwargs):
        super(CreateRentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages={'required': u'必填项', 'invalid': u'无效数据', 'invalid_choice': u'无效的数据'}


class CreateEntireRentForm(forms.ModelForm):
    # 创建整租的帖子

    class Meta:
        model = EntireRent
        fields = ['author','title', 'fee', 'district', 'house_type','rent_begins',
                  'contactor', 'content', 'phone', 'weixin', 'pet', 'smoke', 'parking','rent_ends',
                  'driving_time_toschool_hour', 'transit_time_toschool_hour',
                  'address', 'district_other', 'house_type_other', 'room_type_other', 'expire_date',
                  'transit_time_toschool_minute', 'driving_time_toschool_minute','pak_nums']
    def __init__(self, *args, **kwargs):
        super(CreateEntireRentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages={'required': u'必填项', 'invalid': u'无效数据', 'invalid_choice': u'无效的数据'}


class CustomizedCarForm(forms.ModelForm):

    class Meta:
        model = CustomizedCar
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomizedCarForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages={'required': u'必填项', 'invalid': u'无效数据', 'invalid_choice': u'无效的数据'}


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['author', 'title', 'car_type', 'car_type_other', 'brand', 'vehicle_age', 'vehicle_miles', 'level_type',
                  'level_type_other', 'transmission_type', 'displacement', 'drive_type', 'inside_color',  
                  'outside_color','oil_type', 'turbo', 'vin_number', 'contactor', 'phone', 'weixin', 'fee2', 'contact_way',
                  'content', 'expire_date']

    def __init__(self, *args, **kwargs):
        super(CreateCarForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages={'required': u'必填项', 'invalid': u'无效数据', 'invalid_choice': u'无效的数据'}


class CarPictureForm(forms.Form):
    car = models.ForeignKey(Car)
    image = forms.ImageField(required=False)


class CreateShareForm(forms.ModelForm):
    class Meta:
        model = Rent2
        fields = ['title', 'house_id', 'fee', 'rent_begins', 'rent_ends', 'house_type', 'room_type', 'pet',
                  'smoke', 'parking', 'driving_time_toschool', 'transit_time_toschool', 'address', 'contactor',
                  'phone', 'weixin', 'gender_require', 'house_type_other', 'room_type_other', 'content']

    def __init__(self, *args, **kwargs):
        super(CreateShareForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages={'required': u'必填项', 'invalid': u'无效数据', 'invalid_choice': u'无效的数据'}


class InspectForm(forms.ModelForm):
    class Meta:
        model = CarInspection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InspectForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages={'required': u'必填项', 'invalid': u'无效数据', 'invalid_choice': u'无效的数据'}

class UsedForm(forms.ModelForm):
    class Meta:
        model = Used
        fields = '__all__'

class UsedGoodsForm(forms.ModelForm):
    class Meta:
        model = UsedGoods
        exclude = ['used_id','weixin','reply_num','post_date','phone','belong_to','expire_date','active','is_notice']

class CreateUsedGoodsForm(forms.ModelForm):
    class Meta:
        model = UsedGoods
        exclude = ['used_id','weixin','reply_num','post_date','phone','belong_to','expire_date','active','is_notice']

    def __init__(self, *args, **kwargs):
        super(CreateUsedGoodsForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required=False


class UsedBookForm(forms.ModelForm):
    class Meta:
        model = UsedBook
        exclude = ['book_id','weixin','reply_num','post_date','phone','belong_to','expire_date','active','is_notice']

class CreateUsedBookForm(forms.ModelForm):
    class Meta:
        model = UsedBook
        exclude = ['book_id','weixin','reply_num','post_date','phone','belong_to','expire_date','active','is_notice']


class CreateExposureForm(forms.ModelForm):
    class Meta:
        model = Exposure
        fields = ['title','content']

class CreatePostMessageForm(forms.ModelForm):
    class Meta:
        model = PostMessage
        exclude = ['',]


