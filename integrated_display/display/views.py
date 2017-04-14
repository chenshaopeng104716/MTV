#coding:utf-8
from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from .models import *
from django.http import  HttpResponseRedirect,HttpResponse
from django.db import connection
from SQLclass import Newmofang
import pandas as pd
import datetime
import time
import json
import operator
import psycopg2
import MySQLdb
# Create your views here.
import sys
reload(sys)
sys.setdefaultencoding('utf8')


###全平台模块
def platform(request):
    start_time = time.time()
    if request.method == 'GET':
        calculate_date = datetime.datetime.now()-datetime.timedelta(days=1)
    elif request.method == 'POST':
        post_date = request.POST.get('search_date')
        calculate_date = datetime.datetime.strptime(post_date, "%Y-%m-%d")

    ###日期计算
    start_date, end_date, end_date_show, last_week_start_date, last_week_end_date, \
    last_2week_start_date, last_2week_end_date, month_to_month_date,year_to_year_date,date_str = date_calculate(calculate_date)

    ###初始化类
    platform_class = Newmofang(start_date=start_date,end_date=end_date,last_week_start_date=last_week_start_date,last_week_end_date=last_week_end_date)
    ###查询月vv
    vv_month_sql = platform_class.module_search(searchtype='platform_vv_month')

    ###查询日vv
    vv_day_sql = platform_class.module_search(searchtype='platform_vv_day')

    ###查询日uv
    uv_day_sql = platform_class.module_search(searchtype='platform_uv_day')
    ###查询日pv
    pv_day_sql = platform_class.module_search(searchtype='platform_pv_day')
    ###查询日时长
    duration_day_sql = platform_class.module_search(searchtype='platform_duration_day')
    ###查询全平台kpi完成情况
    kpi_platform_sql = platform_class.module_search(searchtype='platform_kpi')
    # print kpi_platform_sql
    ###查询终端vv、uv
    date_list = platform_class.datetime_process()
    terminal_list = platform_class.bid_dict.values()
    vv_terminal_day_sql = platform_class.module_search(searchtype='platform_vv_terminal_day')
    # print vv_terminal_day_result
    uv_terminal_day_sql = platform_class.module_search(searchtype='platform_uv_terminal_day')


    ###查询频道vv、uv
    channel_list = platform_class.cid_dict.values()
    vv_channel_day_sql = platform_class.module_search(searchtype='platform_vv_channel_day')
    uv_channel_day_sql = platform_class.module_search(searchtype='platform_uv_channel_day')

    ###查询dau
    dau_platform_day_sql = platform_class.module_search(searchtype='platform_dau_day')

    ###查询最近一周的日均uv、日均vv
    uv_pid_day_avg_sql = platform_class.module_search(searchtype='platform_uv_pid_day_avg')###合集日均uvtop20

    ###合并sql,一次查询
    sql_combine = Newmofang().sql_union(vv_month_sql,vv_day_sql,uv_day_sql,pv_day_sql,duration_day_sql,kpi_platform_sql,vv_terminal_day_sql,uv_terminal_day_sql,
                                        vv_channel_day_sql,uv_channel_day_sql,dau_platform_day_sql,uv_pid_day_avg_sql)
    all_result = Newmofang().sql_query(sql_combine)
    ###利用pandas包把all_result分到不同的查询
    vv_month_result = all_result[all_result['module_name']=='platform_vv_month'].sort(['col1'])
    vv_day_result = all_result[all_result['module_name']=='platform_vv_day'].sort(['col1'])
    uv_day_result = all_result[all_result['module_name']=='platform_uv_day'].sort(['col1'])
    pv_day_result = all_result[all_result['module_name']=='platform_pv_day'].sort(['col1'])
    duration_day_result = all_result[all_result['module_name']=='platform_duration_day'].sort(['col1'])
    kpi_platform_result = all_result[all_result['module_name']=='platform_kpi'].sort(['col1'])
    vv_terminal_day_result = all_result[all_result['module_name']=='platform_vv_terminal_day'].sort(['col1'])
    uv_terminal_day_result = all_result[all_result['module_name'] == 'platform_uv_terminal_day'].sort(['col1'])
    vv_channel_day_result = all_result[all_result['module_name'] == 'platform_vv_channel_day'].sort(['col1'])
    uv_channel_day_result = all_result[all_result['module_name'] == 'platform_uv_channel_day'].sort(['col1'])
    dau_platform_day_result = all_result[all_result['module_name'] == 'platform_dau_day'].sort(['col1'])
    uv_pid_day_avg_result = all_result[all_result['module_name'] == 'platform_uv_pid_day_avg']
    pid_list = uv_pid_day_avg_result['col1'].tolist()###获取pid列表
    pid_list_to_str = map(lambda x:str(x),pid_list)
    pid_str = ','.join(pid_list_to_str)###合集id列表，供vv查询用
    vv_pid_day_avg_sql = Newmofang(last_week_start_date=last_week_start_date,pid_str=pid_str,last_week_end_date=last_week_end_date).module_search(searchtype='platform_vv_pid_day_avg') ###合集日均uvtop20
    vv_pid_day_avg_result = Newmofang().sql_query(vv_pid_day_avg_sql)

    ###数据处理
    pid_day_avg_result = platform_pid_day_avg_result_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)

    kpi_ratio = kpi_platform_process(kpi_platform_result)

    overview_platform_day_dict = overview_platform_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,pv_day_result,duration_day_result)###往日概览数据
    vv_month_date, vv_month_lastyear, vv_month_thisyear = vv_month_process(vv_month_result=vv_month_result)###平台月度uv数据
    vv_day_date, vv_day_data, uv_day_data = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)###全平台日vv、uv、人均vv数据
    vv_terminal_day_dict = vv_terminal_day_process(vv_terminal_day_result=vv_terminal_day_result,terminal_list=terminal_list)  ###分端vv变化
    uv_terminal_day_dict = uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result,terminal_list=terminal_list)  ###分端uv变化
    vv_channel_day_dict = vv_channel_day_process(vv_channel_day_result=vv_channel_day_result,channel_list=channel_list)  ###分频道vv变化
    uv_channel_day_dict = uv_channel_day_process(uv_channel_day_result=uv_channel_day_result,channel_list=channel_list)  ###分频道uv变化
    dau_day_data, uv_ration_day_data = dau_day_process(dau_platform_day_result=dau_platform_day_result,uv_day_result=uv_day_result)

    end_time = time.time()
    print 'time elapse is %s'%(end_time-start_time)
    return render(request, 'index.html', {'kpi_ratio':kpi_ratio,'vv_day_date':json.dumps(vv_day_date),'vv_day_data':json.dumps(vv_day_data),
                                       'uv_day_data': json.dumps(uv_day_data),'vv_month_date':json.dumps(vv_month_date),
                                          'vv_month_lastyear':json.dumps(vv_month_lastyear),'vv_month_thisyear':json.dumps(vv_month_thisyear),
                                          'vv_terminal_day_dict':vv_terminal_day_dict,'uv_terminal_day_dict':uv_terminal_day_dict,'vv_channel_day_dict':vv_channel_day_dict,
                                       'uv_channel_day_dict':uv_channel_day_dict,'dau_day_data':dau_day_data,'uv_ration_day_data':uv_ration_day_data,
                                        'overview_platform_day_dict':overview_platform_day_dict,'pid_day_avg_result':json.dumps(pid_day_avg_result),
                                          'date_str':date_str})

