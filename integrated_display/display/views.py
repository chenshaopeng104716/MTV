#coding:utf-8
from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from .models import *
from django.http import  HttpResponseRedirect,HttpResponse
from django.db import connection
from SQLclass import Newmofang
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

    start_date = (calculate_date - datetime.timedelta(days=29)).date().strftime('%Y%m%d')###查询开始时间
    end_date = calculate_date.date().strftime('%Y%m%d')###查询结束时间

    end_date_show = calculate_date.date().strftime('%Y.%m.%d')###在页面显示需要的数据格式
    if calculate_date.isoweekday() == 7:###判断计算日期是否为星期天最近一周的开始时间有区别
        last_week_start_date = (calculate_date - datetime.timedelta(days=calculate_date.isoweekday()-1)).date().strftime('%Y%m%d')###最近一周的开始日期
        last_week_end_date = calculate_date.date().strftime('%Y%m%d')###最近一周的结束日期
    else:
        last_week_start_date = (calculate_date - datetime.timedelta(days=calculate_date.isoweekday()+6)).date().strftime('%Y%m%d')###最近一周的开始日期
        last_week_end_date = (calculate_date - datetime.timedelta(days=calculate_date.isoweekday())).date().strftime('%Y%m%d')###最近一周的结束日期

    month_to_month_date = (calculate_date - datetime.timedelta(days=1)).date().strftime('%Y%m%d')###环比的日期，2天前
    year_to_year_date = (calculate_date - datetime.timedelta(days=7)).date().strftime('%Y%m%d')###同比的日期，8天前

    ###每日概况及最后的重点节目的前端日期字符串

    date_str = [end_date_show,last_week_start_date+'-'+last_week_end_date]

    ###查询月vv
    vv_month_result = Newmofang(searchtype='platform_vv_month',end_date=end_date).sql_query()

    ###查询日vv
    vv_day_result = Newmofang(searchtype='platform_vv_day',start_date=start_date,end_date=end_date).sql_query()
    ###查询日uv
    uv_day_result = Newmofang(searchtype='platform_uv_day',start_date=start_date,end_date=end_date).sql_query()
    ###查询日pv
    pv_day_result = Newmofang(searchtype='platform_pv_day',start_date=start_date,end_date=end_date).sql_query()
    ###查询日时长
    duration_day_result = Newmofang(searchtype='platform_duration_day',start_date=start_date,end_date=end_date).sql_query()
    ###查询全平台kpi完成情况
    kpi_platform_result = Newmofang(searchtype='platform_kpi',end_date=end_date).sql_query()
    print kpi_platform_result
    ###查询终端vv、uv
    date_list = Newmofang(start_date=start_date, end_date=end_date).datetime_process()
    terminal_list = Newmofang().bid_dict.values()
    vv_terminal_day_result = Newmofang(searchtype='platform_vv_terminal_day',start_date=start_date,end_date=end_date).sql_query()
    # print vv_terminal_day_result
    uv_terminal_day_result = Newmofang(searchtype='platform_uv_terminal_day',start_date=start_date,end_date=end_date).sql_query()


    ###查询频道vv、uv
    channel_list = Newmofang().cid_dict.values()
    vv_channel_day_result = Newmofang(searchtype='platform_vv_channel_day', start_date=start_date, end_date=end_date).sql_query()
    uv_channel_day_result = Newmofang(searchtype='platform_uv_channel_day', start_date=start_date, end_date=end_date).sql_query()

    ###查询dau
    dau_platform_day_result = Newmofang(searchtype='platform_dau_day', start_date=start_date, end_date=end_date).sql_query()

    ###查询最近一周的日均uv、日均vv
    uv_pid_day_avg_result = Newmofang(searchtype='platform_uv_pid_day_avg', start_date=last_week_start_date, end_date=last_week_end_date).sql_query()###合集日均uvtop20
    pid_str = ','.join(map(lambda x: str(x[0]), uv_pid_day_avg_result))###合集id列表，供vv查询用
    vv_pid_day_avg_result = Newmofang(searchtype='platform_vv_pid_day_avg', start_date=last_week_start_date,pid_str=pid_str,end_date=last_week_end_date).sql_query()  ###合集日均uvtop20

    pid_day_avg_result = platform_pid_day_avg_result_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)
    ###数据转化为列表传入前端
    kpi_ratio = kpi_platform_process(kpi_platform_result)
    # print kpi_ratio
    overview_platform_day_dict = overview_platform_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,pv_day_result,duration_day_result)###往日概览数据
    vv_month_date, vv_month_lastyear, vv_month_thisyear = vv_month_process(vv_month_result=vv_month_result)###平台月度uv数据
    vv_day_date, vv_day_data, uv_day_data,vv_day_perperson = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)###全平台日vv、uv、人均vv数据
    vv_terminal_day_dict = vv_terminal_day_process(vv_terminal_day_result=vv_terminal_day_result,date_list=date_list,terminal_list=terminal_list)  ###分端vv变化
    uv_terminal_day_dict = uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result, date_list=date_list,terminal_list=terminal_list)  ###分端uv变化
    vv_channel_day_dict = vv_channel_day_process(vv_channel_day_result=vv_channel_day_result, date_list=date_list,channel_list=channel_list)  ###分频道vv变化
    uv_channel_day_dict = uv_channel_day_process(uv_channel_day_result=uv_channel_day_result, date_list=date_list,channel_list=channel_list)  ###分频道uv变化
    dau_day_data, uv_ration_day_data = dau_day_process(dau_day_result=dau_platform_day_result,uv_day_data=uv_day_data)

    end_time = time.time()
    print 'time elapse is %s'%(end_time-start_time)
    return render(request, 'index.html', {'kpi_ratio':kpi_ratio,'vv_day_date':json.dumps(vv_day_date),'vv_day_data':json.dumps(vv_day_data),
                                       'uv_day_data': json.dumps(uv_day_data),'vv_day_perperson':json.dumps(vv_day_perperson),
                                       'vv_month_date':json.dumps(vv_month_date),'vv_month_lastyear':json.dumps(vv_month_lastyear),
                                       'vv_month_thisyear':json.dumps(vv_month_thisyear),'vv_terminal_day_dict':vv_terminal_day_dict,
                                       'uv_terminal_day_dict':uv_terminal_day_dict,'vv_channel_day_dict':vv_channel_day_dict,
                                       'uv_channel_day_dict':uv_channel_day_dict,'dau_day_data':dau_day_data,'uv_ration_day_data':uv_ration_day_data,
                                        'overview_platform_day_dict':overview_platform_day_dict,'pid_day_avg_result':json.dumps(pid_day_avg_result),
                                          'date_str':date_str})

