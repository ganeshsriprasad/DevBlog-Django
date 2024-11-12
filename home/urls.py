from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="homes"),
    path('posts/', views.all_posts, name="all_posts"),
    path('checker/', views.temp, name="teemmp"),
    path('registration/', views.Registration, name= "the_signup"),
    path('login/', views.the_login, name= "the_login"),
    path('logout/', views.the_logout, name= "logout"),
    path('about/', views.about, name= "about"),
     path('contact/', views.contact, name= "contact"),
    path('artical/<slug:the_artical>/', views.artical_view, name='artical'),
    
# -------- Not 404 hanlder But showing 404 by redirecting to 404 if none of page clicked here -------
    # path('404/', views.f404, name= "404"),
    # re_path(r'^.*$', RedirectView.as_view(url='/404/')),

# ------------------------------------------------------------------------------

]