def ltt(request):
    pass


def channel(request):
    start_time = time.time()
    path = request.get_full_path()
    channel_dict = {'show':'综艺','tv':'电视剧','movie':'电影','cartoon':'动漫'}
    channel_name = request.GET.get('name')###获取url中传过来的参数
    channel_name_eng = channel_name###后续post需要该参数
    if request.method == 'GET':
        calculate_date = datetime.datetime.now() - datetime.timedelta(days=1)
    elif request.method == 'POST':
        post_date = request.POST.get('search_date')###获取post表单中的参数
        calculate_date = datetime.datetime.strptime(post_date, "%Y-%m-%d")

    start_date, end_date, end_date_show, last_week_start_date, last_week_end_date, \
    last_2week_start_date, last_2week_end_date, month_to_month_date,year_to_year_date,date_str = date_calculate(calculate_date)

    ###初始类
    channel_class = Newmofang(channel_name=channel_name,start_date=start_date,end_date=end_date,
                              last_week_start_date=last_week_start_date,last_week_end_date=last_week_end_date,
                              last_2week_start_date=last_2week_start_date,last_2week_end_date=last_2week_end_date)

    ###查询月vv
    vv_month_sql = channel_class.module_search(searchtype='channel_vv_month')

    ###查询日vv
    vv_day_sql = channel_class.module_search(searchtype='channel_vv_day')

    ###查询日uv
    uv_day_sql = channel_class.module_search(searchtype='channel_uv_day')

    ###查询日时长
    duration_day_sql = channel_class.module_search(searchtype='channel_duration_day')
    ###查询频道kpi完成情况
    kpi_channel_sql = channel_class.module_search(searchtype='channel_kpi')
    # print kpi_platform_sql
    ###查询终端vv、uv
    date_list = channel_class.datetime_process()
    terminal_list = channel_class.bid_dict.values()
    vv_terminal_day_sql = channel_class.module_search(searchtype='channel_vv_terminal_day')
    # print vv_terminal_day_result
    uv_terminal_day_sql = channel_class.module_search(searchtype='channel_uv_terminal_day')

    ###查询上一周的vvtop50
    pid_vv_week_ago_sql = channel_class.module_search(searchtype='channel_pid_vv_change')

    ###查询最近一周的日均uv、日均vv
    uv_pid_day_avg_sql = channel_class.module_search(searchtype='channel_uv_pid_day_avg')###合集日均uvtop20

    ###合并sql,一次查询
    sql_combine = Newmofang().sql_union(vv_month_sql,vv_day_sql,uv_day_sql,duration_day_sql,kpi_channel_sql,vv_terminal_day_sql,uv_terminal_day_sql,
                                        uv_pid_day_avg_sql,pid_vv_week_ago_sql)
    all_result = Newmofang().sql_query(sql_combine)

    ###利用pandas包把all_result分到不同的查询
    vv_month_result = all_result[all_result['module_name']=='channel_vv_month'].sort(['col1'])
    vv_day_result = all_result[all_result['module_name']=='channel_vv_day'].sort(['col1'])
    uv_day_result = all_result[all_result['module_name']=='channel_uv_day'].sort(['col1'])
    duration_day_result = all_result[all_result['module_name']=='channel_duration_day'].sort(['col1'])
    kpi_channel_result = all_result[all_result['module_name']=='channel_kpi'].sort(['col1'])
    vv_terminal_day_result = all_result[all_result['module_name']=='channel_vv_terminal_day'].sort(['col1'])
    uv_terminal_day_result = all_result[all_result['module_name'] == 'channel_uv_terminal_day'].sort(['col1'])
    uv_pid_day_avg_result = all_result[all_result['module_name'] == 'channel_uv_pid_day_avg']
    pid_vv_week_ago_result = all_result[all_result['module_name'] == 'channel_pid_vv_change_this']

    pid_week_list = pid_vv_week_ago_result['col1'].tolist()
    pid_week_list_to_str = map(lambda x:str(x),pid_week_list)###转化为字符串传入sql
    pid_week_str = ','.join(pid_week_list_to_str)###前一周的合集vvtop中的pid列表

    pid_vv_2week_ago_sql = Newmofang(channel_name=channel_name,last_2week_start_date=last_2week_start_date,pid_str=pid_week_str,last_2week_end_date=last_2week_end_date).module_search(searchtype='channel_pid_vv_change')
    pid_vv_2week_ago_result = Newmofang().sql_query(pid_vv_2week_ago_sql)
    # print 'pid_vv_week_ago_result:',pid_vv_week_ago_result,'pid_vv_2week_ago_result:',pid_vv_2week_ago_result

    pid_vv_change_dict = channel_pid_vv_change_process(pid_week_str, pid_vv_week_ago_result, pid_vv_2week_ago_result)

    ###根据uv top20的pid列表查询对应的vv
    pid_list = uv_pid_day_avg_result['col1'].tolist()###获取pid列表
    pid_list_to_str = map(lambda x:str(x),pid_list)###转化为字符串传入sql
    pid_str = ','.join(pid_list_to_str)###合集id列表，供vv查询用
    # print pid_str
    vv_pid_day_avg_sql = Newmofang(channel_name=channel_name,last_week_start_date=last_week_start_date,pid_str=pid_str,last_week_end_date=last_week_end_date).module_search(searchtype='channel_vv_pid_day_avg') ###合集日均uvtop20
    vv_pid_day_avg_result = Newmofang().sql_query(vv_pid_day_avg_sql)

    # ###vv、uv条形图
    # pid_bar_dict = channel_pid_day_avg_bar_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)
    # print pid_bar_dict
    ###vv、uv气泡图
    pid_day_avg_result = channel_pid_day_avg_result_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)


    ###数据转化为列表传入前端
    kpi_ratio = kpi_channel_process(kpi_channel_result,channel_name)

    overview_channel_day_dict = overview_channel_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,duration_day_result)###往日概览数据
    vv_month_date, vv_month_lastyear, vv_month_thisyear = vv_month_process(vv_month_result=vv_month_result)###平台月度uv数据
    vv_day_date, vv_day_data, uv_day_data = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)###全平台日vv、uv、人均vv数据
    vv_terminal_day_dict = vv_terminal_day_process(vv_terminal_day_result=vv_terminal_day_result,terminal_list=terminal_list)  ###分端vv变化
    uv_terminal_day_dict = uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result,terminal_list=terminal_list)  ###分端uv变化
    end_time = time.time()
    print 'time elapse is %s'%(end_time-start_time)
    return render(request,'channel_ltt.html',{'path':path,'vv_month_date':json.dumps(vv_month_date),'vv_month_lastyear':json.dumps(vv_month_lastyear),'channel_name_eng':channel_name_eng,
                                   'vv_month_thisyear':json.dumps(vv_month_thisyear),'date_str':date_str,'channel_name':json.dumps([channel_dict[channel_name]]),
                                        'kpi_ratio':kpi_ratio,'overview_channel_day_dict':overview_channel_day_dict,'channel_name_div':[channel_dict[channel_name]],
                                          'vv_day_data': json.dumps(vv_day_data),'uv_day_data':json.dumps(uv_day_data),'vv_day_date':json.dumps(vv_day_date),
                                          'vv_terminal_day_dict': vv_terminal_day_dict,'uv_terminal_day_dict': uv_terminal_day_dict,
                                          'pid_day_avg_result': json.dumps(pid_day_avg_result),'pid_vv_change_dict':json.dumps(pid_vv_change_dict),})

