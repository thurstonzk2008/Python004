from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg
import re

from .models import SKUs, Comments


def indexnull(request):
    sku = SKUs.objects.all().values('sku')[0]['sku']
    return HttpResponseRedirect(f'{sku}')


def search(request):
    sku = request.GET.get('sku')
    search = request.GET.get('search')

    skus = SKUs.objects.all()
    skuname = skus.filter(sku=sku).values('skuname')[0]['skuname']

    # search格式：
    # 1. 评论关键字： "keyword"
    # 2. 开始日期："2020-10-20"
    # 3. 日期区间："2020-10-20 - 2020-12-30"
    comms = Comments.objects.filter(sku=sku)
    if re.match(r'^\d{4}-\d{2}-\d{2}$', search):  # Start Date
        sdate = search
        comms = comms.filter(updatetime__gte=sdate)
        print(comms)
    elif re.match(r'^\d{4}-\d{2}-\d{2} - \d{4}-\d{2}-\d{2}$', search):  # Duration
        sdate, edate = search.split(' - ')
        comms = comms.filter(updatetime__range=[sdate, edate])
    else:  # Key word
        key = search
        comms = comms.filter(cdescription__contains=key)

    return render(request, 'search.html', locals())


def indexsku(request, sku):
    skus = SKUs.objects.all()
    skuname = skus.filter(sku=sku).values('skuname')[0]['skuname']
    skunow = sku

    comms = Comments.objects.filter(sku=sku)
    commscount = comms.count()

    queryset = comms.values('sentiments')
    filter_sens = {'sentiments__gte': 0.5}
    positive = queryset.filter(**filter_sens).count()
    negative = commscount - positive

    sentiments__avg = f"{100*comms.aggregate(Avg('sentiments'))['sentiments__avg']:0.2f}"

    return render(request, 'index.html', locals())
