from django.shortcuts import render
from django.views import generic
import requests
from bs4 import BeautifulSoup
import re
from .models import SavedNews
from django.shortcuts import redirect
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
            #news_list.append({"title":title, "url":url_news})
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
            
            titles=request.POST.getlist('title')
            urls=request.POST.getlist('url')
            checks=request.POST.getlist('checks')
            
            for check in checks:
                new_record = SavedNews(title=titles[int(check)-1], url=urls[int(check)-1])
                new_record.save()

            if "yahoo" in urls[0]:
                context = self.scraping_yahoo()
                return render(request, 'scraping_news/scraping.html', context)
            if "nhk" in urls[0]:
                context = self.scraping_nhk()
                return render(request, 'scraping_news/scraping.html', context)
            if "yomiuri" in urls[0]:
                context = self.scraping_yomiuri()
                return render(request, 'scraping_news/scraping.html', context)

class SavedView(generic.TemplateView):
    template_name = 'scraping_news/saved.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs) 
        #saved_news = SavedNews.objects.all().values_list('title', flat=True).order_by('title').distinct()
        #_saved_news = SavedNews.objects.all().values_list("title").distinct()
        _saved_news = SavedNews.objects.all()
        
        title_list = []
        saved_news = []
        for n in _saved_news:
            if n.title in title_list:
                continue
            title_list.append(n.title)
            saved_news.append(n)
        context = {
            "saved_news": saved_news
        }
        return self.render_to_response(context)

    def post(self, request):
        print(request.POST)
        checks=request.POST.getlist('checks')
        for check in checks:
            del_record = SavedNews.objects.get(id=int(check))
            del_record.delete()            
        return redirect('scraping_app:saved')


# class SavedView(generic.ListView):
#     """保存結果表示"""
#     template_name = 'scraping_news/saved.html'
#     #model = SavedNews
#     query_set = SavedNews.objects.distinct()
#     context_object_name = "saved_news"

#     # def get_queryset(self, **kwargs):
#     #     queryset = super().get_queryset(**kwargs).distinct("title")
#     #     return queryset

#     def post(self, request):
#         print(request.POST)
#         checks=request.POST.getlist('checks')
#         for check in checks:
#             del_record = SavedNews.objects.get(id=int(check))
#             del_record.delete()
            
#         return redirect('scraping_app:saved')
#         #render(request, 'scraping_news/saved.html')
