from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import  createnew
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from urllib.parse import quote

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

meta_url="https://www.metacritic.com/search/movie/{}/results"
base_url="https://www.rottentomatoes.com/search?search={}"
def start(response):
    return HttpResponseRedirect("/login")
def index(response):
    return render(response,"main/base.html",{})

def home(response):
    return render(response,"main/home.html",{})

def li(response,id):
    ls = list.objects.get(id=id)
    if response.method == "POST":
        if response.POST.get("save"):
            for item in ls.item_set.all():
              if response.POST.get("c"+str(item.id)):
                item.checked=True
              else:
                item.checked=False
              item.save()
        elif response.POST.get("add"):
            txt = response.POST.get("arg1")
            if len(txt)>2:
             if response.POST.get("arg2"):
                b=True
             else :
                b=False
             ls.item_set.create(text=txt,checked=b)               
    return render(response,"main/lists.html",{"ls" : ls})
def cinema(response,id):
    movie=Movie.objects.get(id=id)
    return render(response,"main/particular.html",{"movie" : movie})

def create(response):
    if response.method == "POST":
        form = createnew(response.POST)
        if form.is_valid() :
            n=form.cleaned_data["name"]
            t=list(name=n)
            t.save()
            response.user.todolist.add(t)
        return HttpResponseRedirect("/%i" %t.id)
    else:
       form = createnew()
    return render(response,"main/create.html",{"form" : form})

def view(response):
    return render(response,"main/view.html",{})


