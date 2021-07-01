from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('keyboard/', views.keyboard, name='keyboard'),
    path('recommend/', views.recommend, name='recommend'),
    path('medicine/', views.medicine, name='medicine'),
    path('med_detail/', views.med_detail, name='med_detail'),
    path('precautions/', views.precautions, name='precautions'),
    path('check/', views.check, name='check'),
    path('checkusage/', views.checkusage, name='checkusage'),
    path('checkprecaution/', views.checkprecaution, name='checkprecaution'),
    path('showmap/', views.showmap, name='showmap'),
    path('food/', views.food, name='food'),
    path('imageupload/', views.imageupload, name='imageupload'),
    path('imagelist/', views.imagelist, name='imagelist'),
    path('textract/', views.textract, name='textract'),
    path('mapping/', views.mapping, name='mapping')
]
