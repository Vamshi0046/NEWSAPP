from django.shortcuts import render,HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from app1.forms import signupF,loginF
import datetime
import requests
import json
def news(request):
    if request.method == 'POST':
        Day=datetime.date.today()
        Today=Day.strftime("%d")
        n = request.POST.get('news_type')
        url = f"https://newsapi.org/v2/everything?q={n}&from=2023-03-{Today}&sortBy=publishedAt&apiKey=d16f9163c3474ad79ebf3ec9a90d3811"
        r = requests.get(url)
        news = r.json()
        print(news)
        # news=json.loads(r.text)
        articles = news['articles']
        for article in articles:
            article['image_url'] = article.get('urlToImage', '') 
        return render(request, 'htmlfiles/news.html', {'articles': articles})
    return render(request, 'htmlfiles/news.html')



def signup(request):
    if request.method=="POST":
        fm=signupF(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm=signupF()
    return render(request,'htmlfiles/signup.html',{'form':fm})


def userlogin(request):
    if request.method=='POST':
        fm=loginF(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/news/')
    else:
        fm=loginF()
    return render(request,'htmlfiles/userlogin.html',{'loginform':fm})


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def base(request):
    return render(request,'htmlfiles/base.html')





























