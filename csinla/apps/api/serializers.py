from csinla_posts.models import Exposure,Car,Rent,EntireRent,UsedGoods,UsedBook,Rent2,Used,Post,PostMessage
from csinla_accounts.models import Profile,NewStudentSubmission,NewStudentComment,ApplyUrl
from rest_framework import serializers
from csinla_accounts.models import WechatInfo
class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'username','images')

class ExposureListSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Exposure
        fields = ('id', 'title', 'content','author','reply_num','post_date','images','times')

class ExposureSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Exposure
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date',
                  'active','phone','weixin','last_change_time','images','times')

class CarSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Car
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date','times',
                  'active','phone','weixin','last_change_time','images','car_id','car_type',
                  'car_type_other','brand','vehicle_age','vehicle_miles','fee','fee2','price',
                  'price2','level_type','level_type_other','transmission_type','displacement','drive_type',
                  'inside_color','outside_color','oil_type','turbo','vin_number','contactor','contact_way')

class RentSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Rent
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date','contact_way','contactor','times',
                  'active','phone','weixin','last_change_time','images','house_id','rent_begins','address','transit_time_toschool_hour',
                  'rent_ends','district','district_other','fee','house_type','share','house_type_other','transit_time_toschool_minute',
                  'room_type','room_type_other','pet','smoke','parking','gender_require','driving_time_toschool_hour',
                  'driving_time_toschool_minute')

class EntireRentSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = EntireRent
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date','contactor','contact_way',
                  'active','phone','weixin','last_change_time','images','house_id','rent_begins','address',
                  'rent_ends','district','district_other','fee','house_type','share','house_type_other','transit_time_toschool_minute',
                  'room_type_other','pet','smoke','parking','driving_time_toschool_hour','pak_nums','transit_time_toschool_hour',
                  'driving_time_toschool_minute')

class UsedGoodsSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = UsedGoods
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date',
                  'active','phone','weixin','last_change_time','images','district','address',
                  'connect_name','connect_phone','connect_wx','content_detail','used_id')

class UsedBookSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = UsedBook
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date',
                  'active','phone','weixin','last_change_time','images','district','address',
                  'connect_name','connect_phone','connect_wx','content_detail','book_id')

class Rent2Serializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Rent2
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date','contact_way','contactor',
                  'active','phone','weixin','last_change_time','images','house_id','rent_begins','address','driving_time_toschool',
                  'rent_ends','district','district_other','fee','house_type','share','house_type_other','transit_time_toschool',
                  'room_type','room_type_other','pet','smoke','parking','gender_require')

class UsedSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Used
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date',
                  'active','phone','weixin','last_change_time','images','district','address',
                  'connect_name','connect_phone','connect_wx','content_detail','used_id','times')

class WechatInfoSerializer(serializers.ModelSerializer):
    userinfo = ProfileListSerializer()
    class Meta:
        model = WechatInfo
        fields = ('open_id', 'unionid', 'scene_id','nickname','headimgurl','sex','province',
                  'city','country','userinfo')

class PostSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    class Meta:
        model = Post
        fields = ('id', 'title', 'content','author','reply_num','post_date','expire_date','times',
                  'active','phone','weixin','last_change_time','pic_nums','images','belong_to')


class PostMessageSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    creator = ProfileListSerializer()
    class Meta:
        model = PostMessage
        fields = ('post', 'create_time', 'creator','content_text','message_type','reply_message','floor','is_valid',
                  'has_read')


class NewStudentSubmissionSerializer(serializers.ModelSerializer):
    user = ProfileListSerializer()
    class Meta:
        model = NewStudentSubmission
        fields = (
        'title', 'content', 'content_detail', 'img', 'url', 'user', 'belong', 'is_valid')

class NewStudentCommentSerializer(serializers.ModelSerializer):
    user = ProfileListSerializer()
    class Meta:
        model = NewStudentComment
        fields = (
        'comments', 'fav_nums', 'belong', 'user')

class ApplyUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyUrl
        fields = (
        'url', 'belong', 'name')