def ltt(request):
    pass


def channel(request):
    path = request.get_full_path()
    channel_dict = {'show':'综艺','tv':'电视剧','movie':'电影','cartoon':'动漫'}
    channel_name = request.GET.get('name')###获取url中传过来的参数
    channel_name_eng = channel_name###后续post需要该参数
    if request.method == 'GET':
        calculate_date = datetime.datetime.now() - datetime.timedelta(days=1)
    elif request.method == 'POST':
        post_date = request.POST.get('search_date')###获取post表单中的参数
        calculate_date = datetime.datetime.strptime(post_date, "%Y-%m-%d")

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

    ###查询月vv
    vv_month_result = Newmofang(searchtype='channel_vv_month',channel_name=channel_name,end_date=end_date).sql_query()

    ###查询日vv
    vv_day_result = Newmofang(searchtype='channel_vv_day',channel_name=channel_name,start_date=start_date,end_date=end_date).sql_query()
    ###查询日uv
    uv_day_result = Newmofang(searchtype='channel_uv_day',channel_name=channel_name,start_date=start_date,end_date=end_date).sql_query()
    ###查询日时长
    duration_day_result = Newmofang(searchtype='channel_duration_day',channel_name=channel_name,start_date=start_date,end_date=end_date).sql_query()
    ###查询全平台kpi完成情况
    kpi_platform_result = Newmofang(searchtype='channel_kpi',channel_name=channel_name,end_date=end_date).sql_query()

    ###查询终端vv、uv
    date_list = Newmofang(start_date=start_date, end_date=end_date).datetime_process()
    terminal_list = Newmofang().bid_dict.values()
    vv_terminal_day_result = Newmofang(searchtype='channel_vv_terminal_day',channel_name=channel_name,start_date=start_date,end_date=end_date).sql_query()
    # print vv_terminal_day_result
    uv_terminal_day_result = Newmofang(searchtype='channel_uv_terminal_day',channel_name=channel_name,start_date=start_date,end_date=end_date).sql_query()

    ###查询上一周的vvtop50
    pid_vv_week_ago_result = Newmofang(searchtype='channel_pid_vv_change',channel_name=channel_name,start_date=last_week_start_date,end_date=last_week_end_date).sql_query()
    pid_week_str = ','.join(set(map(lambda x: str(x[0]), pid_vv_week_ago_result)))###前一周的合集vvtop中的pid列表
    pid_vv_2week_ago_result = Newmofang(searchtype='channel_pid_vv_change',channel_name=channel_name,pid_str=pid_week_str,start_date=last_2week_start_date,end_date=last_2week_end_date).sql_query()
    # print 'pid_vv_week_ago_result:',pid_vv_week_ago_result,'pid_vv_2week_ago_result:',pid_vv_2week_ago_result

    pid_vv_change_dict = channel_pid_vv_change_process(pid_week_str, pid_vv_week_ago_result, pid_vv_2week_ago_result)

    ###查询最近一周的日均uv、日均vv
    uv_pid_day_avg_result = Newmofang(searchtype='channel_uv_pid_day_avg',channel_name=channel_name, start_date=last_week_start_date, end_date=last_week_end_date).sql_query()###合集日均uvtop20
    pid_str = ','.join(set(map(lambda x: str(x[1]), uv_pid_day_avg_result)))###合集id列表，供vv查询用
    # print pid_str
    vv_pid_day_avg_result = Newmofang(searchtype='channel_vv_pid_day_avg',channel_name=channel_name, start_date=last_week_start_date,pid_str=pid_str,end_date=last_week_end_date).sql_query()  ###合集日均uvtop20

    # ###vv、uv条形图
    # pid_bar_dict = channel_pid_day_avg_bar_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)
    # print pid_bar_dict
    ###vv、uv气泡图
    pid_day_avg_result = channel_pid_day_avg_result_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)


    ###数据转化为列表传入前端
    kpi_ratio = kpi_channel_process(kpi_platform_result,channel_name)

    overview_channel_day_dict = overview_channel_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,duration_day_result)###往日概览数据
    vv_month_date, vv_month_lastyear, vv_month_thisyear = vv_month_process(vv_month_result=vv_month_result)###平台月度uv数据
    vv_day_date, vv_day_data, uv_day_data,vv_day_perperson = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)###全平台日vv、uv、人均vv数据
    vv_terminal_day_dict = vv_terminal_day_process(vv_terminal_day_result=vv_terminal_day_result,date_list=date_list,terminal_list=terminal_list)  ###分端vv变化
    uv_terminal_day_dict = uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result, date_list=date_list,terminal_list=terminal_list)  ###分端uv变化

    return render(request,'channel_ltt.html',{'path':path,'vv_month_date':json.dumps(vv_month_date),'vv_month_lastyear':json.dumps(vv_month_lastyear),'channel_name_eng':channel_name_eng,
                                   'vv_month_thisyear':json.dumps(vv_month_thisyear),'date_str':date_str,'channel_name':json.dumps([channel_dict[channel_name]]),
                                        'kpi_ratio':kpi_ratio,'overview_channel_day_dict':overview_channel_day_dict,'channel_name_div':[channel_dict[channel_name]],
                                          'vv_day_data': json.dumps(vv_day_data),'uv_day_data':json.dumps(uv_day_data),'vv_day_date':json.dumps(vv_day_date),
                                          'vv_terminal_day_dict': vv_terminal_day_dict,'uv_terminal_day_dict': uv_terminal_day_dict,
                                          'pid_day_avg_result': json.dumps(pid_day_avg_result),'pid_vv_change_dict':json.dumps(pid_vv_change_dict),})

