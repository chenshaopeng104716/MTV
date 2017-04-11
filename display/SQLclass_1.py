#coding:utf-8

import psycopg2
import MySQLdb
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class Newmofang(object):

    """新魔方相关数据查询"""

    def __init__(self,**kwargs):

        ###数据查询用表
        self.search_dict = {'kpi_platform':'vv_cid_day','vv_platform_day': 'vv_cid_day', 'uv_platform_day': 'bid_uv_day','pv_platform_day':'dau_bid_day',
                            'duration_platform_day':'pt_bid_day','vv_platform_month': 'vv_cid_day','vv_terminal_day':'vv_cid_day',
                            'uv_terminal_day':'bid_uv_day','vv_channel_day':'vv_cid_day','uv_channel_day':'cid_uv_day',
                            'dau_platform_day':'dau_bid_day','uv_pid_day_avg':'pid_uv_day','vv_pid_day_avg':'vv_pid_day'}
        ###查询对应模块所用类内部函数
        self.func_dict = {"kpi_platform":self.kpi_platform,"vv_platform_month": self.vv_platform_month,"vv_platform_day": self.vv_platform_day,"pv_platform_day":self.pv_platform_day,"uv_platform_day": self.uv_platform_day,
                          "duration_platform_day":self.duration_platform_day,"vv_terminal_day":self.vv_terminal_day,"uv_terminal_day":self.uv_terminal_day,"vv_channel_day":self.vv_channel_day,
                          "uv_channel_day":self.uv_channel_day,"dau_platform_day":self.dau_platform_day,"uv_pid_day_avg":self.uv_pid_day_avg,"vv_pid_day_avg":self.vv_pid_day_avg}
        ###魔方数据库中bid对应的终端
        self.bid_dict = {"1":"ott","102":"pcweb","104":"phonem","5":"padweb","6":"macclient","7":"win10client","8":"pcclient","9":"android","10":"apad","11":"ipad","12":"iphone","13":"mui"}
        ###媒资数据库中cid对应的频道
        self.cid_dict = {"1":"show","2":"tv","3":"movie","7":"cartoon","87":"show","83":"tv","84":"movie","88":"cartoon"}
        ###魔方数据库包含刷量频道,本项目不包含刷量数据,要去除,vv、uv中的刷量频道,现在为bid in (2,4)
        self.bid_not_in = 'bid not in (2,4)'
        ###魔方数据库dau中的刷量频道，现在为bid in (2,4,5)
        self.dau_bid_not_in = 'bid not in (2,4,5)'
        try:###初始化数据库连接
            self.conn = psycopg2.connect(database="dm_result", user="product_readonly", password="deDr7Toi29Sj&SkDS#LL",
                                    host="10.100.5.85", port="2345")
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError:
            print datetime.datetime.now().date()
            print ("新魔方数据库无法连接")
            self.conn = None
            self.cursor = None
        if "start_date" in kwargs:
            self.start_date = kwargs['start_date']
        if "end_date" in kwargs:
            self.end_date = kwargs['end_date']
        if "searchtype" in kwargs:
            self.searchtype = kwargs['searchtype']###查询模块
            self.table = self.search_dict[self.searchtype]  ###返回查询的数据对应的表
        if "pid_str" in kwargs:
            self.pid_str = kwargs['pid_str']

    ###媒资数据库获取合集名称
    def cms_sql(self):
        conn = MySQLdb.connect(host="10.100.5.41", user="app_hefang", passwd="app_hefang1234", db="cms",
                               charset="utf8")
        cursor = conn.cursor()
        sql = "select a.id,a.title,b.classcn from hunantv_v_collection a,hunantv_v_class b where a.rootid = b.id and a.id in (%s);" % self.pid_str
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    ###按照查询模块调取具体函数
    def func(self):
        return self.func_dict.get(self.searchtype)

    ###模块查询
    def sql_query(self):###具体查询，返回结果
        if self.conn != None:###判断数据库连接是否正常
            sql = self.func()()
            print sql
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()
            # print self.table
        else:
            result = None
        return result

    def kpi_platform(self):
        ###每个月对应的季度
        quarter = {1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:3,10:4,11:4,12:4}
        ###每个季度对应的开始日期
        quarter_start_date = {1:'20170101',2:'20170401',3:'20170701',4:'20171001'}
        ###现在季度
        quarter_now = quarter[datetime.datetime.now().month]
        calculate_start_time = quarter_start_date[quarter_now]
        calculate_end_time = self.end_date###查询结束时间
        sql = "select avg(a.vv) as vv from (select date,sum(vv) as vv from {table} where {bid_not_in} " \
              "and date>='{start_time}' and date<='{end_time}' GROUP BY date) a;".format(table=self.table,start_time=calculate_start_time,end_time=calculate_end_time,bid_not_in=self.bid_not_in)
        return sql


    def vv_platform_month(self):###全平台月vv汇总模块
        sql = "select substring(date from 1 for 6) as date,sum(vv) as vv from {table} where date>='20160101' and date<='{end_date}' and {bid_not_in} " \
              "GROUP BY substring(date from 1 for 6) order by substring(date from 1 for 6)".format(table=self.table,end_date=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def vv_platform_day(self):###全平台每日vv
        sql = "select date,sum(vv) as vv from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date".format(table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def uv_platform_day(self):###全平台每日uv
        sql = "select date,sum(uv) as uv from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date".format(table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def pv_platform_day(self):
        sql = "select date,sum(pv) as pv from {table} where {dau_bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date".format(table=self.table,start_time=self.start_date,end_time=self.end_date,dau_bid_not_in=self.dau_bid_not_in)
        return sql

    def duration_platform_day(self):
        sql = "select date,sum(pt) as pt from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date".format(table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def vv_terminal_day(self):###按频道查询vv
        case_when_sql = self.bid_sql()
        sql = "select date,{case_when_sql} as bid_name,sum(vv) as vv from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,bid order by date".format(case_when_sql=case_when_sql,table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def uv_terminal_day(self):
        case_when_sql = self.bid_sql()
        sql = "select date,{case_when_sql} as bid_name,sum(uv) as uv from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,bid order by date".format(case_when_sql=case_when_sql,table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def vv_channel_day(self):
        case_when_sql = self.cid_sql()
        sql = "select date,{case_when_sql} as cid_name,sum(vv) as vv from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,cid_name order by date".format(case_when_sql=case_when_sql,table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def uv_channel_day(self):
        case_when_sql = self.cid_sql()
        sql = "select date,{case_when_sql} as cid_name,sum(uv) as uv from {table} " \
              "where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date,cid_name order by date".format(case_when_sql=case_when_sql,table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def dau_platform_day(self):
        sql = "select date,sum(uv) as dau from {table} where {dau_bid_not_in} and date>='{start_time}' and date<='{end_time}' group by date order by date".format(table=self.table,start_time=self.start_date,end_time=self.end_date,dau_bid_not_in=self.dau_bid_not_in)
        return sql

    def vv_pid_day_avg(self):
        sql = "select pid,round(sum(vv)/7) as vv from {table} where {bid_not_in} and pid in ({pid_str}) and date>='{start_time}' and date<='{end_time}' group by pid order by round(sum(vv)/7) desc limit 20".format(table=self.table,pid_str=self.pid_str,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
        return sql

    def uv_pid_day_avg(self):
        sql = "select pid,round(sum(uv)/7) as uv from {table} where {bid_not_in} and date>='{start_time}' and date<='{end_time}' group by pid order by round(sum(uv)/7) desc limit 20".format(table=self.table,start_time=self.start_date,end_time=self.end_date,bid_not_in=self.bid_not_in)
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
    print Newmofang(searchtype='kpi_platform').sql_query()
    # print newmofang('vv','20170102','20170302').sql_query()
    # print newmofang('uv','20170102','20170302').sql_query()