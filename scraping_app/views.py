from django.shortcuts import render
from django.views import generic
import requests
from bs4 import BeautifulSoup
import re
from .models import SavedNews
#from django.https import HttpResponseResirect


class IndexView(generic.TemplateView):
    """スクレイピング表示"""

    template_name = 'scraping_news/scraping.html'

    def scraping_yahoo(self):
        news_list = []
        response = requests.get("https://news.yahoo.co.jp/")
        bs = BeautifulSoup(response.text, "html.parser")
        data_list = bs.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
        for data in data_list:
            title = data.contents[0]
            url_news = data.attrs["href"]
            news_list.append([title, url_news])
        #news_list = news_list[:-1]
        context = {'news_list': news_list[:-1],}
        #context['news_list'] = news_list[:-1]
        return context

    def scraping_nhk(self):
        news_list = []
        response = requests.get("https://www3.nhk.or.jp/news/")
        bs = BeautifulSoup(response.content, "html.parser")
        data_list = bs.find_all("dd")
        for data in data_list:
            title=data.text
            url_news = data.a.attrs["href"]
            if "www"  not in url_news:
                news_list.append([title, "https://www3.nhk.or.jp"+url_news])
        context = {'news_list': news_list,}
        return context

    def scraping_yomiuri(self):
        news_list = []
        response = requests.get("https://www.yomiuri.co.jp/")
        bs = BeautifulSoup(response.text, "html.parser")
        data_list = bs.find_all("h3", class_="title")
        for data in data_list:
            title=data.text
            url_news = data.a.attrs["href"]
            if "https"  in url_news:
                news_list.append([title, url_news])
        context = {'news_list': news_list,}
        return context

    def post(self, request):
        if "yahoo" in request.POST:
            context = self.scraping_yahoo()
            return render(request, 'scraping_news/scraping.html', context)
        if "nhk" in request.POST:
            context = self.scraping_nhk()
            return render(request, 'scraping_news/scraping.html', context)
        if "yomiuri" in request.POST:
            context = self.scraping_yomiuri()
            return render(request, 'scraping_news/scraping.html', context)

        if "save" in request.POST:
            print(request.POST)
            sn =  SavedNews(title=request.POST["title"], url=request.POST["url"])
            sn.save()
            # news = SavedNews(content=request.POST["content"])
            # news.save()
            return render(request, 'scraping_news/scraping.html')



class SavedView(generic.ListView):
    """保存結果表示"""
    template_name = 'scraping_news/saved.html'
    model = SavedNews
    context_object_name = "saved_news"
    # saved_news = SavedNews.objects.all
    # context = {'saved_news': saved_news}
    
    #     #template = loader.get_template('reservations.html')
    # context = {
    #     'saved_news': saved_news
    #     }


    # def get(self, request, **kwargs):
    #     saved_news = SavedNews.objects.all
    #     context = {'saved_news': saved_news}
    #     return self.render_to_response(context)
    
    # context_object_name = "saved_news"