def kpi_platform_process(kpi_platform_result):
    ###每季度的kpi目标
    kpi_target = 100000000
    kpi_now = kpi_platform_result[0][0]
    kpi_ratio = round(kpi_now/kpi_target*100,2)
    return kpi_ratio

def kpi_channel_process(kpi_platform_result,channel_name):
    ###每季度的kpi目标
    kpi_target_dict = {'show':35000000,'tv':35000000,'movie':6000000,'cartoon':22000000,'music':600000}
    kpi_target = kpi_target_dict[channel_name]
    kpi_now = kpi_platform_result[0][0]
    kpi_ratio = round(kpi_now/kpi_target*100,2)
    return kpi_ratio


def data_format(result,format_type):###sql返回结果处理
    if result != []:
        date_list = [each[0] for each in result]###日期列表
        if format_type == 'normal':
            data_list = [round(each[1]/10000,1) for each in result]###数据列表
        elif format_type == 'duration':
            data_list = [round(each[1] / 60, 1) for each in result]  ###数据列表
        return date_list,data_list###返回x轴时间列表和y轴值列表

def overview_platform_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,pv_day_result,duration_day_result):###处理往日概况模块,暂定为昨日vv、uv、pv、时长数据
    days_ago_location = date_list.index(end_date)###昨日日期在日期列表中的位置
    month_to_month_location = date_list.index(month_to_month_date)###环比日期在日期列表中的位置
    year_to_year_location = date_list.index(year_to_year_date)###同比日期在日期列表中的位置
    # print days_ago_location,month_to_month_location,year_to_year_location
    vv_day_data = data_format(vv_day_result,format_type='normal')[1]###获取vv列表
    uv_day_data = data_format(uv_day_result,format_type='normal')[1]###获取uv列表
    vv_perperson_day_data = list(map(lambda x: round(x[0] / x[1], 1), zip(vv_day_data, uv_day_data)))###计算人均vv列表
    pv_day_data = data_format(pv_day_result,format_type='normal')[1]###获取pv列表
    duration_day_data = data_format(duration_day_result,format_type='duration')[1]###获取时长列表
    duration_perperson_day_data = list(map(lambda x: round(x[0] / x[1]/10000, 1), zip(duration_day_data, uv_day_data)))  ###计算人均观看时长列表
    data_dict = {'vv': vv_day_data, 'uv': uv_day_data, 'pv': pv_day_data, 'vv_perperson':vv_perperson_day_data,'duration_perperson': duration_perperson_day_data }
    # print uv_day_data,duration_day_data,duration_perperson_day_data
    overview_platform_day_dict = {}
    ###计算概览数据,每个部分的数据均以 [昨日数据，环比，同比] 进行显示
    for key in data_dict.keys():
        x = data_dict[key]
        overview_result = [x[days_ago_location],'%.2f'%round((x[days_ago_location]/x[month_to_month_location]-1)*100,2),'%.2f'%round((x[days_ago_location]/x[year_to_year_location]-1)*100,2)]
        overview_platform_day_dict[key] = overview_result
    # print overview_platform_day_dict
    return overview_platform_day_dict
    # overview_platform_day_dict['vv'] = [vv_day_data[days_ago_location],round(vv_day_data[days_ago_location]/vv_day_data[month_to_month_location]-1]

