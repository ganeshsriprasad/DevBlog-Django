from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name= "dashboard"),
    path('<str:page>/', views.dashboard_options, name= "option"),
    path('update/<str:uid>/', views.update_post, name= "update_post"),
    path('delete/<str:uid>/', views.delete_post, name= "delete_post"),
    # path('contact/', views.feedback, name= "the_about"),
    # path('dashboard/your_posts/<slug:key>/', views.edit_post, name='edit_post'),
    # path('delete_post/<slug:slug>/', views.delete_post, name='delete_post'),
    # path('dashboard/your_posts/', views.your_posts, name='your_posts'),
    # path('dashboard/<str:option>/', views.dynamic_option, name="dynamic_option"),
]
