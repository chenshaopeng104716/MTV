#coding:utf-8
from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from .models import *
from django.http import  HttpResponseRedirect,HttpResponse
from django.db import connection
from data_process import *
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

    ###节目模块li标签top10uv的合集
    program_li_show_sql = platform_class.module_search(searchtype='program_li_show')

    ###合并sql,一次查询
    sql_combine = Newmofang().sql_union(vv_month_sql,vv_day_sql,uv_day_sql,pv_day_sql,duration_day_sql,kpi_platform_sql,vv_terminal_day_sql,uv_terminal_day_sql,
                                        vv_channel_day_sql,uv_channel_day_sql,dau_platform_day_sql,uv_pid_day_avg_sql,program_li_show_sql)
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
    program_li_show_result = all_result[all_result['module_name'] == 'program_li_show']
    pid_list = uv_pid_day_avg_result['col1'].tolist()###获取pid列表
    pid_list_to_str = map(lambda x:str(x),pid_list)
    pid_str = ','.join(pid_list_to_str)###合集id列表，供vv查询用
    vv_pid_day_avg_sql = Newmofang(last_week_start_date=last_week_start_date,pid_str=pid_str,last_week_end_date=last_week_end_date).module_search(searchtype='platform_vv_pid_day_avg') ###合集日均uvtop20
    vv_pid_day_avg_result = Newmofang().sql_query(vv_pid_day_avg_sql)

    ###数据处理
    pid_day_avg_result = platform_pid_day_avg_result_process(pid_str, vv_pid_day_avg_result, uv_pid_day_avg_result)

    kpi_ratio = kpi_platform_process(kpi_platform_result,end_date)

    overview_platform_day_dict = overview_platform_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,pv_day_result,duration_day_result)###往日概览数据
    vv_month_date, vv_month_lastyear, vv_month_thisyear = vv_month_process(vv_month_result=vv_month_result)###平台月度uv数据
    vv_day_date, vv_day_data, uv_day_data = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)###全平台日vv、uv、人均vv数据
    vv_terminal_day_dict = vv_terminal_day_process(vv_terminal_day_result=vv_terminal_day_result,terminal_list=terminal_list)  ###分端vv变化
    uv_terminal_day_dict = uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result,terminal_list=terminal_list)  ###分端uv变化
    vv_channel_day_dict = vv_channel_day_process(vv_channel_day_result=vv_channel_day_result,channel_list=channel_list)  ###分频道vv变化
    uv_channel_day_dict = uv_channel_day_process(uv_channel_day_result=uv_channel_day_result,channel_list=channel_list)  ###分频道uv变化
    dau_day_data, uv_ration_day_data = dau_day_process(dau_platform_day_result=dau_platform_day_result,uv_day_result=uv_day_result)
    program_li_show_dict = program_li_show_process(program_li_show_result)
    end_time = time.time()
    print 'time elapse is %s'%(end_time-start_time)
    return render(request, 'platform.html', {'kpi_ratio':kpi_ratio,'vv_day_date':json.dumps(vv_day_date),'vv_day_data':json.dumps(vv_day_data),
                                       'uv_day_data': json.dumps(uv_day_data),'vv_month_date':json.dumps(vv_month_date),
                                          'vv_month_lastyear':json.dumps(vv_month_lastyear),'vv_month_thisyear':json.dumps(vv_month_thisyear),
                                          'vv_terminal_day_dict':vv_terminal_day_dict,'uv_terminal_day_dict':uv_terminal_day_dict,'vv_channel_day_dict':vv_channel_day_dict,
                                       'uv_channel_day_dict':uv_channel_day_dict,'dau_day_data':dau_day_data,'uv_ration_day_data':uv_ration_day_data,
                                        'overview_platform_day_dict':overview_platform_day_dict,'pid_day_avg_result':json.dumps(pid_day_avg_result),
                                          'date_str':date_str,'program_li_show_dict':program_li_show_dict})

###频道模块
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

    ###节目模块li标签top10uv的合集
    program_li_show_sql = channel_class.module_search(searchtype='program_li_show')

    ###合并sql,一次查询
    sql_combine = Newmofang().sql_union(vv_month_sql,vv_day_sql,uv_day_sql,duration_day_sql,kpi_channel_sql,vv_terminal_day_sql,uv_terminal_day_sql,
                                        uv_pid_day_avg_sql,pid_vv_week_ago_sql,program_li_show_sql)
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
    program_li_show_result = all_result[all_result['module_name'] == 'program_li_show']
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
    kpi_ratio = kpi_channel_process(kpi_channel_result,channel_name,end_date)

    overview_channel_day_dict = overview_channel_day_process(date_list,end_date,month_to_month_date,year_to_year_date,vv_day_result,uv_day_result,duration_day_result)###往日概览数据
    vv_month_date, vv_month_lastyear, vv_month_thisyear = vv_month_process(vv_month_result=vv_month_result)###平台月度uv数据
    vv_day_date, vv_day_data, uv_day_data = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)###全平台日vv、uv数据
    vv_terminal_day_dict = vv_terminal_day_process(vv_terminal_day_result=vv_terminal_day_result,terminal_list=terminal_list)  ###分端vv变化
    uv_terminal_day_dict = uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result,terminal_list=terminal_list)  ###分端uv变化
    program_li_show_dict = program_li_show_process(program_li_show_result)###节目模块合集标签
    end_time = time.time()
    print 'time elapse is %s'%(end_time-start_time)
    return render(request,'channel.html',{'path':path,'vv_month_date':json.dumps(vv_month_date),'vv_month_lastyear':json.dumps(vv_month_lastyear),'channel_name_eng':channel_name_eng,
                                   'vv_month_thisyear':json.dumps(vv_month_thisyear),'date_str':date_str,'channel_name':json.dumps([channel_dict[channel_name]]),
                                        'kpi_ratio':kpi_ratio,'overview_channel_day_dict':overview_channel_day_dict,'channel_name_div':[channel_dict[channel_name]],
                                          'vv_day_data': json.dumps(vv_day_data),'uv_day_data':json.dumps(uv_day_data),'vv_day_date':json.dumps(vv_day_date),
                                          'vv_terminal_day_dict': vv_terminal_day_dict,'uv_terminal_day_dict': uv_terminal_day_dict,
                                          'pid_day_avg_result': json.dumps(pid_day_avg_result),'pid_vv_change_dict':json.dumps(pid_vv_change_dict),
                                          'program_li_show_dict':program_li_show_dict,})