def overview_channel_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,duration_day_result):###处理往日概况模块,暂定为昨日vv、uv、pv、时长数据
    days_ago_location = date_list.index(end_date)###昨日日期在日期列表中的位置
    month_to_month_location = date_list.index(month_to_month_date)###环比日期在日期列表中的位置
    year_to_year_location = date_list.index(year_to_year_date)###同比日期在日期列表中的位置
    print days_ago_location,month_to_month_location,year_to_year_location
    vv_day_data = data_format(vv_day_result,format_type='normal')[1]###获取vv列表
    uv_day_data = data_format(uv_day_result,format_type='normal')[1]###获取uv列表
    vv_perperson_day_data = list(map(lambda x: round(x[0] / x[1], 1), zip(vv_day_data, uv_day_data)))###计算人均vv列表
    duration_day_data = data_format(duration_day_result,format_type='duration')[1]###获取时长列表
    duration_perperson_day_data = list(map(lambda x: round(x[0] / x[1]/10000, 1), zip(duration_day_data, uv_day_data)))  ###计算人均观看时长列表
    data_dict = {'vv': vv_day_data, 'uv': uv_day_data, 'vv_perperson':vv_perperson_day_data,'duration_perperson': duration_perperson_day_data }
    # print uv_day_data,duration_day_data,duration_perperson_day_data
    overview_platform_day_dict = {}
    ###计算概览数据,每个部分的数据均以 [昨日数据，环比，同比] 进行显示
    for key in data_dict.keys():
        x = data_dict[key]
        overview_result = [x[days_ago_location],'%.2f'%round((x[days_ago_location]/x[month_to_month_location]-1)*100,2),'%.2f'%round((x[days_ago_location]/x[year_to_year_location]-1)*100,2)]
        overview_platform_day_dict[key] = overview_result
    # print overview_platform_day_dict
    return overview_platform_day_dict
    # overview_platform_day_dict['vv'] = [vv_day_data[days_ago_location],round(vv_day_data[days_ago_location]/vv_day_data[month_to_month_location]-1]