def results(response):
    search = response.POST.get("search")
    #print(search)
    final_url=base_url.format(quote_plus(search))
    r = requests.get(final_url)
    #print(final_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    x=soup.find_all('search-page-media-row')
    movie_title=[]
    movie_links=[]
    movie_cast=[]
    movie_year=[]
    movie_rating=[]
    movie_images=[]
    show_title=[]
    show_links=[]
    show_cast=[]
    show_year=[]
    show_rating=[]
    show_images=[]
    meta_rating=[]
    for i in range(0,len(x)):
       z=x[i].get('releaseyear')
       if len(z)!=0 :
          y=x[i].find('a',attrs={ 'class' : 'unset',
                             'slot' : 'title'  })
          img=x[i].find('a',attrs={'class' : 'unset',
                             'slot' : 'thumbnail'  })
          img1 = img.find('img').get('src')
          movie_images.append(img1)
          movie_links.append(y.get('href'))                         
          movie_title.append(y.text.strip())
          movie_cast.append(x[i].get('cast'))
          movie_year.append(x[i].get('releaseyear'))
          if x[i].get('tomatometerscore')=="":
            movie_rating.append('N/A')
          else:
            movie_rating.append(x[i].get('tomatometerscore'))
       else:
          y=x[i].find('a',attrs={ 'class' : 'unset',
                             'slot' : 'title'  })
          img=x[i].find('a',attrs={'class' : 'unset',
                             'slot' : 'thumbnail'  })
          img1 = img.find('img').get('src')
          show_images.append(img1)
          show_links.append(y.get('href'))                         
          show_title.append(y.text.strip())
          show_cast.append(x[i].get('cast'))
          show_year.append(x[i].get('startyear'))
          show_rating.append(x[i].get('tomatometerscore'))
    movies_list=[]
    shows_list=[]
    movies_id=[]
    
    for i in range(0,len(show_title)):
        shows_list.append((show_title[i],show_links[i],show_cast[i],show_images[i],show_rating[i],show_year[i])) 
    cast_list=[]
    movie_info_list=[]
    watch_list=[]
    scraped=0
    for url in movie_links:
       cast_dict={}
       site=None
       if (url != ''):
        site=requests.get(url)
       else:
        continue
       soup = BeautifulSoup(site.content, 'html5lib')
       print(url)
       castsection = soup.find('div', attrs={'class':'castSection'})
       cast_table=[]
       if(castsection):
         cast_table=castsection.find_all('div', attrs={'class':'cast-item media inlineBlock'})
       for i in cast_table:
        cast_dict[i.find_all('span')[0].text.strip()]=i.find_all('span')[1].text.strip()
       cast_list.append(cast_dict)
       movie_info={}
       plot=soup.find('div' , attrs={'id' : 'movieSynopsis'}).text.strip()
       movie_info['plot:']=plot
       y=soup.find('ul' , attrs={'class' : 'content-meta info'})
       z=y.find_all('li')
       t=z[0].find('div', attrs={'class' : 'meta-label subtle'}).text
       if z[0].find('div', attrs={'class' : 'meta-value genre'}) !=None:
          t1=z[0].find('div', attrs={'class' : 'meta-value genre'}).text.strip()
          t1 = t1.replace("\n", "")
          t1=t1.replace(" ","")
          movie_info[t]=t1
       for i in range(1,len(z)):
            t=z[i].find('div', attrs={'class' : 'meta-label subtle'}).text
            t1=z[i].find('div', attrs={'class' : 'meta-value'}).text.strip()
            t1 = t1.replace("\n", "")
            t1=t1.replace(" ","")
            if t=="Release Date (Theaters):" or t=="Release Date (Streaming):" :
               movie_info['Release Date:']=t1
            else:
               movie_info[t]=t1
       if 'Release Date:' not in movie_info.keys():
        movie_info['Release Date:']='N/A'
       if 'Director:' not in movie_info.keys():
        movie_info['Director:']='N/A'
       if 'Producer:' not in movie_info.keys():
        movie_info['Producer:']='N/A'
       if 'Writer:' not in movie_info.keys():
        movie_info['Writer:']='N/A'
       if 'Genre:' not in movie_info.keys():
        movie_info['Genre:']='N/A'
       if 'Original Language:' not in movie_info.keys():
        movie_info['Original Language:']='N/A'
       if 'Runtime:' not in movie_info.keys():
        movie_info['Runtime:']='N/A'
       if 'Plot:' not in movie_info.keys():
        movie_info['Plot:']='N/A'
       movie_info_list.append(movie_info)
       watch_dict={}
       where=soup.find_all('where-to-watch-meta')
       x=soup.find_all('where-to-watch-bubble')
       for i in where:
        i.find('where-to-watch-bubble').find()
        watch_dict[i.get('href')]=i.find('where-to-watch-bubble').get('image')
       watch_list.append(watch_dict)
       scraped = scraped+1
    movie_obj=[]
    for i in range(0,len(movie_info_list)):
      se=meta_url.format(quote(movie_title[i]))
      got=requests.get(se, headers=headers)
      res=BeautifulSoup(got.content, 'html5lib')
      if (res.find('span', attrs={'class':'metascore_w medium movie positive'})):
        print(se)
        meta_rating.append(res.find('span', attrs={'class':'metascore_w medium movie positive'}).text)
      else:
        meta_rating.append("N/A")

      
      flag=0
      for x in Movie.objects.all():
        if (x.title == movie_title[i]):
            cine_id=x.id
            break
      else:
          m1=Movie(title=movie_title[i],plot=movie_info_list[i]['plot:'],language=movie_info_list[i]['Original Language:'],
                  Director=movie_info_list[i]['Director:'],Producer=movie_info_list[i]['Producer:'],Writer=movie_info_list[i]['Writer:'],
                  year=movie_info_list[i]['Release Date:'],duration=movie_info_list[i]['Runtime:'],
                  genre=movie_info_list[i]['Genre:'],rating=movie_rating[i],platform=watch_list[i],
                  cast=cast_list[i],image=movie_images[i])
          m1.save()
          cine_id=m1.id

      movies_id.append(cine_id)
      movie_obj.append(Movie.objects.get(id=cine_id))
    for k in movie_info_list[0].keys():
       print(k)
    for i in range(0,scraped):
        movies_list.append((movie_title[i],movie_links[i],movie_cast[i],movie_images[i],movie_rating[i],movie_year[i],movies_id[i]))
    stuff={
         'searched':search,
         'movies_list':movies_list,
         'shows_list' : shows_list,
         'movie_obj':movie_obj,
    }
    print(meta_rating)
    return render(response,"main/results.html",stuff)

def wishlist(request):
    movies = Movie.objects.filter(users_wishlist=request.user)
    return render(request, "main/watchlist.html", {"wishlist": movies})


def add_to_wishlist(request, id):
    product = get_object_or_404(Movie, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
    else:
        product.users_wishlist.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def favlist(request):
    movies = Movie.objects.filter(users_favlist=request.user)
    return render(request, "main/favlist.html", {"favlist": movies})

def add_to_favlist(request, id):
    product = get_object_or_404(Movie, id=id)
    if product.users_favlist.filter(id=request.user.id).exists():
        product.users_favlist.remove(request.user)
    else:
        product.users_favlist.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def watchedlist(request):
    movies = Movie.objects.filter(users_watchedlist=request.user)
    return render(request, "main/watchedlist.html", {"watchedlist": movies})

def add_to_watchedlist(request, id):
    product = get_object_or_404(Movie, id=id)
    if product.users_watchedlist.filter(id=request.user.id).exists():
        product.users_watchedlist.remove(request.user)
    else:
        product.users_watchedlist.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])