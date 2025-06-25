from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from ys import models
from django.db.models import Q
import json
import akshare as ak
import pandas as pd
# Create your views here.


def index(request):
    search = request.GET.get('search')
    if search:
        posts = models.Post.objects.filter(
            Q(title__contains=search) | Q(author__name__contains=search) | Q(content__contains=search))
    else:
        posts = models.Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def article(request, id_):
    post = models.Post.objects.filter(id=id_)
    if not post:
        return HttpResponse('文章不存在')
    post = post.first()
    comments = models.Comment.objects.filter(post=post)
    like_nums = models.Like.objects.filter(post=post).count()
    favorite_nums = models.Favorite.objects.filter(post=post).count()
    form = {
        'post': post,
        'comments': comments,
        'flag': False,
        'like_nums': like_nums,
        'favorite_nums': favorite_nums,
    }
    # print(post.author.id, request.session['info']['id'])
    if request.session.get('info') and post.author.id == request.session['info']['id']:
        form['flag'] = True
    return render(request, 'open_article.html', form)

def main(request):
    form = {}
    return render(request, 'main.html',form)

def api(request):
    if request.method == 'POST':
        data0 = json.loads(request.body.decode('utf-8'))
        input_data = data0.get('input_data')
        '''
        "stock_info_sz_name_code"  # 深证证券交易所股票代码和简称
         "stock_info_sh_name_code"  # 上海证券交易所股票代码和简称
         "stock_info_bj_name_code"  # 北京证券交易所股票代码和简称'''
        # print(input_data)
        data, first, new_data = profitability(input_data)
        data2, first2 = solvency(input_data)
        data3, first3 = money(input_data)
        # 加权净资产收益率（加权ROE =归属于母公司所有者的净利润 / 归属于母公司股东权益合计# 归属于母公司所有者的净利润 资产负债表：归属于母公司股东权益合计
        p1 = first['归属于母公司所有者的净利润'][0] / first2['归属于母公司股东权益合计'][0] * 100
        # 净利润同比增速
        p2 = (first['净利润'][0] - first['净利润'][4]) / first['净利润'][4] * 100
        # 总资产周转率
        p3 = first['营业收入'][0] / (first2['资产总计'][0] + first2['资产总计'][1]) * 2 * 100
        # 销售现金比率
        p4 = first3['销售商品、提供劳务收到的现金'][0] / first['营业收入'][0] * 100
        # 资产负债率
        p5 = first2['负债合计'][0] / first2['资产总计'][0] * 100
        # pie = [[first['净利润'][i],first['报告日'][i]]  for i in range(1, 5)]
        pie = [{'value': first['营业收入'][i], 'name': str(first['报告日'][i])[:10]} for i in range(1, 5)]
        # print(pie)
        form = {
            'data1':data,
            'data2':data2,
            'leida': [round(p1, 2), round(p2, 2), round(p3, 2), round(p4, 2), round(p5, 2), ],
            'pie': pie,
            'new_data':new_data,
        }
        return JsonResponse(form)

# 盈利能力
def profitability(stock):
    df = ak.stock_financial_report_sina(stock=stock, symbol="利润表")
    # df.to_excel("利润表.xlsx")
    df['报告日'] = pd.to_datetime(df['报告日'])
    # 提取年份
    df['年份'] = df['报告日'].dt.year
    first = df.head(6).to_dict(orient='list')
    new_data = df[df['报告日'].dt.year > 2019][['报告日', '营业收入', '营业成本']].reset_index()
    new_data['报告日'] =  new_data['报告日'].astype(str).str[:10]
    new_data['营业收入'] = new_data['营业收入'] / 100000000
    new_data['营业成本'] = new_data['营业成本'] / 100000000
    new_data = new_data.sort_values(by='报告日')
    new_data = new_data.to_dict(orient='list')
    # to_dict(orient='list'))
    # 按年份汇总
    df = df.groupby('年份')[['营业收入', '营业成本', '营业利润', '净利润']].sum().reset_index()
    df = df[(df['年份'] > 2019) & (df['年份'] < 2025)]
    df['毛利率'] = (df['营业收入'] - df['营业成本']) / df['营业收入']*100
    df['营业利润率'] = df['营业利润'] / df['营业收入']*100
    df['净利率'] = df['净利润'] / df['营业收入']*100
    dict_data = df.to_dict(orient='list')
    # df.to_excel("盈利能力.xlsx")
    return dict_data, first, new_data

# 短期偿债能力
def solvency(stock):
    df = ak.stock_financial_report_sina(stock=stock, symbol="资产负债表")
    # df.to_excel("资产负债表.xlsx")
    df['报告日'] = pd.to_datetime(df['报告日'])
    # 提取年份
    df['年份'] = df['报告日'].dt.year
    first = df.head(6).to_dict(orient='list')
    # 按年份汇总
    df = df.groupby('年份')[['流动资产合计', '流动负债合计', '存货', '预付款项', '负债合计', '资产总计']].sum().reset_index()
    df = df[(df['年份'] > 2019) & (df['年份'] < 2025)]
    df['流动比率'] = df['流动资产合计'] / df['流动负债合计']
    df['速动比率'] = (df['流动资产合计'] - df['存货'] - df['预付款项']) / df['流动负债合计']
    df['资产负债率'] = df['负债合计'] / df['资产总计']*100
    dict_data = df.to_dict(orient='list')
    # print(dict_data)
    # df.to_excel("短期偿债能力.xlsx")
    return dict_data, first

def money(stock):
    df = ak.stock_financial_report_sina(stock=stock, symbol="现金流量表")
    df['报告日'] = pd.to_datetime(df['报告日'])
    # 提取年份
    df['年份'] = df['报告日'].dt.year
    first = df.head(6).to_dict(orient='list')
    df = df[(df['年份'] > 2019) & (df['年份'] < 2025)]
    dict_data = df.to_dict(orient='list')
    return dict_data, first