###频道模块合集条形图数据计算
def channel_pid_day_avg_bar_process(pid_str,vv_pid_day_avg_result,uv_pid_day_avg_result):
    cms_result = Newmofang(pid_str=pid_str).cms_sql()
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
    cms_result = Newmofang(pid_str=pid_week_str).cms_sql()
    pid_vv_change_list = []
    for pid_week_each in pid_vv_week_ago_result:
        for pid_2week_each in pid_vv_2week_ago_result:
            for cms_each in cms_result:
                if pid_week_each[0] == pid_2week_each[0] and str(cms_each[0]) == str(pid_week_each[0]):
                    pid_vv_change_list.append([cms_each[1],pid_week_each[1],pid_2week_each[1],round((pid_week_each[1]-pid_2week_each[1])/pid_2week_each[1]*100,1)])
    ###针对两周vv的差值进行排序
    pid_vv_change_list.sort(key=operator.itemgetter(3))
    print 'pid_vv_change_list:',pid_vv_change_list
    ###降幅部分
    pid_vv_change_decrease = pid_vv_change_list[:10]###跌幅前10
    pid_vv_change_decrease = filter(lambda x: x[3] < 0, pid_vv_change_decrease)###必须是环比<0
    pid_vv_change_decrease.sort(key=operator.itemgetter(3),reverse=True)
    pid_vv_change_decrease_name = map(lambda x:x[0],pid_vv_change_decrease)###降幅top10的合集名称
    pid_vv_change_decrease_vv = map(lambda x:x[3], pid_vv_change_decrease)###降幅top10的vv差值
    ###涨幅部分
    pid_vv_change_increase = pid_vv_change_list[-10:]
    pid_vv_change_increase = filter(lambda x: x[3] > 0, pid_vv_change_increase)  ###必须是环比>0
    pid_vv_change_increase_name = map(lambda x:x[0],pid_vv_change_increase)###涨幅top10的合集名称
    pid_vv_change_increase_vv = map(lambda x:x[3], pid_vv_change_increase)###涨幅top10的vv差值
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
    cms_result = Newmofang(pid_str=pid_str).cms_sql()
    # print cms_result
    pid_list = map(lambda x: str(x[0]), uv_pid_day_avg_result)
    ###总的list,根据echarts中js需要的数据格式，最后的结构为 [[综艺频道数据],[电视剧频道数据]]，每个频道数据为[vv,uv,人均vv,合集名称,频道名称]
    pid_day_avg_result = []
    ###各频道list
    show_day_avg_result = []###综艺
    tv_day_avg_result = []###电视剧
    movie_day_avg_result = []  ###电影
    cartoon_day_avg_result = []  ###动漫
    for pid in pid_list:
        for cms_each in cms_result:
            for vv_each in vv_pid_day_avg_result:
                for uv_each in uv_pid_day_avg_result:
                    if str(pid) == str(cms_each[0]) and str(pid) == str(vv_each[0]) and str(pid) == str(uv_each[0]):
                        if cms_each[2] == u'综艺':
                            show_day_avg_result.append([round(uv_each[1]/10000),round(vv_each[1]/10000),round(vv_each[1]/uv_each[1],1),cms_each[1],cms_each[2]])
                        elif cms_each[2] == u'电视剧':
                            tv_day_avg_result.append([round(uv_each[1] / 10000), round(vv_each[1] / 10000),round(vv_each[1] / uv_each[1], 1), cms_each[1], cms_each[2]])
                        elif cms_each[2] == u'电影':
                            movie_day_avg_result.append([round(uv_each[1] / 10000), round(vv_each[1] / 10000),round(vv_each[1] / uv_each[1], 1), cms_each[1], cms_each[2]])
                        elif cms_each[2] == u'动漫':
                            cartoon_day_avg_result.append([round(uv_each[1] / 10000), round(vv_each[1] / 10000),round(vv_each[1] / uv_each[1], 1), cms_each[1], cms_each[2]])
    pid_day_avg_result.extend([show_day_avg_result,tv_day_avg_result,movie_day_avg_result,cartoon_day_avg_result])
    return pid_day_avg_result


