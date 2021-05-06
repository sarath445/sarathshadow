from django.urls import path
from . import views
from .forms import BlogForm
from django.views.generic import TemplateView,ListView,DetailView
from accounts.views import scrape,news_list


urlpatterns = [
    #path('register/',views.register),
    path('login/',views.login_page),
    path('home/',views.home_page),
    path('logout/',views.logout_page),
    path('',views.nav_page),
    path('edit/',views.edit_profile),
    path('pswd/',views.change_password),
    path('create/',views.create_blog),
    path('delete/<int:id>/',views.delete_user),
    #path('detail/<int:id>/',views.detailed_blog),
    path('likeblog/',views.like_blog),
    path('darkmodeon/',views.dark_modeon),
    path('darkmodeoff/',views.dark_modeoff),
    path('cf/',views.DemoView.as_view()),
    path('bf/',views.DemoView.as_view(template_name="create_blog.html",form_class=BlogForm)),
    path('sl/',TemplateView.as_view(template_name="login.html")),
    path('myblog/',views.DemoBlog.as_view()),
    path('detail/<pk>/',views.DetailedBlog.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('scrape/', scrape, name="scrape"),
    path('live/', news_list, name="news"),
    path('weather/',views.index),


]