def date_calculate(calculate_date):
    start_date = (calculate_date - datetime.timedelta(days=29)).date().strftime('%Y%m%d')  ###查询开始时间
    end_date = calculate_date.date().strftime('%Y%m%d')  ###查询结束时间

    end_date_show = calculate_date.date().strftime('%Y.%m.%d')  ###在页面显示需要的数据格式
    if calculate_date.isoweekday() == 7:  ###判断计算日期是否为星期天最近一周的开始时间有区别
        last_week_start_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday() - 1)).date().strftime(
            '%Y%m%d')  ###最近一周的开始日期
        last_week_end_date = calculate_date.date().strftime('%Y%m%d')  ###最近一周的结束日期
        last_2week_start_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday() + 6)).date().strftime(
            '%Y%m%d')  ###最近二周前的开始日期
        last_2week_end_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday())).date().strftime(
            '%Y%m%d')  ###最近二周前的结束日期
    else:
        last_week_start_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday() + 6)).date().strftime(
            '%Y%m%d')  ###最近一周的开始日期
        last_week_end_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday())).date().strftime(
            '%Y%m%d')  ###最近一周的结束日期
        last_2week_start_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday() + 13)).date().strftime(
            '%Y%m%d')  ###最近二周前的开始日期
        last_2week_end_date = (
        calculate_date - datetime.timedelta(days=calculate_date.isoweekday() + 7)).date().strftime(
            '%Y%m%d')  ###最近二周前的结束日期

    month_to_month_date = (calculate_date - datetime.timedelta(days=1)).date().strftime('%Y%m%d')  ###环比的日期，2天前
    year_to_year_date = (calculate_date - datetime.timedelta(days=7)).date().strftime('%Y%m%d')  ###同比的日期，8天前

    ###每日概况及最后的重点节目的前端日期字符串

    date_str = [end_date_show, last_week_start_date + '-' + last_week_end_date ]
    return start_date,end_date,end_date_show,last_week_start_date,last_week_end_date,last_2week_start_date,\
           last_2week_end_date,month_to_month_date,year_to_year_date,date_str


