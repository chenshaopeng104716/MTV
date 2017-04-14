#coding:utf-8

import psycopg2
import MySQLdb
import datetime
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class Newmofang(object):

    """新魔方相关数据查询"""

    def __init__(self,**kwargs):

        ###数据查询用表
        self.search_dict = {'platform_kpi':'vv_cid_day','platform_vv_day': 'vv_cid_day', 'platform_uv_day': 'bid_uv_day','platform_pv_day':'dau_bid_day',
                            'platform_duration_day':'pt_bid_day','platform_vv_month': 'vv_cid_day','platform_vv_terminal_day':'vv_cid_day',
                            'platform_uv_terminal_day':'bid_uv_day','platform_vv_channel_day':'vv_cid_day','platform_uv_channel_day':'cid_uv_day',
                            'platform_dau_day':'dau_bid_day','platform_uv_pid_day_avg':'pid_uv_day','platform_vv_pid_day_avg':'vv_pid_day',

                            'channel_kpi':'vv_cid_day','channel_vv_month':'vv_cid_day','channel_vv_day':'vv_cid_day','channel_uv_day':'cid_uv_day',
                            'channel_duration_day':'pt_cid_day','channel_vv_terminal_day':'vv_cid_day','channel_uv_terminal_day':'cid_uv_day',
                            'channel_uv_pid_day_avg': 'pid_uv_day', 'channel_vv_pid_day_avg': 'vv_pid_day','channel_pid_vv_change':'vv_pid_day',
                            }
        ###查询对应模块所用类内部函数
        self.func_dict = {"platform_kpi":self.platform_kpi,"platform_vv_month": self.platform_vv_month,"platform_vv_day": self.platform_vv_day,"platform_pv_day":self.platform_pv_day,"platform_uv_day": self.platform_uv_day,
                          "platform_duration_day":self.platform_duration_day,"platform_vv_terminal_day":self.platform_vv_terminal_day,"platform_uv_terminal_day":self.platform_uv_terminal_day,"platform_vv_channel_day":self.platform_vv_channel_day,
                          "platform_uv_channel_day":self.platform_uv_channel_day,"platform_dau_day":self.platform_dau_day,"platform_uv_pid_day_avg":self.platform_uv_pid_day_avg,"platform_vv_pid_day_avg":self.platform_vv_pid_day_avg,

                          "channel_kpi":self.channel_kpi,"channel_vv_month":self.channel_vv_month,"channel_vv_day":self.channel_vv_day,"channel_uv_day":self.channel_uv_day,
                          "channel_duration_day":self.channel_duration_day,"channel_vv_terminal_day":self.channel_vv_terminal_day,"channel_uv_terminal_day":self.channel_uv_terminal_day,
                          "channel_uv_pid_day_avg":self.channel_uv_pid_day_avg,"channel_vv_pid_day_avg":self.channel_vv_pid_day_avg,"channel_pid_vv_change":self.channel_pid_vv_change,
                          }
        ###魔方数据库中bid对应的终端
        self.bid_dict = {"1":"ott","102":"pcweb","104":"phonem","5":"padweb","6":"macclient","7":"win10client","8":"pcclient","9":"android","10":"apad","11":"ipad","12":"iphone","13":"mui"}
        ###媒资数据库中cid对应的频道
        self.cid_dict = {"1":"show","2":"tv","3":"movie","7":"cartoon","87":"show","83":"tv","84":"movie","88":"cartoon"}
        ###魔方数据库包含刷量频道,本项目不包含刷量数据,要去除,vv、uv中的刷量频道,现在为bid in (2,4)
        self.bid_not_in = 'bid not in (2,4)'
        ###魔方数据库dau中的刷量频道，现在为bid in (2,4,5)
        self.dau_bid_not_in = 'bid not in (2,4,5)'
        ###频道模块不同的频道名称对应在魔方数据库中的cid,注意：mpp和ott的频道id不一样
        self.newmofang_cid_dict = {'show':'1,87','tv':'2,83','movie':'3,84','cartoon':'7,88'}
        try:###初始化数据库连接
            self.conn = psycopg2.connect(database="dm_result", user="product_readonly", password="deDr7Toi29Sj&SkDS#LL",
                                    host="10.100.5.85", port="2345")
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError:
            print datetime.datetime.now().date()
            print ("新魔方数据库无法连接")
            self.conn = None
            self.cursor = None
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
        if "channel_name" in kwargs:###查询具体频道时要把频道名称传进来
            self.channel_cid = self.newmofang_cid_dict[kwargs['channel_name']]

    ###媒资数据库获取合集名称
    def cms_sql(self):
        cms_dict = {'mpp':{'host':"10.100.5.41",'user':"app_hefang", 'passwd':"app_hefang1234", 'db':"cms",'charset':"utf8",
                           'sql':'select a.id as pid,a.title as pid_title,b.classcn as bid_title from hunantv_v_collection a,hunantv_v_class b where a.rootid = b.id and a.id in (%s);'},
                    'ott':{'host': "10.100.1.70", 'user': "app_hefang", 'passwd': "app_hefang1234", 'db': "tv",'charset': "utf8",
                           'sql':'select a.id as pid,a.`desc` as pid_title,b.`desc` as bid_title from sndlvl a,fstlvl b where a.fstlvl_id=b.id and a.id in (%s);'},}
        for terminal in cms_dict.keys():
            conn = MySQLdb.connect(host=cms_dict[terminal]['host'],user=cms_dict[terminal]['user'],passwd=cms_dict[terminal]['passwd'],db=cms_dict[terminal]['db'],charset=cms_dict[terminal]['charset'])
            sql = cms_dict[terminal]['sql'] % self.pid_str
            if terminal == 'mpp':###不同的媒资合集命名
                mpp_result = pd.read_sql(sql,conn)
            elif terminal == 'ott':
                ott_result = pd.read_sql(sql,conn)
            conn.close()
        cms_result = pd.concat([mpp_result,ott_result])
        return cms_result###合集去重

    ###按照查询模块调取具体函数
    def func(self,searchtype):
        return self.func_dict.get(searchtype)

    ###模块查询
    def sql_query(self,sql_all):###具体查询，返回结果
        if self.conn != None:###判断数据库连接是否正常
            print sql_all
            result = pd.read_sql(sql_all,self.conn)
            self.conn.close()
            # print self.table
        else:
            result = None
        return result

    ###所有查询汇总在一起union all
    @staticmethod
    def sql_union(*args):
        sql_all = ' union all '.join(args)
        return sql_all

    def module_search(self,searchtype):###根据模块查询返回具体的sql
        table = self.search_dict[searchtype]
        module = self.func(searchtype)
        return module(table)

    def platform_kpi(self,table):
        ###每个月对应的季度
        quarter = {1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:3,10:4,11:4,12:4}
        ###查询日期的年份
        year = str(self.end_date)[:4]
        ###每个季度对应的开始日期
        quarter_start_date = {1:year+'0101',2:year+'0401',3:year+'0701',4:year+'1001'}
        ###现在季度
        quarter_now = quarter[(datetime.datetime.strptime(self.end_date, "%Y%m%d")).month]
        calculate_start_time = quarter_start_date[quarter_now]
        calculate_end_time = self.end_date###查询结束时间
        sql = "(select max(date) as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(avg(a.vv)/10000) as num,'platform_kpi' as module_name from (select date,sum(vv) as vv from {table} where {bid_not_in} " \
              "and date>='{start_time}' and date<='{end_time}' GROUP BY date) a)".format(table=table,start_time=calculate_start_time,end_time=calculate_end_time,bid_not_in=self.bid_not_in)
        return sql

    def channel_kpi(self,table):
        ###每个月对应的季度
        quarter = {1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:3,10:4,11:4,12:4}
        ###查询日期的年份
        year = str(self.end_date)[:4]
        ###每个季度对应的开始日期
        quarter_start_date = {1:year+'0101',2:year+'0401',3:year+'0701',4:year+'1001'}
        ###现在季度
        quarter_now = quarter[(datetime.datetime.strptime(self.end_date, "%Y%m%d")).month]
        calculate_start_time = quarter_start_date[quarter_now]
        calculate_end_time = self.end_date###查询结束时间
        sql = "(select max(date) as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(avg(a.vv)/10000,1) as num,'channel_kpi' as module_name from " \
              "(select date,sum(vv) as vv from {table} where {bid_not_in} and cid in ({channel_cid}) " \
              "and date>='{start_time}' and date<='{end_time}' GROUP BY date) a)".format(table=table,start_time=calculate_start_time,end_time=calculate_end_time,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql

    def platform_vv_month(self,table):###全平台月vv汇总模块
        sql = "(select cast(substring(date from 1 for 6) as integer) as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num," \
              "'platform_vv_month' as module_name from {table} where date>='20160101' and date<='{end_date}' and {bid_not_in} " \
              "GROUP BY substring(date from 1 for 6) order by substring(date from 1 for 6))".format(table=table,end_date=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_vv_month(self,table):
        sql = "(select cast(substring(date from 1 for 6) as integer) as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'channel_vv_month' as module_name " \
              "from {table} where date>='20160101' and date<='{end_date}' and {bid_not_in} and cid in ({channel_cid}) " \
              "GROUP BY substring(date from 1 for 6) order by substring(date from 1 for 6))".format(table=table,end_date=self.end_date,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql

    def platform_vv_day(self,table):###全平台每日vv
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'platform_vv_day' as module_name from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_vv_day(self,table):###全平台每日vv
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'channel_vv_day' as module_name from {table} where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql


    def platform_uv_day(self,table):###全平台每日uv
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/10000,1) as num,'platform_uv_day' as module_name from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_uv_day(self,table):###频道模块每日uv
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/10000,1) as num,'channel_uv_day' as module_name from {table} where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql

    def platform_pv_day(self,table):###全平台模块每日pv
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(pv)/10000,1) as num,'platform_pv_day' as module_name from {table} where {dau_bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,dau_bid_not_in=self.dau_bid_not_in)
        return sql

    def platform_duration_day(self,table):
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(pt)/600000,1) as num,'platform_duration_day' as module_name from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_duration_day(self,table):
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(pt)/600000,1) as num,'channel_duration_day' as module_name from {table} where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql

    def platform_vv_terminal_day(self,table):###按终端查询vv
        case_when_sql = self.bid_sql()
        sql = "(select date as col1,{case_when_sql} as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'platform_vv_terminal_day' as module_name from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,bid order by date)".format(case_when_sql=case_when_sql,table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_vv_terminal_day(self,table):###按终端查询vv
        case_when_sql = self.bid_sql()
        sql = "(select date as col1,{case_when_sql} as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'channel_vv_terminal_day' as module_name from {table} " \
              "where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' group by date,bid order by date)".format(case_when_sql=case_when_sql,table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql

    def platform_uv_terminal_day(self,table):
        case_when_sql = self.bid_sql()
        sql = "(select date as col1,{case_when_sql} as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/10000,1) as num,'platform_uv_terminal_day' as module_name from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,bid order by date)".format(case_when_sql=case_when_sql,table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_uv_terminal_day(self,table):
        case_when_sql = self.bid_sql()
        sql = "(select date as col1,{case_when_sql} as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/10000,1) as num,'channel_uv_terminal_day' as module_name from {table} " \
              "where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' group by date,bid order by date)".format(case_when_sql=case_when_sql,table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in,channel_cid=self.channel_cid)
        return sql

    def platform_vv_channel_day(self,table):###按频道查询vv
        case_when_sql = self.cid_sql()
        sql = "(select date as col1,{case_when_sql} as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'platform_vv_channel_day' as module_name from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,col2 order by date)".format(case_when_sql=case_when_sql,table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def platform_uv_channel_day(self,table):
        case_when_sql = self.cid_sql()
        sql = "(select date as col1,{case_when_sql} as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/10000,1) as num,'platform_uv_channel_day' as module_name from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,col2 order by date)".format(case_when_sql=case_when_sql,table=table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def platform_dau_day(self,table):
        sql = "(select date as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/10000,1) as num,'platform_dau_day' as module_name from {table} where {dau_bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date)".format(table=table,start_time=self.start_date,end_time=self.end_date,dau_bid_not_in=self.dau_bid_not_in)
        return sql

    def platform_vv_pid_day_avg(self,table):
        sql = "(select pid as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/70000,1) as num,'platform_vv_pid_day_avg' as module_name" \
              " from {table} where {bid_not_in} and pid in ({pid_str}) and date>='{start_time}' and date<='{end_time}' group by pid order by round(sum(vv)/7) desc limit 20)".format(table=table,pid_str=self.pid_str,start_time=self.last_week_start_date,end_time=self.last_week_end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_vv_pid_day_avg(self,table):
        case_when_sql = self.bid_sql()
        sql = "(select a.bid_name as col1,a.pid as col2,'null' as col3,'null' as col4,'null' as col5,a.vv as num,'channel_vv_pid_day_avg' as module_name from " \
              "(select {case_when_sql} as bid_name,pid,round(sum(vv)/70000,1) as vv from {table} where pid in ({pid_str}) and date>='{start_time}' and date<='{end_time}' " \
              "and bid in (1,102,9,12) and cid in ({channel_cid}) GROUP BY bid,pid) a)".format(table=table,case_when_sql=case_when_sql,start_time=self.last_week_start_date,end_time=self.last_week_end_date,channel_cid=self.channel_cid,pid_str=self.pid_str)
        return sql

    def platform_uv_pid_day_avg(self,table):
        sql = "(select pid as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(uv)/70000,1) as num,'platform_uv_pid_day_avg' as module_name" \
              " from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by pid order by round(sum(uv)/7) desc limit 20)".format(table=table,start_time=self.last_week_start_date,end_time=self.last_week_end_date,bid_not_in=self.bid_not_in)
        return sql

    def channel_uv_pid_day_avg(self,table):
        case_when_sql = self.bid_sql()
        sql = "(select a.pid as col1,a.bid_name as col2,'null' as col3,'null' as col4,'null' as col5,a.uv as num,'channel_uv_pid_day_avg' as module_name from " \
              "(select {case_when_sql} as bid_name,pid,round(sum(uv)/70000,1) as uv,rank() over (partition by bid order by sum(uv)/7 desc) as rank from {table} where date>='{start_time}' and date<='{end_time}' " \
              "and bid in (1,102,9,12) and cid in ({channel_cid}) GROUP BY bid,pid) a where a.rank<='10')".format(table=table,case_when_sql=case_when_sql,start_time=self.last_week_start_date,end_time=self.last_week_end_date,channel_cid=self.channel_cid)
        return sql

    def channel_pid_vv_change(self,table):
        ###判断是否传过来了pid字符串,若无则查询top50vv,若有则查询给予pid的vv
        if not hasattr(self,'pid_str'):
            sql = "(select pid as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'channel_pid_vv_change_this' as module_name from {table} where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' group by pid order by sum(vv) desc limit 50)".format(
                table=table, start_time=self.last_week_start_date, end_time=self.last_week_end_date, bid_not_in=self.bid_not_in ,channel_cid=self.channel_cid)
        else:
            sql = "(select pid as col1,'null' as col2,'null' as col3,'null' as col4,'null' as col5,round(sum(vv)/10000,1) as num,'channel_pid_vv_change_before' as module_name from {table} where {bid_not_in} and cid in ({channel_cid}) and date>='{start_time}' and date<='{end_time}' and pid in ({pid_str}) group by pid)".format(
                table=table, start_time=self.last_2week_start_date, end_time=self.last_2week_end_date, bid_not_in=self.bid_not_in,pid_str=self.pid_str ,channel_cid=self.channel_cid)
        return sql

    def bid_sql(self):###构造bid sql
        sql = 'case bid '
        for bid in self.bid_dict.keys():
            sql += "when {bid} then '{bid_name}' ".format(bid=bid,bid_name=self.bid_dict[bid])
        sql += "else 'else' end"
        return sql

    def cid_sql(self):###构造bid sql
        sql = 'case cid '
        for cid in self.cid_dict.keys():
            sql += "when {cid} then '{cid_name}' ".format(cid=cid,cid_name=self.cid_dict[cid])
        sql += "else 'else' end"
        return sql

    def datetime_process(self):###返回查询中开始时间与结束时间段内的日期列表
        start_date = datetime.datetime.strptime(self.start_date, '%Y%m%d').date()  ###字符串转换为日期格式
        end_date = datetime.datetime.strptime(self.end_date, '%Y%m%d').date()
        date_list = list()
        curr_date = start_date + datetime.timedelta(1)
        date_list.append("%04d%02d%02d" % (start_date.year, start_date.month, start_date.day))
        while curr_date != end_date:
            date_list.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
            curr_date += datetime.timedelta(1)
        date_list.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
        return date_list





if __name__ == '__main__':
    # print newmofang(searchtype='vv_platform_month').sql_query()
    # print newmofang(searchtype='vv_platform_day',start_date='20170301',end_date='20170307').sql_query()
    # print newmofang(searchtype='vv_terminal_day', start_date='20170301', end_date='20170307').sql_query()
    pp = Newmofang(start_date='20170401',end_date='20170406')
    aa = pp.module_search(searchtype='platform_kpi')
    bb = pp.module_search(searchtype='platform_vv_month')
    print pp.sql_union(aa,bb)
    # qq = Newmofang(searchtype='platform_vv_month',channel_name='show',start_date='20170401',end_date='20170406').platform_vv_month()
    # sql_all = Newmofang().sql_union(pp,qq)
    # print newmofang('vv','20170102','20170302').sql_query()
    # print newmofang('uv','20170102','20170302').sql_query()