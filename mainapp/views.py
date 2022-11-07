from ast import Global
from multiprocessing import context
from django.shortcuts import redirect, render
import requests
import json
from bs4 import BeautifulSoup


def home(request):
    url='https://api.covid19api.com/summary'
   
    data=requests.get(url).json()["Global"]
    countriesdata=requests.get(url).json()["Countries"]
    news="https://newsapi.org/v2/top-headlines?country=in&apiKey=cb0df83fd349468fa616de52f03a6cef&category=health"
    newsdata=requests.get(news).json()["articles"]


    url2 = "https://www.indiatvnews.com/topic/coronavirus"
    page = requests.get(url2).text
    doc = BeautifulSoup(page, "html.parser")
    div=doc.find("ul",class_="newsListfull").find_all("li")
    list1=[]
    for i in div:
        list2=[]
        list2.append(i.a.img.get("data-original"))
        list2.append(i.find("img").get("alt"))
        list2.append(i.find("a").get("title"))
        list1.append(list2)
    context={
        "data":data,
        "contries":countriesdata,
        "newsdata":newsdata,
        "newslist":list1
    }
    return render(request,"covin/index.html",context)




def cuntrylive(request,Country):
    url1='https://api.covid19api.com/summary'
    countriesdata=requests.get(url1).json()["Countries"]
    conlist=[]
    NewConfirmed=None
    TotalConfirmed=None
    NewDeaths=None
    TotalDeaths=None
    NewRecovered=None
    TotalRecovered=None
    for i in countriesdata:
        if i.get("Country")==Country:
            conlist.append(i)
    for data in conlist:
        NewConfirmed=data.get("NewConfirmed")
        TotalConfirmed=data.get("TotalConfirmed")
        NewDeaths=data.get("NewDeaths")
        TotalDeaths=data.get("TotalDeaths")
        NewRecovered=data.get("NewRecovered")
        TotalRecovered=data.get("TotalRecovered")
    url=f"https://api.covid19api.com/live/country/{Country}/status/confirmed"
    data=requests.get(url).json()
    context={
        "livecoun":data,
        "country":Country,
        "conlist":conlist,
        "NewConfirmed":NewConfirmed,
        "TotalConfirmed":TotalConfirmed,
        "NewDeaths": NewDeaths,
        "TotalDeaths":TotalDeaths,
        "NewRecovered":NewRecovered,
        "TotalRecovered":TotalRecovered,

    }
    return render(request,"covin/country.html",context)


def city(request,city,Country,date):
    url="https://data.covid19india.org/state_district_wise.json"
    data1=requests.get(url).json()[city]
    url2=f"https://api.covid19api.com/live/country/{Country}/status/confirmed"
    data=requests.get(url2).json()
    Confirmed=None
    Deaths=None
    Recovered=None
    Active=None
    Date=None
    for d in data:
        if city==d.get("Province") and date==str(d.get("Date")):
            Confirmed=d.get("Confirmed")
            Deaths=d.get("Deaths")
            Recovered=d.get("Recovered")
            Active=d.get("Active")
            Date=d.get("Date")
    context={
        "data":data1,
        "Confirmed":Confirmed,
        "Deaths":Deaths,
        "Recovered":Recovered,
        "Active":Active,
        "date":Date,
        "city":city
    }
    return render(request,"covin/city.html",context)





def news(request):

    news="https://newsapi.org/v2/top-headlines?country=in&apiKey=cb0df83fd349468fa616de52f03a6cef&category=health"
    newsdata=requests.get(news).json()["articles"]
    #############
    url = "https://www.indiatvnews.com/topic/coronavirus"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div1=doc.find("ul",class_="newsListfull").find_all("li")

    list1=[]
    for i in div1:
            list2=[]
            list2.append(i.a.img.get("data-original"))
            list2.append(i.find("img").get("alt"))
            list2.append(i.find("a").get("title"))
            list2.append(i.find("a").get("href"))
            list1.append(list2)

    page=50
    for page in range(1,page+1):
        url2 = f"https://www.indiatvnews.com/topic/coronavirus/{page}"
        page = requests.get(url2).text
        doc = BeautifulSoup(page, "html.parser")
        div=doc.find("ul",class_="newsListfull").find_all("li")
        for i in div:
            list2=[]
            list2.append(i.a.img.get("data-original"))
            list2.append(i.find("img").get("alt"))
            list2.append(i.find("a").get("title"))
            list2.append(i.find("a").get("href"))
            list1.append(list2)
    
    context={
        "newslist":list1,
        "newsdata":newsdata
    }
    return render(request,"covin/news.html",context)


def newsdetails(request):
    url=request.GET.get('url')
    news=requests.get(url).text
    doc=BeautifulSoup(news,"html.parser")
    title=doc.find(class_="arttitle").string
    description=doc.find("h2" ,class_="artdec").string
    publish_on=doc.find(class_="published-on").string
    author=doc.find(class_="author-name").string
    image=doc.find(class_="artbigimg row").find("img").get("data-original")
    content=doc.find("div",class_="content").find_all("p")
    list_for_content=[]
    for content_dt in content:
        list_for_content.append(content_dt.string)
    context={
            "title":title,
            "description":description,
            "publish_on":publish_on,
            "author": author,
            "image":image,
            "list_for_content":list_for_content

        }
    return render(request,"covin/newsdetails.html",context)

def newsdetails2(request):
    url=request.GET.get('url')
    news=requests.get(url).text
    doc=BeautifulSoup(news,"html.parser")
    heding=doc.find_all("h1")
    text=doc.find_all("p")
    image=doc.find_all("img")
    print(image,"%%%%%%%%%%%%%%%%555")
      
    

    context={

        }
    return redirect(request,"covin/newsdetails.html",context)