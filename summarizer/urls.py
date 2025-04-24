from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('summarize/', summarize_text, name='summarize_text'),
    path('download-summary/', download_summary, name='download_summary'),

]