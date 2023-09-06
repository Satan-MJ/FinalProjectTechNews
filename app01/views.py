import json
import math
import random
import time
from datetime import datetime

import pytz
import jieba
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app01.models import Articles3, InvertedIndex
from app01.models import Comments
from django.db.models import Q, QuerySet


# print('Loading')
# jieba.load_userdict("THUOCL_animal.txt")
# print('1')
# jieba.load_userdict("THUOCL_caijing.txt")
# print('2')
# jieba.load_userdict("THUOCL_car.txt")
# print('3')
# jieba.load_userdict("THUOCL_chengyu.txt")
# print('4')
# # jieba.load_userdict("THUOCL_diming.txt")
# print('5')
# jieba.load_userdict("THUOCL_food.txt")
# print('6')
# jieba.load_userdict("THUOCL_it.txt")
# print('7')
# jieba.load_userdict("THUOCL_law.txt")
# print('8')
# jieba.load_userdict("THUOCL_lishimingren.txt")
# print('9')
# jieba.load_userdict("THUOCL_medical.txt")
# print('10')
# jieba.load_userdict("THUOCL_poem.txt")
# print("Loaded")


# Create your views here.

def to_json(articles):
    json_data = []
    for art in articles:
        json_data.append(art.to_dict())
    return json.dumps(json_data)


def home(request):
    context = {}
    random_id = random.sample(range(1, Articles3.objects.count() - 1), 20)
    items = [Articles3.objects.get(id=i) for i in random_id]

    context['articles'] = to_json(items)

    return render(request, 'home.html', context)


articles: QuerySet = QuerySet()
articles_fs: QuerySet = QuerySet()
fltr = None
sort = 'time'

def appendPageContext(context: dict):
    context['count'] = len(articles_fs)
    context['total_page'] = math.ceil(len(articles_fs) / 20)
    return context

def ArticlesContext(context: dict):
    global articles_fs

    context = appendPageContext(context)
    context['articles'] = to_json(articles_fs[:20])

    context['cats2'] = [f'2022-{m:02d}' for m in range(6, 13)]
    context['cats3'] = [f'2023-{m:02d}' for m in range(1, 9)]

    return context


def HandlePagination(request):
    page_num = request.GET.get("page-num")
    page_num = int(page_num)
    return HttpResponse(to_json(articles_fs[(page_num - 1) * 20:page_num * 20]), content_type="application/json")

def getSorted():
    global sort, articles
    if sort == "time":
        return articles
    elif sort == "pop":
        return articles.order_by('-com_count')

def HandleSort(request):
    global articles, articles_fs, sort
    sort = request.GET.get("sort")
    articles_fs = getSorted()

    if fltr is not None:
        articles_fs = articles_fs.filter(fltr)
    return HttpResponse(to_json(articles_fs[:20]), content_type="application/json")

def HandelFilter(request):
    global articles, articles_fs, fltr
    f = json.loads(request.GET.get("filter"))
    q = Q()
    articles_fs = getSorted()
    if len(f) == 0:
        fltr = None
    else:
        for item in f:
            y = item[9:13]
            m = item[14:16]
            q = q | Q(date__year=y, date__month=m)
        fltr = q
        articles_fs = articles_fs.filter(q)

    return JsonResponse(appendPageContext({"articles": [a.to_dict() for a in articles_fs[:20]]}))
    #return HttpResponse(to_json(articles_fs[:20]), content_type="application/json")


def collections(request):
    global articles, articles_fs
    if 'page-num' in request.GET.keys():
        return HandlePagination(request)
    elif 'sort' in request.GET.keys():
        return HandleSort(request)
    elif 'filter' in request.GET.keys():
        return HandelFilter(request)
    else:
        time_st = time.time()
        articles = Articles3.objects.all()
        articles_fs = articles
        context = ArticlesContext({'type': 'collections'})
        time_ed = time.time()
        context['duration'] = time_ed - time_st
        return render(request, 'search.html', context)


def search(request):
    global articles, articles_fs
    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        if keyword is None or keyword == '':
            return redirect('/')

        time_st = time.time()

        keywords = keyword.split(' ')
        f = Q()
        for k in keywords:
            f = f | Q(text__icontains=k) | Q(title__icontains=k)
        articles = Articles3.objects.filter(f)
        articles_fs = articles

        time_ed = time.time()

        context = ArticlesContext({'type': 'search', 'keyword': keyword})


        context['duration'] = time_ed - time_st

        return render(request, 'search.html', context)
    else:
        if 'sort' in request.GET.keys():
            return HandleSort(request)
        elif 'filter' in request.GET.keys():
            return HandelFilter(request)
        else:
            return HandlePagination(request)


def get_comments(article_id):
    comments = Comments.objects.filter(article=article_id).order_by('-date', '-time')
    return [
        {'id': com.id, 'username': com.username, 'comment': com.comment, 'date': com.date.isoformat(),
         'time': com.time.isoformat()} for com in comments]


def article(request, a_id):
    if request.method == 'GET':
        art = Articles3.objects.get(id=a_id)

        paras = art.text.split('\n')
        paras.append('')

        img_str = art.images[:-1].split(';')
        imgs = {}
        for s in img_str:
            img_split = s.split(',')
            if len(img_split) != 3:
                continue
            print(img_split)
            imgs[int(img_split[0])] = (img_split[1], img_split[2])

        body = []
        for i in range(0, len(paras)):
            if i in imgs.keys():
                body.append({'text': paras[i], 'photo': 1, 'src': imgs[i][0], 'capt': imgs[i][1]})
            else:
                body.append({'text': paras[i], 'photo': 0})

        context = {'id': a_id, 'title': art.title, 'body': body, 'img_src': art.img_src, 'date': art.date.isoformat(),
                   'time': art.time.isoformat(), 'src': art.src, 'url': art.url,
                   'comments': json.dumps(get_comments(a_id))}

        return render(request, 'article.html', context)
    else:
        article_id = request.POST.get("article_id")
        a = Articles3.objects.get(id=article_id)

        if request.POST.get("operation") == "add":
            comment = request.POST.get("comment")
            username = request.POST.get("username")

            if comment == '' or username == '':
                return JsonResponse({'code': 1, 'message': '请输入评论内容或用户名'})

            dt = datetime.now(pytz.timezone('Asia/Shanghai'))
            d = dt.date().isoformat()
            t = dt.time().strftime("%H:%M:%S")

            c = Comments.objects.create(username=username, comment=comment, date=d, time=t, article_id=article_id)
            c.save()

            a.com_count = a.count_comments()
            a.save()

            return JsonResponse({'code': 0, 'id': c.id, 'username': username, 'comment': comment, 'date': d, 'time': t})
        else:
            comment_id = request.POST.get("id")
            Comments.objects.get(id=comment_id).delete()

            a.com_count = a.count_comments()
            a.save()

            return JsonResponse(get_comments(article_id), safe=False)