###频道模块合集气泡图数据计算
def channel_pid_day_avg_result_process(pid_str,vv_pid_day_avg_result,uv_pid_day_avg_result):
    cms_result = Newmofang(pid_str=pid_str).cms_sql()
    print 'cms_result:',map(lambda x:str(x[0]) ,cms_result)
    print 'uv_pid_day_avg_result:',map(lambda x:str(x[1]) ,uv_pid_day_avg_result)
    print 'vv_pid_day_avg_result:',map(lambda x:str(x[1]) ,vv_pid_day_avg_result)
    ###总的list,根据echarts中js需要的数据格式，最后的结构为 [[频道数据]]，频道数据为[vv,uv,人均vv,合集名称,频道名称]
    pid_day_avg_result = []
    ###
    pcweb_day_avg_result = []###pcweb
    android_day_avg_result = []###android
    iphone_day_avg_result = []  ###iphone
    ott_day_avg_result = []  ###ott
    for uv_each in uv_pid_day_avg_result:
        for vv_each in vv_pid_day_avg_result:
            for cms_each in cms_result:
                if  str(vv_each[0]) == str(uv_each[0]) and str(vv_each[1]) == str(uv_each[1]) and str(uv_each[1]) == str(cms_each[0]):
                    if uv_each[0] == 'pcweb':
                        pcweb_day_avg_result.append([round(uv_each[2]/10000,1),round(vv_each[2]/10000,1),round(vv_each[2]/uv_each[2],1),cms_each[1],uv_each[0]])
                    elif uv_each[0] == 'android':
                        android_day_avg_result.append([round(uv_each[2] / 10000,1), round(vv_each[2] / 10000,1),round(vv_each[2] / uv_each[2], 1), cms_each[1], uv_each[0]])
                    elif uv_each[0] == 'iphone':
                        iphone_day_avg_result.append([round(uv_each[2] / 10000,1), round(vv_each[2] / 10000,1),round(vv_each[2] / uv_each[2], 1), cms_each[1], uv_each[0]])
                    elif uv_each[0] == 'ott':
                        ott_day_avg_result.append([round(uv_each[2] / 10000,1), round(vv_each[2] / 10000,1),round(vv_each[2] / uv_each[2], 1), cms_each[1], uv_each[0]])
    pid_day_avg_result.extend([pcweb_day_avg_result,android_day_avg_result,iphone_day_avg_result,ott_day_avg_result])
    print pid_day_avg_result
    return pid_day_avg_result



