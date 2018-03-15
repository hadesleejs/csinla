from django.conf.urls import url
from csinla_curricular import views
from .views import CurricularView
urlpatterns = [
    url(r'^$', CurricularView.as_view(),name='curricular'),
    url(r'^subjects_compare$', views.subjects_compare),
    url(r'^pdf_view$', views.pdf_view),
    url(r'^build_view$', views.build_view),
]