def kpi_platform_process(kpi_platform_result):
    ###每季度的kpi目标
    kpi_target = 10000
    kpi_now = kpi_platform_result['num'].unique()
    kpi_ratio = round(kpi_now/kpi_target*100,2)
    return kpi_ratio

def kpi_channel_process(kpi_channel_result,channel_name):
    ###每季度的kpi目标
    kpi_target_dict = {'show':3500,'tv':3500,'movie':600,'cartoon':2200,'music':60}
    kpi_target = kpi_target_dict[channel_name]
    kpi_now = kpi_channel_result['num'].unique()
    kpi_ratio = round(kpi_now/kpi_target*100,2)
    return kpi_ratio


def overview_platform_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,pv_day_result,duration_day_result):###处理往日概况模块,暂定为昨日vv、uv、pv、时长数据
    days_ago_location = date_list.index(end_date)###昨日日期在日期列表中的位置
    month_to_month_location = date_list.index(month_to_month_date)###环比日期在日期列表中的位置
    year_to_year_location = date_list.index(year_to_year_date)###同比日期在日期列表中的位置
    # print days_ago_location,month_to_month_location,year_to_year_location
    vv_result = vv_day_result[['col1','num']]
    vv_result.columns = ['date','vv']
    uv_result = uv_day_result[['col1', 'num']]
    uv_result.columns = ['date', 'uv']
    pv_result = pv_day_result[['col1', 'num']]
    pv_result.columns = ['date', 'pv']
    duration_result = duration_day_result[['col1', 'num']]
    duration_result.columns = ['date', 'duration']
    data_all = pd.merge(vv_result,uv_result)###合并数据
    data_all = pd.merge(data_all,pv_result)
    data_all = pd.merge(data_all,duration_result)
    data_all['vv_perperson'] = map(lambda x, y: round(x / y, 1), data_all['vv'], data_all['uv'])  ###计算人均vv
    data_all['duration_perperson'] = map(lambda x, y: round(x / y, 1), data_all['duration'],data_all['uv'])   ###计算人均观看时长列表

    ###计算列表
    key_list = ['vv','uv','pv','vv_perperson','duration_perperson']
    overview_platform_day_dict = {}
    ###计算概览数据,每个部分的数据均以 [昨日数据，环比，同比] 进行显示
    for key in key_list:
        x = data_all[key]
        overview_result = ['%.1f'%x[days_ago_location],'%.2f'%round((x[days_ago_location]/x[month_to_month_location]-1)*100,2),'%.2f'%round((x[days_ago_location]/x[year_to_year_location]-1)*100,2)]
        overview_platform_day_dict[key] = overview_result
    # print overview_platform_day_dict
    return overview_platform_day_dict
    # overview_platform_day_dict['vv'] = [vv_day_data[days_ago_location],round(vv_day_data[days_ago_location]/vv_day_data[month_to_month_location]-1]