###月vv数据处理
def vv_month_process(vv_month_result):
    vv_month_data = data_format(vv_month_result,format_type='normal')[1]
    ###月份列表
    vv_month_date = [str(i) + '月' for i in range(1, 13)]
    ###第一年vv
    vv_month_lastyear = vv_month_data[:12]
    vv_month_thisyear = vv_month_data[12:]
    return vv_month_date,vv_month_lastyear,vv_month_thisyear

###日vv、uv、人均vv处理
def vv_day_process(vv_day_result,uv_day_result):
    vv_day_date,vv_day_data = data_format(vv_day_result,format_type='normal')
    uv_day_date, uv_day_data = data_format(uv_day_result,format_type='normal')
    vv_day_perperson = list(map(lambda x:round(x[0]/x[1],1),zip(vv_day_data,uv_day_data)))
    # print ("{vv_day_data} \n {uv_day_data} \n {vv_day_perperson}").format(vv_day_data=vv_day_data,uv_day_data=uv_day_data,vv_day_perperson=vv_day_perperson)
    return vv_day_date,vv_day_data,uv_day_data,vv_day_perperson



###日vv分端处理
def vv_terminal_day_process(vv_terminal_day_result,date_list,terminal_list):
    vv_terminal_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for terminal in terminal_list:
        terminal_list = list()###每个终端对应的字典
        for date in date_list:
            for result in vv_terminal_day_result:
                if date == str(result[0]) and terminal == str(result[1]):
                    terminal_list.append(round(result[2]/10000,1))
        vv_terminal_day_dict[terminal] = terminal_list
    return vv_terminal_day_dict


###日uv分端处理
def uv_terminal_day_process(uv_terminal_day_result,date_list,terminal_list):
    uv_terminal_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for terminal in terminal_list:
        terminal_list = list()###每个终端对应的字典
        for date in date_list:
            for result in uv_terminal_day_result:
                if date == str(result[0]) and terminal == str(result[1]):
                    terminal_list.append(round(result[2]/10000,1))
        uv_terminal_day_dict[terminal] = terminal_list
    return uv_terminal_day_dict


###日vv分频道处理
def vv_channel_day_process(vv_channel_day_result,date_list,channel_list):
    vv_channel_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for channel in channel_list:
        channel_list = list()###每个终端对应的字典
        for date in date_list:
            for result in vv_channel_day_result:
                if date == str(result[0]) and channel == str(result[1]):
                    channel_list.append(round(result[2]/10000,1))
        vv_channel_day_dict[channel] = channel_list
    return vv_channel_day_dict


###日uv分端处理
def uv_channel_day_process(uv_channel_day_result,date_list,channel_list):
    uv_channel_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    for channel in channel_list:
        channel_list = list()###每个终端对应的字典
        for date in date_list:
            for result in uv_channel_day_result:
                if date == str(result[0]) and channel == str(result[1]):
                    channel_list.append(round(result[2]/10000,1))
        uv_channel_day_dict[channel] = channel_list
    return uv_channel_day_dict


###日dau处理
def dau_day_process(dau_day_result,uv_day_data):
    ###先将sql结果转换为列表，再对应位置相除
    dau_result = data_format(dau_day_result,format_type='normal')[1]
    uv_dau = zip(uv_day_data,dau_result)
    uv_ration = map(lambda x:round(x[0]/x[1],2),uv_dau)
    return dau_result,uv_ration