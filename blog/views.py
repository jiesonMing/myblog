from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Banner, Article, Tag, Link, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # 分页
import time
import json
from time import sleep
import requests
import urllib.request
from bs4 import BeautifulSoup

# 公共函数
def global_variable(request):
    allcategory = Category.objects.all()
    remen = Article.objects.filter(tui__id=2)[:6] # 热门
    tags = Tag.objects.all() # 标签
    return locals()

#把Banner表导入
def index(request):
    banner = Banner.objects.filter(is_active=True)[0:4]#查询所有幻灯图数据，并进行切片
    tui = Article.objects.filter(tui__id=1)[:3]#查询推荐位ID为1的文章
    allarticle = Article.objects.all().order_by('-id')[0:10] #所有文章
    #hot = Article.objects.all().order_by('?')[:10]#随机推荐
    #hot = Article.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('-views')[:10]#通过浏览数进行排序,倒序
    link = Link.objects.all() # 链接
    
    return render(request, 'index.html', locals())

#列表页
def list(request,lid):
    list = Article.objects.filter(category_id=lid) #获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid) #获取当前文章的栏目名

    page = request.GET.get('page')#在URL中获取当前页面数
    paginator = Paginator(list, 5)#对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)#获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'list.html', locals())

#内容页
def show(request,sid):
    show = Article.objects.get(id=sid)#查询指定ID的文章
    hot = Article.objects.all().order_by('?')[:10]#内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    all_comment = Comments.objects.all().filter(article_id=sid)
    # 访问次数+1
    show.views = show.views + 1
    show.save()

    return render(request, 'show.html', locals())

#标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)#通过文章标签进行查询文章
    tname = Tag.objects.get(name=tag)#获取当前搜索的标签名
    page = request.GET.get('page')
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'tags.html', locals())

# 搜索页
def search(request):
    ss=request.GET.get('search')#获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)#获取到搜索关键词通过标题进行匹配
    page = request.GET.get('page')
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'search.html', locals())

# 关于我们
def about(request):
    return render(request, 'page.html',locals())

# 添加评论
def add_comment(request):
    
    article = request.POST.get('article',None)
    content = request.POST.get('content',None)
    created_time = time.time()

    comments_arr = Comments.objects.filter(article_id=article) #查询指定ID的文章
    comments_len = len(comments_arr)
    comments_len+=1
    username = '匿名用户' + str(comments_len)

    add_comments = Comments(article_id=article,content=content,created_time=created_time,username=username)
    add_comments.save()
    return HttpResponse('{"status": "success"}', content_type='application/json')

# 404
def page_not_found(request):
    return render(request, '404.html')

# python应用
def application(request):
    return render(request, 'application/index.html')

# 百度热点数据
def baidu_hot_data(request):
    # file_path = 'D:\\python\data.json'
    # #file_path = '/www/myblog/data/data.json'
    # fb = open(file_path, 'r')
    # dicts = json.load(fb)
    # fb.close()
    # data = json.dumps(dicts)
    # 获取网站首页全部内容
    cnt = 50 #只能1-50
    time_s = round(time.time() * 1000)
    time_s = time_s.__str__()
    url = 'https://zhidao.baidu.com/question/api/hotword?rn='+cnt.__str__()+'&t='+time_s
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    dataList = json.loads(content)['data'][0:15]

    data = json.dumps(dataList)
    return HttpResponse(data, content_type='application/json')

# 机器人聊天
def robot_chat(request):
    text = request.GET.get('text')
    data = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": text
            }
        },
        "userInfo": {
            "apiKey": "d1375188443743699e7d3b73f4040e2b",
            "userId": "441c7926f4c8da1d"
        }
    }
    res = requests.post("http://openapi.tuling123.com/openapi/api/v2",json=data)
    # new_res = res.json().get("results")[0].get("values").get("text")
    return HttpResponse(res, content_type='application/json') # 规定了返回的类型，数据就必须是规定的类型

# from common.GetContensByUrl import GetContensByUrl
import re
# 爬虫抓取内容
def scapy_contents(request):
    sleep(3)
    request_url = request.GET.get('request_url')
    content_type = request.GET.get('content_type')

    res = requests.get(request_url)
    res.encoding = 'utf-8'
    html = res.text
    
    bf = BeautifulSoup(html, 'html.parser')
    bf.prettify()
    texts = bf.find_all('img')


    # 打开「detail_content」文件
    fout = open('test.txt', 'w', encoding='utf8')
    # 写入文件内容
    fout.write(html)
    #关闭文件
    fout.close()
    return HttpResponse(texts)