def overview_channel_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,duration_day_result):###处理往日概况模块,暂定为昨日vv、uv、pv、时长数据
    days_ago_location = date_list.index(end_date)###昨日日期在日期列表中的位置
    month_to_month_location = date_list.index(month_to_month_date)###环比日期在日期列表中的位置
    year_to_year_location = date_list.index(year_to_year_date)###同比日期在日期列表中的位置
    # print days_ago_location,month_to_month_location,year_to_year_location
    vv_result = vv_day_result[['col1','num']]
    vv_result.columns = ['date','vv']
    uv_result = uv_day_result[['col1', 'num']]
    uv_result.columns = ['date', 'uv']
    duration_result = duration_day_result[['col1', 'num']]
    duration_result.columns = ['date', 'duration']
    data_all = pd.merge(vv_result,uv_result)###合并数据
    data_all = pd.merge(data_all,duration_result)
    data_all['vv_perperson'] = map(lambda x, y: round(x / y, 1), data_all['vv'], data_all['uv'])  ###计算人均vv
    data_all['duration_perperson'] = map(lambda x, y: round(x / y, 1), data_all['duration'],data_all['uv'])   ###计算人均观看时长列表

    ###计算列表
    key_list = ['vv','uv','vv_perperson','duration_perperson']
    overview_platform_day_dict = {}
    ###计算概览数据,每个部分的数据均以 [昨日数据，环比，同比] 进行显示
    for key in key_list:
        x = data_all[key]
        overview_result = ['%.1f'%x[days_ago_location],'%.2f'%round((x[days_ago_location]/x[month_to_month_location]-1)*100,2),'%.2f'%round((x[days_ago_location]/x[year_to_year_location]-1)*100,2)]
        overview_platform_day_dict[key] = overview_result
    # print overview_platform_day_dict
    return overview_platform_day_dict
    # overview_platform_day_dict['vv'] = [vv_day_data[days_ago_location],round(vv_day_data[days_ago_location]/vv_day_data[month_to_month_location]-1]

