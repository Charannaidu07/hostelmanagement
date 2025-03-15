from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('logout/',views.logout,name='logout'),
    path('features/',views.features,name='features'),
    path('help/',views.help,name='help'),
    path('profile/',views.profile,name='profile'),
    path('anouncements/',views.anouncements,name='anouncements'),
    path('outing/',views.outing,name='outing'),
    path('outing/request/', views.outing_request, name='outing_request'),
]
