from django.urls import path
f
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('summarize/', summarize_text, name='summarize_text'),
]