###频道模块合集条形图数据计算
def channel_pid_day_avg_bar_process(pid_str,vv_pid_day_avg_result,uv_pid_day_avg_result):
    cms_result = Newmofang(pid_str=pid_str).cms_sql().drop_duplicates()
    print cms_result
    pid_list = map(lambda x: str(x[0]), uv_pid_day_avg_result)
    pid_list.reverse()
    pid_name_list = []
    pid_uv_list = []
    pid_vv_list = []
    for pid in pid_list:
        for cms_each in cms_result:
            for vv_each in vv_pid_day_avg_result:
                for uv_each in uv_pid_day_avg_result:
                    if str(pid) == str(cms_each[0]) and str(pid) == str(vv_each[0]) and str(pid) == str(uv_each[0]):
                        pid_name_list.append(cms_each[1])
                        pid_uv_list.append(round(uv_each[1]/10000))
                        pid_vv_list.append(round(vv_each[1]/10000))
    pid_bar_dict = {}
    pid_bar_dict['name'] = pid_name_list
    pid_bar_dict['vv'] = pid_vv_list
    pid_bar_dict['uv'] = pid_uv_list
    return pid_bar_dict

###频道模块合集vv涨跌幅top10数据计算
def channel_pid_vv_change_process(pid_week_str,pid_vv_week_ago_result,pid_vv_2week_ago_result):
    cms_result = Newmofang(pid_str=pid_week_str).cms_sql().drop_duplicates()
    vv_week_ago_result = pid_vv_week_ago_result[['col1','num']]###取出需要的列，重命名
    vv_week_ago_result.columns = ['pid','vv_week_ago']
    vv_2week_ago_result = pid_vv_2week_ago_result[['col1','num']]###取出需要的列，重命名
    vv_2week_ago_result.columns = ['pid','vv_2week_ago']
    dataframe_all = pd.merge(cms_result,vv_week_ago_result,how='inner',on='pid')
    dataframe_all = pd.merge(dataframe_all,vv_2week_ago_result,how='inner',on='pid')
    dataframe_all['vv_diff'] = map(lambda x,y:round(100*(x-y)/y),dataframe_all['vv_week_ago'],dataframe_all['vv_2week_ago'])
   ###针对两周vv的差值百分比进行排序
    dataframe_all = dataframe_all.sort('vv_diff')
    ###涨幅部分
    pid_vv_change_increase = dataframe_all[dataframe_all['vv_diff']>0][-10:]
    pid_vv_change_increase_name = pid_vv_change_increase['pid_title'].tolist()###涨幅top10的合集名称
    pid_vv_change_increase_vv = pid_vv_change_increase['vv_diff'].tolist()###涨幅top10的vv差值
    ###降幅部分
    pid_vv_change_decrease = dataframe_all[dataframe_all['vv_diff']<0][:10]
    pid_vv_change_decrease = pid_vv_change_decrease.sort('vv_diff',ascending=False)
    pid_vv_change_decrease_name = pid_vv_change_decrease['pid_title'].tolist()###降幅top10的合集名称
    pid_vv_change_decrease_vv = pid_vv_change_decrease['vv_diff'].tolist()###降幅top10的vv差值

    ###放入字典
    pid_vv_change_dict = {}
    pid_vv_change_dict['decrease_name'] = pid_vv_change_decrease_name
    pid_vv_change_dict['decrease_vv'] = pid_vv_change_decrease_vv
    pid_vv_change_dict['increase_name'] = pid_vv_change_increase_name
    pid_vv_change_dict['increase_vv'] = pid_vv_change_increase_vv
    print pid_vv_change_dict
    return pid_vv_change_dict



