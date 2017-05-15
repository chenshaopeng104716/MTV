###coding:utf-8

import time
import datetime
import pandas as pd
import numpy as np
from SQLclass import *


def date_calculate(calculate_date):
    start_date = '20170101'  ###查询开始时间
    # start_date = (calculate_date - datetime.timedelta(days=29)).date().strftime('%Y%m%d')  ###查询开始时间
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


def kpi_platform_process(kpi_platform_result,end_date):
    ###每季度的kpi目标
    kpi_target = {2017:{01:10000,02:10000}}
    ###每个月对应的季度
    quarter = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}
    year = int(end_date[:4])###当前年份
    month = int(end_date[4:6])###当前月份
    quarter_now = quarter[month]###当前季度
    kpi_now = kpi_platform_result['num'].unique()###当前已完成kpi
    kpi_target_quarter = kpi_target[year][quarter_now]
    kpi_ratio = round(kpi_now/kpi_target_quarter*100,2)
    return kpi_ratio

def kpi_channel_process(kpi_channel_result,channel_name,end_date):
    ###每季度的kpi目标
    kpi_target_dict = {'show':{2017:{01:2835,02:2835}},'tv':{2017:{01:3000,02:3000}},'movie':{2017:{01:600,02:600}},'cartoon':{2017:{01:2200,02:2100}}}
    ###每个月对应的季度
    quarter = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}
    year = int(end_date[:4])###当前年份
    month = int(end_date[4:6])###当前月份
    quarter_now = quarter[month]###当前季度
    kpi_now = kpi_channel_result['num'].unique()
    kpi_target_quarter = kpi_target_dict[channel_name][year][quarter_now]
    kpi_ratio = round(kpi_now/kpi_target_quarter*100,2)
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
    cms_result = Newmofang(pid_str=pid_str).cms_sql(cms_type='search_pid_name')
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
    cms_result = Newmofang(pid_str=pid_week_str).cms_sql(cms_type='search_pid_name')
    vv_week_ago_result = pid_vv_week_ago_result[['col1','num']]###取出需要的列，重命名
    vv_week_ago_result.columns = ['pid','vv_week_ago']
    vv_2week_ago_result = pid_vv_2week_ago_result[['col1','num']]###取出需要的列，重命名
    vv_2week_ago_result.columns = ['pid','vv_2week_ago']
    dataframe_all = pd.merge(cms_result,vv_week_ago_result,how='inner',on='pid')
    dataframe_all = pd.merge(dataframe_all,vv_2week_ago_result,how='inner',on='pid')
    dataframe_all['vv_diff'] = map(lambda x,y:round(100*(x-y)/y),dataframe_all['vv_week_ago'],dataframe_all['vv_2week_ago'])
    dataframe_all = dataframe_all[dataframe_all['vv_diff'] != np.inf]###过滤掉正无穷
    dataframe_all = dataframe_all[dataframe_all['vv_diff'] != -np.inf]  ###过滤掉负无穷
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
    cms_result = Newmofang(pid_str=pid_str).cms_sql(cms_type='search_pid_name')
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
    cms_result = Newmofang(pid_str=pid_str).cms_sql(cms_type='search_pid_name')
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

###节目模块日uv分端处理
def program_uv_terminal_day_process(uv_terminal_day_result,terminal_list):
    uv_terminal_day_dict = dict()###返回的数据字典，数据格式为：  {终端1：[列表1],终端2：[列表2]}
    dataframe = pd.pivot_table(uv_terminal_day_result, index=['col1'], columns=['col2'], values=['num'], fill_value=0)###数据转置处理
    for terminal in terminal_list:
        try:
            terminal_list = dataframe['num'][terminal].tolist()
            uv_terminal_day_dict[terminal] = terminal_list
        except:
            pass
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
    data_all['uv_ration'] = map(lambda x,y:'%.2f'%round(x/y*100,2),data_all['uv'],data_all['dau'])
    dau_list = data_all['dau'].tolist()
    ration_list = data_all['uv_ration'].tolist()
    return dau_list,ration_list

###节目模块li标签top10uv
def program_li_show_process(program_li_show_result):
    pid_list = program_li_show_result['col1'].tolist()###获取top10的pid
    pid_list_to_str = map(lambda x:str(x),pid_list)###格式转换
    pid_str = ','.join(pid_list_to_str)###合集id列表，供媒资查询合集名称用
    cms_result = Newmofang(pid_str=pid_str).cms_sql(cms_type='search_pid_name')###查询媒资信息(合集id,合集名称)
    cms_list_result = map(lambda x,y:{x:y},cms_result['pid_title'],cms_result['pid'])###转化为列表
    cms_dict_result = reduce(lambda x,y:dict(x,**y),cms_list_result)###转化为字典
    return cms_dict_result

###节目模块日正短片vv
def program_duration_isfull_day_process(duration_isfull_day_result):
    duration_isfull_day_dict = dict()###返回的数据字典，数据格式为：  {正片：[列表1],短片：[列表2]}
    dataframe = pd.pivot_table(duration_isfull_day_result, index=['col1'], columns=['col2'], values=['num'], fill_value=0)###数据转置处理
    full_short_list = ['full','short']
    for isfull in full_short_list:
        try:
            isfull_list = dataframe['num'][isfull].tolist()
            duration_isfull_day_dict[isfull] = isfull_list
        except:
            pass
    return duration_isfull_day_dict

###节目模块播放时长分布
def program_pt_type_day_process(pt_type_day_result):
    pt_type_day_dict = dict()###返回的数据字典，数据格式为：  {时长1：[列表1],时长2：[列表2]}
    dataframe = pd.pivot_table(pt_type_day_result, index=['col3'], columns=['col2'], values=['num'], fill_value=0)###数据转置处理
    dataframe = dataframe.reindex(['0min-1min', '1min-15min', '15min-30min', '30min-1hour', '1hour-2hour', '>2hour'])###数据排序
    pt_type_list = ['pcweb','iphone','android','ott']
    for pt_type in pt_type_list:
        try:
            pt_list = map(lambda x:{'name':x,'value':dataframe['num'][pt_type][x]},dataframe['num'][pt_type].index)
            pt_type_day_dict[pt_type] = pt_list
        except:
            pass
    return pt_type_day_dict

###节目模块正短片vv分布
def program_vid_isfull_day_process(vid_isfull_day_result,cms_result):
    vid_isfull = vid_isfull_day_result[['col2','num']]
    vid_isfull[['col2']] = vid_isfull[['col2']].astype('int64')###类型转换
    dataframe = pd.merge(vid_isfull,cms_result,left_on='col2',right_on='vid')
    ###正片top10
    full_dataframe = dataframe[dataframe['isfull'] == 1][['vid_name','num']].sort('num')[-10:]
    short_dataframe = dataframe[dataframe['isfull'] == 0][['vid_name','num']].sort('num')[-10:]
    full_vid_name = full_dataframe['vid_name'].tolist()
    full_num = full_dataframe['num'].tolist()
    short_vid_name = short_dataframe['vid_name'].tolist()
    short_num = short_dataframe['num'].tolist()
    program_vid_isfull_dict = dict()
    program_vid_isfull_dict[u'full_vid_name'] = full_vid_name
    program_vid_isfull_dict[u'short_vid_name'] = short_vid_name
    program_vid_isfull_dict[u'full_num'] = full_num
    program_vid_isfull_dict[u'short_num'] = short_num
    return program_vid_isfull_dict
