from django.urls import path

from . import views

urlpatterns = [

    path('index/', views.index, name='index'),
    path('pred/', views.pred, name='pred'),
    path('contact/', views.contact, name='contact'),
    path('',views.redirect_root),
    path('search/<str:se>/<str:stock_symbol>/', views.search, name='predict_stock'),

    path('Home/',views.Index_Data,name="home"), 
    path('DashBoard/',views.DashBoard,name="dashboard"), 
    path('Show_Data/<int:id>',views.Show_Data,name='Show_Data'),
    path('login/',views.loginview,name='login'),
    path('reg/',views.regview,name='regview')
   ]
