import requests
from django.shortcuts import render,HttpResponse,redirect
from bs4 import BeautifulSoup as BSoup
from accounts.models import Headline
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .forms import RegistrationForm,UpdateForm,BlogForm, Cityform
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from .models import Blogs,Likes
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import FormView
import json
from .models import City
from newsapi import NewsApiClient

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Saved')
        else:
            return render(request,'form.html',{'form':form})
    else:
        form = RegistrationForm()
        return render(request,'form.html',{'form':form})

def login_page(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        obj=authenticate(username=username,password=password)
        if obj:
            login(request,obj)
            return redirect('/accounts/home/')
        else:
            return HttpResponse("username or password incorrect")
    return render(request,'login.html')

@login_required(login_url="/accounts/login/")
def home_page(request):
    blogs=Blogs.objects.all()[::-1]
    return render(request,'Home.html',{'blogs':blogs})

def logout_page(request):
    logout(request)
    return redirect('/accounts/login/')

def nav_page(request):
    return render(request,'navbar.html')

def edit_profile(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/home/')
        else:
            return render(request,'edit.html',{'form':form})
    else:
        form = UpdateForm(instance=request.user)
        return render(request,'edit.html',{'form':form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/accounts/home/')
        else:
            return render(request,'form.html',{'form':form})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request,'form.html',{'form':form})

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            return redirect('/accounts/home/')
        else:
            return render(request,'create_blog.html',{'form':form})
    else:
        form =BlogForm()
        return render(request,'create_blog.html',{'form':form})

@login_required(login_url="/accounts/login/")
def my_blogs(request):
    blogs=Blogs.objects.filter(user=request.user)[::-1]
    return render(request,'my_blogs.html',{'blogs':blogs})

def delete_user(request,id):
    blog=Blogs.objects.get(id=id)
    if request.user==blog.user:
        blog.delete()
    return redirect('/accounts/myblog/')

def detailed_blog(request,id):
    blog=Blogs.objects.get(id=id)
    check=Likes.objects.filter(user=request.user,blog=blog)
    if check:
        liked=True
    else:
        liked=False
    count=Likes.objects.filter(blog=blog).count()
    return render(request,"detailed_blog.html",{"blog":blog,"liked":liked,"count":count})

def like_blog(request):
    id=request.GET["id"]
    blog=Blogs.objects.get(id=id)
    check=Likes.objects.filter(user=request.user,blog=blog)
    d={}
    if check:
        check[0].delete()
        d["liked"]=False
    else:
        Likes.objects.create(user=request.user,blog=blog)
        d["liked"]=True
    d["count"]=Likes.objects.filter(blog=blog).count()

    response=json.dumps(d)
    return HttpResponse(response,content_type='application/json')

def dark_modeon(request):
    response=redirect('/accounts/home/')
    response.set_cookie("darkmode","on")
    return response

def dark_modeoff(request):
    response=redirect('/accounts/home/')
    response.set_cookie("darkmode","off")
    return response

class DemoView(View):
    template_name="form.html"
    form_class=RegistrationForm

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{"form":form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Saved')
        else:
            return render(request,self.template_name,{'form':form})

class DemoBlog(ListView):
    template_name= "my_blogs.html"

    def get_queryset(self):
        return Blogs.objects.filter(user=self.request.user)[::-1]

class DetailedBlog(DetailView):
    template_name='detailed_blog.html'
    model=Blogs
    context_object_name='blog'
    

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all()
        check=Likes.objects.filter(user=self.request.user,blog=context['blog'])
        if check:
            liked=True
        else:
            liked=False
        count=Likes.objects.filter(blog=context['blog']).count()
        context['liked']=liked
        context['count']=count
        context['blogs']=blogs
        return context
  
class RegisterView(FormView):
    template_name='form.html'
    form_class=RegistrationForm
    success_url='/accounts/login/'

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)


def scrape (request):
    newsapi = NewsApiClient(api_key="eac3e5546aa54fd7b5619d26b190bfc0")
    topheadlines = newsapi.get_top_headlines(sources='bbc-news,the-verge')
    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img) 
    return render(request, 'news.html', context={"mylist" : mylist})   

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news.html", context)

def index(request):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=hourly,daily&appid{"

    if request.method == 'POST':
        form = Cityform(request.POST)
        form.save()
    form = Cityform()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        city_weather = {
            "city" : city.name,
            "temperature" :r['main']['temp'],
            "description" :r['weather'][0]['description'],
            "icon" :r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
       

    context = {"weather_data": weather_data, 'form': form}

    return render(request, 'weather.html', context)    