###节目模块
def program(request):
    start_time = time.time()
    path = request.get_full_path()
    program_id = request.GET.get('id')###获取url中传过来的参数
    if request.method == 'GET':
        calculate_date = datetime.datetime.now() - datetime.timedelta(days=1)
    elif request.method == 'POST':
        post_date = request.POST.get('search_date')###获取post表单中的参数
        calculate_date = datetime.datetime.strptime(post_date, "%Y-%m-%d")
    start_date, end_date, end_date_show, last_week_start_date, last_week_end_date, \
    last_2week_start_date, last_2week_end_date, month_to_month_date,year_to_year_date,date_str = date_calculate(calculate_date)

    ###初始类
    program_class = Newmofang(pid=program_id, start_date=start_date, end_date=end_date,
                              last_week_start_date=last_week_start_date, last_week_end_date=last_week_end_date,)
    date_list = program_class.datetime_process()
    terminal_list = program_class.bid_dict.values()###终端列表
    ###媒资查询合集中vid
    cms_result = program_class.cms_sql(cms_type='search_vid')

    vid_list = map(lambda x:str(x),cms_result['vid'].tolist())###vid列表
    vid_str = ','.join(map(lambda x:"'"+x+"'",vid_list))

    ###合集名称
    program_name = cms_result['pid_title'].unique()[0]
    # comment_result = program_class.program_comment(vid_str=vid_str)###评论模块数据查询
    ###各小模块数据查询
    vv_day_sql = program_class.module_search(searchtype='program_vv_day')
    uv_day_sql = program_class.module_search(searchtype='program_uv_day')
    uv_terminal_day_sql = program_class.module_search(searchtype='program_uv_terminal_day')
    duration_isfull_day_sql = program_class.module_search(searchtype='program_duration_isfull_day')
    pt_type_day_sql = program_class.module_search(searchtype='program_pt_type_day')
    vid_isfull_day_sql = Newmofang(start_date=start_date, end_date=end_date,vid_str=vid_str).module_search(searchtype='program_vid_isfull_day')
    ###节目模块li标签top10uv的合集
    program_li_show_sql = program_class.module_search(searchtype='program_li_show')
    ###合并sql,一次查询
    sql_combine = program_class.sql_union(vv_day_sql,uv_day_sql,uv_terminal_day_sql,duration_isfull_day_sql,pt_type_day_sql,vid_isfull_day_sql,program_li_show_sql)
    all_result = program_class.sql_query(sql_combine)

    ###利用pandas包把all_result分到不同的查询
    vv_day_result = all_result[all_result['module_name']=='program_vv_day'].sort(['col1'])
    uv_day_result = all_result[all_result['module_name']=='program_uv_day'].sort(['col1'])
    uv_terminal_day_result = all_result[all_result['module_name']=='program_uv_terminal_day'].sort(['col1'])
    duration_isfull_day_result = all_result[all_result['module_name']=='program_duration_isfull_day'].sort(['col1'])
    pt_type_day_result = all_result[all_result['module_name'] == 'program_pt_type_day']
    vid_isfull_day_result = all_result[all_result['module_name'] == 'program_vid_isfull_day']
    program_li_show_result = all_result[all_result['module_name'] == 'program_li_show']

    vv_day_date, vv_day_data, uv_day_data = vv_day_process(vv_day_result=vv_day_result,uv_day_result=uv_day_result)  ###全平台日vv、uv数据
    uv_terminal_day_dict = program_uv_terminal_day_process(uv_terminal_day_result=uv_terminal_day_result,terminal_list=terminal_list)  ###分端uv变化
    duration_isfull_day_dict = program_duration_isfull_day_process(duration_isfull_day_result)
    pt_type_day_dict = program_pt_type_day_process(pt_type_day_result)
    vid_isfull_day_dict = program_vid_isfull_day_process(vid_isfull_day_result,cms_result)
    program_li_show_dict = program_li_show_process(program_li_show_result)  ###节目模块合集标签

    end_time = time.time()
    print 'time elapse is %s'%(end_time-start_time)
    return render(request,'program.html',{'path':path,'vv_day_data': json.dumps(vv_day_data),'uv_day_data':json.dumps(uv_day_data),'vv_day_date':json.dumps(vv_day_date)
                                        ,'program_name':program_name,'uv_terminal_day_dict':uv_terminal_day_dict,'duration_isfull_day_dict':duration_isfull_day_dict,
                                          'vid_isfull_day_dict':json.dumps(vid_isfull_day_dict),'pt_type_day_dict':pt_type_day_dict,'end_date':end_date,
                                          'program_li_show_dict':program_li_show_dict,'program_id':program_id},)



def testindex(request):
    return render(request,'index333.html')