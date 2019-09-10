from django.urls import path

from . import views 



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('home/', views.selectbusiness, name='index'),
    path('selectreg/', views.countries_view, name='countries_view'),
    path('bagroup/selectreg/', views.bagroupall, name="bagroupall"),
    path('table/',views.secondpage, name ="secondpage"),
    path('bagroup/table/', views.groupallsecondpage, name='groupallsecondpage'),
    path('table/edit/<int:pk>/', views.edit_item, name="edit_item"),
    path('table/selectcontrol/', views.selectcontrol, name='selectcontrol'),
    path('add_control/<int:pk>/', views.select_control, name="select_control"),
    path('table/selectcontrol/edit/process/<int:pk>/', views.edit_process,name="edit_process"),  #if we click on edit option in control page
    path('edit_control/<int:pk>/', views.select_control, name="select_control"), #if we click on add option in control page
    path('table/view_control',views.thirdpage, name ="thirdpage"),
    path('add_risk/<int:pk>/', views.select_risk, name="select_risk"),
    path('table/edit/businessactivity/<int:pk>/', views.edit_regulation,name="edit_regulation"),
    path('table/selectrisk/',views.selectrisk, name ="selectrisk"),
    path('edit_risk/<int:pk>/', views.select_risk, name="select_risk"),#if we click on add option in Risk page
    path('table/selectrisk/edit/control/<int:pk>/', views.edit_control,name="edit_control"),#if we click on edit option in risk page
    path('table/selectrisk/finalmapping/', views.showfinalmapping, name="showfinalmapping"),
    path('table/selectrisk/finalmapping/view/', views.viewfinalmapping, name="viewfinalmapping"),
    path('table/selectrisk/finalmapping/edit/risk/<int:pk>/', views.edit_risk, name="edit_risk"),#if we click on edit option in final mapping page


    path('table/selectrisk/edit/control/<int:pk>/', views.edit_control,name="edit_control"),
    
    path('risk/<int:pk>/', views.select_risk, name="select_risk"),
    # path('table/edit/businessactivity/<int:pk>/', views.edit_ba,name="edit_ba"),
  
    
   
]