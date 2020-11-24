from django.urls import path
from.views import main, new_search

urlpatterns = [
    path('', main, name='main'),
    path('new_search/', new_search, name='search')
]