###平台模块合集气泡图数据计算
def platform_pid_day_avg_result_process(pid_str,vv_pid_day_avg_result,uv_pid_day_avg_result):
    cms_result = Newmofang(pid_str=pid_str).cms_sql().drop_duplicates()
    # print cms_result
    vv_result = vv_pid_day_avg_result[['col1','num']]###取出需要的列，重命名
    vv_result.columns = ['pid','vv']
    uv_result = uv_pid_day_avg_result[['col1','num']]
    uv_result.columns = ['pid','uv']
    dataframe_all = pd.merge(cms_result,vv_result,how='inner',on='pid')
    dataframe_all = pd.merge(dataframe_all,uv_result,how='inner',on='pid')
    dataframe_all['vv/uv'] = map(lambda x, y: round(x / y, 2), dataframe_all['vv'], dataframe_all['uv'])###计算人均vv
    list_all = []
    for index, row in dataframe_all.iterrows():###取出每一行需要的数据
        list_all.append(row[['uv', 'vv', 'vv/uv', 'pid_title', 'bid_title']].tolist())
    ###总的list,根据echarts中js需要的数据格式，最后的结构为 [[综艺频道数据],[电视剧频道数据]]，每个频道数据为[vv,uv,人均vv,合集名称,频道名称]
    pid_day_avg_result = []
    ###各频道list
    show_day_avg_result = filter(lambda x:x[4]==u'综艺',list_all)###综艺
    tv_day_avg_result = filter(lambda x:x[4]==u'电视剧',list_all)###电视剧
    movie_day_avg_result = filter(lambda x:x[4]==u'电影',list_all)  ###电影
    cartoon_day_avg_result = filter(lambda x:x[4]==u'动漫',list_all)  ###动漫
    pid_day_avg_result.extend([show_day_avg_result,tv_day_avg_result,movie_day_avg_result,cartoon_day_avg_result])
    return pid_day_avg_result


