from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),  # homepage

    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    # (html, view function, name)
    path('logout/', views.logoutuser, name='logout'),



    path('bookstorehpuser/',
         views.bookstorehpuser, name='bookstorehpuser'),

    path('bookstorehpmanager/', views.bookstorehpmanager,
         name='bookstorehpmanager'),

    path('browsebook/', views.browsebook, name='browsebook'),
    path('bookinfo/<str:isbn>/', views.bookinfo, name='bookinfo'),

    path('browsecustomer/', views.browsecustomer, name='browsecustomer'),
    path('customerprofile/<str:username>/',
         views.customerprofile, name='customerprofile'),

    path('recommendedbooks/', views.recommendedbooks, name='recommendedbooks'),
    path('degreeofseprsearch/', views.degreeofseprsearch,
         name='degreeofseprsearch'),

    path('stockmanage/', views.stockmanage, name='stockmanage'),
    path('bookmanage/<str:isbn>/', views.bookmanage, name='bookmanage'),
    path('addbook/', views.addbook, name='addbook'),

    path('statistics/', views.statistics, name='statistics'),
    path('bookstatistics/', views.bookstatistics, name='bookstatistics'),
    path('userstatistics/', views.userstatistics, name='userstatistics'),

    path('managerdata/', views.managerdata, name='managerdata'),

    path('addmanager/<str:username>/', views.addmanager, name='addmanager'),

    path('search/', views.search, name='search'),

    path('changeaccess/<str:username>/',
         views.changeaccess, name='changeaccess'),

    path('addcomment/<str:isbn>/',
         views.addcomment, name='addcomment'),

    path('addtrust/<str:username>/', views.addtrust, name='addtrust'),

    path('addcomment/<str:isbn>/',
         views.addcomment, name='addcomment'),

    path('editcomment/<str:username>/<str:isbn>/',
         views.editcomment, name='editcomment'),

    path('changebookscore/<str:username>/<str:isbn>/',
         views.changebookscore, name='changebookscore'),

    path('deletecomment/<str:username>/<str:isbn>/',
         views.deletecomment, name='deletecomment'),

    path('addusefullness/<str:username>/<str:isbn>/',
         views.addusefullness, name='addusefullness'),

    path('orderhistory/',
         views.orderhistory, name='orderhistory'),

    path('orderplace/<str:isbn>/',
         views.orderplace, name='orderplace'),

    path('deliverystatus/',
         views.deliverystatus, name='deliverystatus'),

    path('changestatus/<int:id>/',
         views.changestatus, name='changestatus'),

    path('deletebook/<int:isbn>/',
         views.deletebook, name='deletebook'),

    path('requestbook/',
         views.requestbook, name='requestbook'),

    path('requestbutton/',
         views.requestbutton, name='requestbutton'),

    path('changereqstatus/<int:id>/',
         views.changereqstatus, name='changereqstatus'),

    path('requestbstatus/',
         views.requestbstatus, name='requestbstatus'),
]
