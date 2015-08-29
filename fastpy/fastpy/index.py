#-*- coding:utf-8 -*-
#import os
#import imp
#import sys
#import time
#import json
#import logging
#import traceback
#import urllib
#from common import base
#from common import net
#from Cheetah.Template import Template
#import string
#import pymongo
#import time
#import datetime
#import thread
#import multiprocessing
#
#svr_host = "192.168.1.13"
#svr_port = 10003
#mongo_host = "192.168.1.15"
#mongo_port = 8996
#
#reload(sys)
#sys.setdefaultencoding('utf8')
#
#curlog = base.FeimatLog("logs/index.log")
#
#login_timeout = 20*60 #s
#clear_del = 2*60 #s
#mgr = multiprocessing.Manager()
#ip_dic = mgr.dict()
#
#stop_clean = False
#def clear_fun(ip_dic_):
#    global stop_clean
#    while False == stop_clean:
#        time.sleep(clear_del)
#        curtime = time.time()
#        curlog.log("cur login:%s\n"%json.dumps(ip_dic_.items()))
#        keylist = ip_dic_.keys();
#        for key in keylist:
#            if ip_dic_[key] < curtime:
#                del ip_dic_[key]
#thread.start_new_thread(clear_fun, (ip_dic,))
#
#def check_login(ip_dic_, request):
#    ip = request.client_ip
#    if ip in ip_dic_:
#        ip_dic_[ip] = time.time() + login_timeout
#        return True
#    else:
#        curlog.log("%s not login\n"%ip)
#        return False
#
#class index():
#    def __init__(self):
#        try:
#            # redis
#            #self.redis_cli = redis.StrictRedis(host=redis_host, port=redis_port)
#
#            # mongo
#            self.mongo_con = pymongo.Connection(mongo_host, mongo_port)
#            self.mongo_db = self.mongo_con.static
#
#            # httpClient
#            self.httpClient = net.KeepAliveCon(svr_host, svr_port)
#
#            # template
#            self.up_t = Template(file="templates/upload.html")
#            self.index_template = Template(file="templates/index.html")
#            self.login_template = Template(file="templates/login.html")
#            self.save_action_template = Template(file="templates/SelectAction.html")
#            self.save_diamond_template = Template(file="templates/SaveDiamond.html")
#            self.save_all_template = Template(file="templates/SaveAll.html")
#            self.select_area_template = Template(file="templates/SelectArea.html")
#            self.tips_t = Template(file="templates/tips.html")
#
#            # chart
#            self.chart_t = Template(file="templates/chart.html")
#            self.uu_t = Template(file="templates/chart_uu.html")
#            self.online_t = Template(file="templates/chart_online.html")
#            self.chart_eq_t = Template(file="templates/chart_eq.html")
#
#            # gm
#            self.gm_main_t = Template(file="templates/gm_main.html")
#            self.gm_sys_t = Template(file="templates/gm_sys.html")
#        except Exception, e:
#            print str(e)+base.getTraceStackMsg()
#
#    def gm_sys(self, request, response_head):
#        try:
#            response_head["Content-Encoding"] = "gzip"
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            if request.command == "get":
#                res = self.httpClient.GetAllArea();
#                response_json = ""
#                if res != "":
#                    response_json = json.loads(res)
#                self.gm_sys_t.arealist = response_json.get("response","")
#                return str(self.gm_sys_t)
#            elif request.command == "post":
#                area_id = request.form.get("area", "")
#                if not area_id.isdigit():
#                    self.tips_t.tips = "请选择正确区号"
#                    return str(self.tips_t)
#                sys_msg = request.form.get("sys_msg", "")
#                data_dic = {}
#                data_dic["sys_msg"] = sys_msg
#                data_dic["area_id"] = int(area_id)
#                res = self.httpClient.PostResponse("/publish_sys_msg", json.dumps(data_dic))
#                if "suc" == res:
#                    self.tips_t.tips = "发布成功"
#                else:
#                    self.tips_t.tips = "发布失败,联系管理员解决"
#                return str(self.tips_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#    def gm_main(self, request, response_head):
#        try:
#            response_head["Content-Encoding"] = "gzip"
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            return str(self.gm_main_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#    def acc_reg_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 101
#            data["title"] = "每天账户注册人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_reg_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 102
#            data["title"] = "每天创建角色人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_del_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 103
#            data["title"] = "每天删除角色人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_login_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 104
#            data["title"] = "每天登录人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_logout_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 105
#            data["title"] = "每天退出人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_login_reward_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 106
#            data["title"] = "每天领取登录奖励人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_ep_on_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 201
#            data["title"] = "每天穿戴装备人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_ep_putdown_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 202
#            data["title"] = "每天脱下装备人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_selltosys_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 203
#            data["title"] = "每天出售物品人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_ep_upgrade_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 204
#            data["title"] = "每天装备升级人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_eq_recast_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 205
#            data["title"] = "每天装备重铸人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_eq_enchant_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 206
#            data["title"] = "每天装备附魔人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_openbox_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 207
#            data["title"] = "每天打开宝箱人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_enchant_compose_json_day(self, request, response_head):
#        try:
#            data = {}
#            op = 208
#            data["title"] = "每天附魔合成人数曲线图";
#            data["sub_title"] = "以小时为单位";
#            data["y_title"] = "人数";
#            cond = {}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            self.get_people_num_perhour(data, op, cond)
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def get_people_num_perhour(self, data, op, cond):
#        col = eval("self.mongo_db.col_%s"%op)
#        now_time = datetime.datetime.now()
#        start_time = now_time + datetime.timedelta(hours=1)
#        start_time = time.strftime('%Y-%m-%d %H')
#        end_time = now_time - datetime.timedelta(hours=72)
#        end_time = end_time.strftime('%Y-%m-%d %H')
#        cond["logtime"] = {"$gte":end_time, "$lte":start_time}
#        cond["operate"] = op
#        data_list = col.find(cond)
#        all_area_dic = {}
#        x_set = {}
#        for row in data_list:
#            area_id = row.get("area_id")
#            area_name = row.get("area_name")
#            logtime = row.get("logtime")
#            logtime = logtime[5:13]
#            #num = row.get("num")
#            num = 1
#            area_dic = all_area_dic.get(area_name,{})
#            if logtime not in area_dic:
#                area_dic[logtime] = num
#            else:
#                area_dic[logtime] = area_dic[logtime] + num
#            all_area_dic[area_name] = area_dic
#            x_set[logtime] = None
#        x_arr = x_set.keys()
#        x_arr.sort()
#        data["x"] = x_arr
#        y_arr = []
#        for sub_area in all_area_dic.keys():
#            sub_y_data = {}
#            sub_y_data["name"] = sub_area
#            area_dic = all_area_dic[sub_area]
#            time_arr = []
#            for time_str in x_arr:
#                time_arr.append(area_dic.get(time_str,0))
#            sub_y_data["data"] = time_arr
#            y_arr.append(sub_y_data)
#        data["y"] = y_arr
#        return data
#
#    def char_online_json_day(self, request, response_head):
#        try:
#            data = {}
#            col = self.mongo_db.online_relate
#            start_time = time.strftime('%Y-%m-%d %H:%M')
#            end_time = datetime.datetime.now() - datetime.timedelta(hours=24)
#            end_time = end_time.strftime('%Y-%m-%d %H:%M')
#            cond = {"insert_time":{"$gte":end_time, "$lte":start_time},
#                    "opcode":"online_char"}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            data_list = col.find(cond)
#            all_area_dic = {}
#            x_set = {}
#            for row in data_list:
#                area_id = row.get("area_id")
#                area_name = row.get("area_name")
#                insert_time = row.get("insert_time")
#                Min = insert_time[14:16]
#                insert_time = insert_time[5:14]
#                if Min == "":
#                    Min = "00"
#                else:
#                    Min = int(Min)
#                    Min = Min/5*5
#                    Min = str(Min)
#                    if len(Min) == 1:
#                        Min = "0" + Min
#                insert_time = insert_time + Min
#                insert_time = insert_time.replace("-",".")
#                num = row.get("num")
#                area_dic = all_area_dic.get(area_name,{})
#                if insert_time not in area_dic:
#                    area_dic[insert_time] = num
#                else:
#                    area_dic[insert_time] = max(area_dic[insert_time], num)
#                all_area_dic[area_name] = area_dic
#                x_set[insert_time] = None
#            x_arr = x_set.keys()
#            x_arr.sort()
#            data["x"] = x_arr
#            y_arr = []
#            for sub_area in all_area_dic.keys():
#                sub_y_data = {}
#                sub_y_data["name"] = sub_area
#                area_dic = all_area_dic[sub_area]
#                time_arr = []
#                for time_str in x_arr:
#                    time_arr.append(area_dic.get(time_str,None))
#                sub_y_data["data"] = time_arr
#                y_arr.append(sub_y_data)
#            data["y"] = y_arr
#            data["title"] = "每天在线人数曲线图";
#            data["sub_title"] = "以分钟为单位";
#            data["y_title"] = "在线人数";
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def char_online_json_month(self, request, response_head):
#        try:
#            data = {}
#            col = self.mongo_db.online_relate
#            start_time = time.strftime('%Y-%m-%d %H:%M')
#            end_time = datetime.datetime.now() - datetime.timedelta(days=30)
#            end_time = end_time.strftime('%Y-%m-%d %H:%M')
#            cond = {"insert_time":{"$gte":end_time, "$lte":start_time},
#                    "opcode":"online_char"}
#            a_id = request.getdic.get("a_id", "")
#            if a_id != "":
#                a_id = a_id.strip("_")
#                id_list = a_id.split("_")
#                id_list = [int(x) for x in id_list]
#                indic = {}
#                indic["$in"] = id_list
#                cond["area_id"] = indic
#            data_list = col.find(cond)
#            all_area_dic = {}
#            x_set = {}
#            for row in data_list:
#                area_id = row.get("area_id")
#                area_name = row.get("area_name")
#                insert_time = row.get("insert_time")
#                insert_time = insert_time[5:10]
#                insert_time = insert_time.replace("-",".")
#                num = row.get("num")
#                area_dic = all_area_dic.get(area_name,{})
#                if insert_time not in area_dic:
#                    area_dic[insert_time] = num
#                else:
#                    area_dic[insert_time] = max(area_dic[insert_time], num)
#                all_area_dic[area_name] = area_dic
#                x_set[insert_time] = None
#            x_arr = x_set.keys()
#            x_arr.sort()
#            data["x"] = x_arr
#            y_arr = []
#            for sub_area in all_area_dic.keys():
#                sub_y_data = {}
#                sub_y_data["name"] = sub_area
#                area_dic = all_area_dic[sub_area]
#                time_arr = []
#                for time_str in x_arr:
#                    time_arr.append(area_dic.get(time_str,None))
#                sub_y_data["data"] = time_arr
#                y_arr.append(sub_y_data)
#            data["y"] = y_arr
#            data["title"] = "每月在线人数曲线图";
#            data["sub_title"] = "以天为单位";
#            data["y_title"] = "在线人数";
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def chart_online(self, request, response_head):
#        try:
#            global ip_dic
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            res = self.httpClient.GetAllArea();
#            response_json = ""
#            if res != "":
#                response_json = json.loads(res)
#            self.online_t.arealist = response_json.get("response","")
#            response_head["Content-Encoding"] = "gzip"
#            return str(self.online_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#    def chart_eq(self, request, response_head):
#        try:
#            global ip_dic
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            response_head["Content-Encoding"] = "gzip"
#            return str(self.chart_eq_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#    def account_uu_json(self, request, response_head):
#        try:
#            response_head["Content-Encoding"] = "gzip"
#            time_list = []
#            res = self.httpClient.GetResponse("/chart_uu")
#            if res != "":
#                res_json = json.loads(res)
#                time_list = res_json.get("response","")
#            num_dic = {}
#            for create_time in time_list:
#                f_val = string.atof(create_time)
#                f_val = f_val/1000
#                x = time.localtime(f_val)
#                s = time.strftime("%m.%d", x)
#                if s in num_dic:
#                    num_dic[s] += 1
#                else:
#                    num_dic[s] = 1
#
#            x_arr = []
#            y_arr = []
#            x_arr = num_dic.keys()
#            x_arr.sort()
#            for k in x_arr:
#                y_arr.append(num_dic[k])
#
#            data = {}
#            y_data = []
#            sub_y_data = {}
#            sub_y_data["name"] = "每天创建人数" #x title
#            sub_y_data["data"] = y_arr
#            y_data.append(sub_y_data)
#
#            data["x"] = x_arr
#            data["y"] = y_data
#            data["title"] = "每月账号创建人数曲线图"
#            data["sub_title"] = ""
#            data["y_title"] = "创建人数"
#            return json.dumps(data)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return ""
#
#    def character_uu_json(self, request, response_head):
#        response_head["Content-Encoding"] = "gzip"
#        data_dic = {}
#        a_id = request.getdic.get("a_id", "")
#        if a_id != "":
#            a_id = a_id.strip("_")
#            id_list = a_id.split("_")
#            id_dic = ""
#            for x in id_list:
#                if x == "":
#                    continue
#                id_dic += "(" + x + ")"
#            data_dic["area_cond"] = id_dic
#        else:
#            data_dic["area_cond"] = ""
#        res = self.httpClient.PostResponse("/character_uu", json.dumps(data_dic))
#        return res
#
#    def chart_uu(self, request, response_head):
#        try:
#            global ip_dic
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            res = self.httpClient.GetAllArea();
#            response_json = ""
#            if res != "":
#                response_json = json.loads(res)
#            self.uu_t.arealist = response_json.get("response","")
#            response_head["Content-Encoding"] = "gzip"
#            return str(self.uu_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#    def chart(self, request, response_head):
#        try:
#            global ip_dic
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            response_head["Content-Encoding"] = "gzip"
#            return str(self.chart_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#
#    def html(self, request, response_head):
#        if request.command == "get":
#            try:
#                response_head["Content-Encoding"] = "gzip"
#                #return str(self.save_action_template)
#                return str(self.login_template)
#            except Exception, e:
#                curlog.log(str(e)+base.getTraceStackMsg())
#                return "{\"error\":\"resource not found\"}"
#        elif request.command == "post":
#            #return json.dumps(ip_dic)
#            try:
#                username = request.form.get("TxtUserName", "")
#                password = request.form.get("TxtPassword", "")
#                if username == "coolplay" and password == "123":
#                    ip = request.client_ip
#                    cleartime = time.time() + login_timeout
#                    global ip_dic
#                    ip_dic[ip] = cleartime
#                    #return json.dumps(ip_dic)
#                    return self.login(request, response_head)
#                else:
#                    return "妈蛋，你要攻击我？"
#            except Exception, e:
#                curlog.log(str(e)+base.getTraceStackMsg())
#                return "{\"error\":\"resource not found\"}"
#
#    def SaveAll(self, request, response_head):
#        try:
#            response_head["Content-Encoding"] = "gzip"
#            global ip_dic
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            if request.command == "get":
#                return self.login(request, response_head)
#            elif request.command == "post":
#                area = request.form.get("area", "")
#                usrname = request.form.get("usrname", "")
#                type = request.form.get("type", "")
#                num = request.form.get("num", "")
#                itemid = request.form.get("itemid", "")
#                insid = request.form.get("insid", "")
#                insmark = request.form.get("insmark", "")
#                inslevel = request.form.get("inslevel", "")
#                taskid = request.form.get("taskid", "")
#
#                if type == "" or not type.isdigit():
#                    self.tips_t.tips = "妈蛋，别攻击我"
#                    return str(self.tips_t)
#                type = int(type)
#
#                dic = {}
#                command = ""
#                if type == 1 or type == 2 or type == 3 or type == 5: #diamond gold exp stamina
#                    if area == "" or not area.isdigit() or usrname == "" or num == "" or not num.isdigit():
#                        self.tips_t.tips = "妈蛋，别攻击我"
#                        return str(self.tips_t)
#                    dic["area_id"] = int(area)
#                    dic["character_name"] = usrname
#                    dic["character_id"] = 0
#                    dic["gm_code"] = type
#                    dic["gm_value"] = int(num)
#                    dic["gm_value_ext_1"] = 0
#                    dic["gm_value_ext_2"] = 0
#                    dic["gm_value_ext_3"] = 0
#                elif type == 4: #item
#                    if area == "" or not area.isdigit() or \
#                            usrname == "" or num == "" or \
#                            not num.isdigit() or \
#                            itemid == "" or not itemid.isdigit():
#                        self.tips_t.tips = "妈蛋，别攻击我"
#                        return str(self.tips_t)
#                    dic["area_id"] = int(area)
#                    dic["character_name"] = usrname
#                    dic["character_id"] = 0
#                    dic["gm_code"] = type
#                    dic["gm_value"] = int(num)
#                    dic["gm_value_ext_1"] = int(itemid)
#                    dic["gm_value_ext_2"] = 0
#                    dic["gm_value_ext_3"] = 0
#                elif type == 6: #PassedScene
#                    if area == "" or not area.isdigit() or usrname == "" or \
#                            not insid.isdigit() or not insmark.isdigit() or \
#                            not inslevel.isdigit():
#                        self.tips_t.tips = "妈蛋，别攻击我"
#                        return str(self.tips_t)
#                    dic["area_id"] = int(area)
#                    dic["character_name"] = usrname
#                    dic["character_id"] = 0
#                    dic["gm_code"] = type
#                    dic["gm_value"] = 0
#                    dic["gm_value_ext_1"] = int(insid)
#                    dic["gm_value_ext_2"] = int(insmark)
#                    dic["gm_value_ext_3"] = int(inslevel)
#                elif type == 7: #passtask
#                    if area == "" or not area.isdigit() or taskid == "" or \
#                            not taskid.isdigit() or usrname == "":
#                        self.tips_t.tips = "妈蛋，别攻击我"
#                        return str(self.tips_t)
#                    dic["area_id"] = int(area)
#                    dic["character_name"] = usrname
#                    dic["task_id"] = int(taskid)
#                    if int(taskid) == 0:
#                        command = "/clear_task"
#                    else:
#                        command = "/modify_task"
#                else:
#                    self.tips_t.tips = "妈蛋，别攻击我"
#                    return str(self.tips_t)
#
#                json_str = json.dumps(dic)
#                if type >= 1 and type <= 6:
#                    res = self.httpClient.SaveProfile(json_str)
#                elif type == 7:
#                    res = self.httpClient.PostResponse(command, json_str)
#                if "kSync" in res:
#                    self.tips_t.tips = "添加成功"
#                else:
#                    self.tips_t.tips = "错误码:"+res
#                return str(self.tips_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
#    def report(self, request, response_head):
#        if request.command == "get":
#            try:
#                response_head["Content-Encoding"] = "gzip"
#                return str(self.index_template)
#            except Exception, e:
#                curlog.log(str(e)+base.getTraceStackMsg())
#                return "{\"error\":\"resource not found\"}"
#        elif request.command == "post":
#            return "妈蛋，你要攻击我？"
#
#    def login(self, request, response_head):
#        if request.command == "get" or request.command == "post":
#            try:
#                response_head["Content-Encoding"] = "gzip"
#                global ip_dic
#                if not check_login(ip_dic, request):
#                    return str(self.login_template)
#                res = self.httpClient.GetAllArea();
#                response_json = ""
#                if res != "":
#                    response_json = json.loads(res)
#                self.save_all_template.arealist = response_json.get("response","")
#
#                res = self.httpClient.GetAllItems();
#                response_json = ""
#                if res != "":
#                    response_json = json.loads(res)
#                self.save_all_template.itemlist = response_json.get("response","")
#
#                res = self.httpClient.GetAllScen();
#                response_json = ""
#                if res != "":
#                    response_json = json.loads(res)
#                self.save_all_template.scenlist = response_json.get("response","")
#
#                res = self.httpClient.GetAllPlayer();
#                response_json = ""
#                if res != "":
#                    response_json = json.loads(res)
#                self.save_all_template.playerlist = response_json.get("response","")
#
#                res = self.httpClient.GetResponse("/get_task")
#                response_json = ""
#                if res != "":
#                    response_json = json.loads(res)
#                self.save_all_template.tasklist = response_json.get("response","")
#
#                return str(self.save_all_template)
#            except Exception, e:
#                curlog.log(str(e)+base.getTraceStackMsg())
#                return str(e)+base.getTraceStackMsg()
#
#    def upload(self, request, response_head):
#        try:
#            response_head["Content-Encoding"] = "gzip"
#            global ip_dic
#            if not check_login(ip_dic, request):
#                return str(self.login_template)
#            if request.command == "get":
#                return str(self.up_t)
#            elif request.command == "post":
#                if "upload_file" not in request.filedic:
#                    self.tips_t.tips = "别攻击我"
#                    return str(self.tips_t)
#                fileitem = request.filedic["upload_file"]
#                if fileitem.filename == "":
#                    self.tips_t.tips = "请选择文件后再上传"
#                    return str(self.tips_t)
#                fd = open("./static/%s" % fileitem.filename, "w")
#                while True:
#                    content = fileitem.file.read(65536)
#                    if not content:
#                        break
#                    fd.write(content)
#                fd.close()
#                url = "/static/%s" % fileitem.filename
#                self.tips_t.tips = "上传成功,下载地址为<br/><a href='%s'>%s</a><br/>" % (url,url)
#                return str(self.tips_t)
#        except Exception, e:
#            curlog.log(str(e)+base.getTraceStackMsg())
#            return str(e)+base.getTraceStackMsg()
#