###频道模块合集气泡图数据计算
def channel_pid_day_avg_result_process(pid_str,vv_pid_day_avg_result,uv_pid_day_avg_result):
    cms_result = Newmofang(pid_str=pid_str).cms_sql().drop_duplicates()
    # print cms_result
    vv_result = vv_pid_day_avg_result[['col1','col2','num']]###取出需要的列，重命名
    vv_result.columns = ['bid_name','pid','vv']
    uv_result = uv_pid_day_avg_result[['col1','col2','num']]
    uv_result.columns = ['pid','bid_name','uv']
    dataframe_all = pd.merge(cms_result,vv_result,how='inner',on=['pid'])
    dataframe_all = pd.merge(dataframe_all,uv_result,how='inner',on=['pid','bid_name'])
    dataframe_all['vv/uv'] = map(lambda x, y: round(x / y, 2), dataframe_all['vv'], dataframe_all['uv'])###计算人均vv
    list_all = []
    for index, row in dataframe_all.iterrows():###取出每一行需要的数据
        list_all.append(row[['uv', 'vv', 'vv/uv', 'pid_title', 'bid_name']].tolist())
    ###总的list,根据echarts中js需要的数据格式，最后的结构为 [[pcweb数据],[[android数据]]，每个终端数据为[vv,uv,人均vv,合集名称,终端名称]
    pid_day_avg_result = []
    ###各终端list
    pcweb_day_avg_result = filter(lambda x:x[4]=='pcweb',list_all)###pcweb
    android_day_avg_result = filter(lambda x:x[4]=='android',list_all)###android
    iphone_day_avg_result = filter(lambda x:x[4]=='iphone',list_all)  ###iphone
    ott_day_avg_result = filter(lambda x:x[4]=='ott',list_all)  ###ott
    pid_day_avg_result.extend([pcweb_day_avg_result,android_day_avg_result,iphone_day_avg_result,ott_day_avg_result])
    return pid_day_avg_result



###月vv数据处理
def vv_month_process(vv_month_result):
    vv_month_data = vv_month_result['num'].tolist()
    ###月份列表
    vv_month_date = [str(i) + '月' for i in range(1, 13)]
    ###第一年vv
    vv_month_lastyear = vv_month_data[:12]
    vv_month_thisyear = vv_month_data[12:]
    return vv_month_date,vv_month_lastyear,vv_month_thisyear

###日vv、uv、人均vv处理
def vv_day_process(vv_day_result,uv_day_result):
    vv_day_result.sort('col1')
    uv_day_result.sort('col1')
    vv_day_date = vv_day_result['col1'].tolist()
    vv_day_date = map(lambda x:int(x),vv_day_date)###类型转换，要不然会报错
    vv_day_data = vv_day_result['num'].tolist()
    uv_day_data = uv_day_result['num'].tolist()
    return vv_day_date,vv_day_data,uv_day_data



###日vv分端处理
def vv_terminal_day_process(vv_terminal_day_result,terminal_list):
    vv_terminal_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for terminal in terminal_list:
        terminal_list = vv_terminal_day_result[vv_terminal_day_result['col2']==terminal]['num'].tolist()
        vv_terminal_day_dict[terminal] = terminal_list
    return vv_terminal_day_dict


###日uv分端处理
def uv_terminal_day_process(uv_terminal_day_result,terminal_list):
    uv_terminal_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for terminal in terminal_list:
        terminal_list = uv_terminal_day_result[uv_terminal_day_result['col2'] == terminal]['num'].tolist()
        uv_terminal_day_dict[terminal] = terminal_list
    return uv_terminal_day_dict


###日vv分频道处理
def vv_channel_day_process(vv_channel_day_result,channel_list):
    vv_channel_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for channel in channel_list:
        channel_list = vv_channel_day_result[vv_channel_day_result['col2'] == channel]['num'].tolist()
        vv_channel_day_dict[channel] = channel_list
    return vv_channel_day_dict


###日uv分端处理
def uv_channel_day_process(uv_channel_day_result,channel_list):
    uv_channel_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for channel in channel_list:
        channel_list = uv_channel_day_result[uv_channel_day_result['col2'] == channel]['num'].tolist()
        uv_channel_day_dict[channel] = channel_list
    return uv_channel_day_dict


###日dau处理
def dau_day_process(dau_platform_day_result,uv_day_result):
    dau_result = dau_platform_day_result[['col1','num']]
    dau_result.columns = ['date','dau']
    uv_result = uv_day_result[['col1', 'num']]
    uv_result.columns = ['date', 'uv']
    ###数据汇总
    data_all = pd.merge(dau_result,uv_result)
    ###对应位置相除
    data_all['uv_ration'] = map(lambda x,y:'%.2f'%round(x/y,2),data_all['uv'],data_all['dau'])
    dau_list = data_all['dau'].tolist()
    ration_list = data_all['uv_ration'].tolist()
    return dau_list,ration_list