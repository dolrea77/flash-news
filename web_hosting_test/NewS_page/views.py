from django.shortcuts import render, redirect
from .models import Crawring, Crawring_ct
from .news_craw import newscrawring
from .model_call import summary
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
def main_page(request):
    craw = Crawring.objects.exclude(summarize='').order_by('-created_at')[:20]
    if request.GET.get('category', None):
        cate = request.GET.get('category', None)
        print('cate: ',cate)
        craw_ct = Crawring_ct.objects.filter(category=cate).exclude(summarize_ct='').order_by('-created_at_ct')[:30]
        return render(request, "main.html", {'craw_ct': craw_ct})

    return render(request, "main.html", {'craw': craw})