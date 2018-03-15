# coding=utf-8
# author=lijiaoshou
# date='2017/8/25 11:25'
from models  import Post,Rent,EntireRent,Car,UsedBook,UsedGoods
from haystack import indexes
# class PostIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     def get_model(self):
#         return Post
#     def index_queryset(self,using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()
class RentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Rent
    def index_queryset(self,using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
class CarIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Car
    def index_queryset(self,using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class EntireRentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return EntireRent
    def index_queryset(self,using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class UsedBookRentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return UsedBook

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class UsedGoodsRentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return UsedGoods

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
