#!/usr/bin/python
#coding:utf-8 
  
import json 
import urllib2 
from urllib2 import URLError 
import sys,argparse
reload(sys)
sys.setdefaultencoding('utf8')
  
class zabbix_api: 
        def __init__(self): 
            self.url = 'http://192.168.0.100/zabbix/api_jsonrpc.php' #修改URL
            self.header = {"Content-Type":"application/json"}         
              
        def user_login(self): 
            data = json.dumps({ 
                               "jsonrpc": "2.0", 
                               "method": "user.login", 
                               "params": { 
                                          "user": "Admin", #修改用户名
                                          "password": "zabbix" #修改密码
                                          }, 
                               "id": 0
                               }) 
              
            request = urllib2.Request(self.url, data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
          
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "\033[041m 用户认证失败，请检查 !\033[0m", e.code 
            else: 
                response = json.loads(result.read()) 
                result.close() 
                #print response['result'] 
                self.authID = response['result'] 
                return self.authID 
              
        def host_item(self,hostName=''): 
            data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                              "output": "extend",
                              "filter":{"host":hostName} 
                              },
                    "auth": self.user_login(),
                    "id": 1
                    })
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
          
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                if hasattr(e, 'reason'): 
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason 
                elif hasattr(e, 'code'): 
                    print 'The server could not fulfill the request.'
                    print 'Error code: ', e.code 
            else: 
                response = json.loads(result.read()) 
                #print response
                result.close() 
                return response['result'][0]['hostid']

        def host_get(self,hostName=''):
            data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                              "output": "extend",
                              "filter":{"host":hostName}
                              },
                    "auth": self.user_login(),
                    "id": 1
                    })
            request = urllib2.Request(self.url,data)
            for key in self.header:
                request.add_header(key, self.header[key])


            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'The server could not fulfill the request.'
                    print 'Error code: ', e.code
            else:
                response = json.loads(result.read())
                #print response
                result.close()
                print "主机数量: \033[31m%s\033[0m"%(len(response['result']))
                for host in response['result']:      
                        status={"0":"OK","1":"Disabled"}
                        available={"0":"Unknown","1":"available","2":"Unavailable"}
                       #print host
                        if len(hostName)==0:
                                print "HostID:\033[32m%s\033[0m\t  Status:\033[32m%-8s\033[0m  Available:\033[31m%-12s\033[0m  HostName:%-30s VisbleName:%-40s"%(host['hostid'],status[host['status']],available[host['available']],host['host'],host['name'])
                        else:
                                print "HostID: \033[32m%s\033[0m\t Status:\033[32m%-8s\033[0m  Available:\033[31m%-12s\033[0m  HostName:%-30s VisbleName:%-40s"%(host['hostid'],status[host['status']],available[host['available']],host['host'],host['name'] )
                                return host['hostid']

 
        def hostgroup_get(self, hostgroupName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method":"hostgroup.get", 
                               "params":{ 
                                         "output": "extend", 
                                         "filter": { 
                                                    "name": hostgroupName 
                                                    } 
                                         }, 
                               "auth":self.user_login(), 
                               "id":1, 
                               }) 
              
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                   
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                #print result.read()
                response = json.loads(result.read()) 
                result.close() 
                #print response()
                for group in response['result']:
                        if  len(hostgroupName)==0:
                                print "groupid : %s \t hostgroup:  \033[31m%s\033[0m" %(group['groupid'],group['name'])
                        else:
                                print "hostgroup:  \033[31m%s\033[0m\tgroupid : %s" %(group['name'],group['groupid'])
                                self.hostgroupID = group['groupid'] 
                                return group['groupid'] 
         
        def trigger_get(self,triggerName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method":"trigger.get", 
                               "params":{
                                         "output": "extend",
                                         "filter": {
                                                    "description": triggerName
                                                   }
                                         }, 
                               "auth":self.user_login(), 
                               "id":1, 
                               }) 
              
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                   
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                #print result.read()
                response = json.loads(result.read()) 
                result.close() 
                #print response()
                for triggerid in response['result']:                  
                         if  len(triggerName)==0:
                                print  "triggerids:  \033[31m%s\033[0m \t description : \033[31m%s\033[32m\tpriority ：\033[31m%s\033[32m\texpression ： \033[31m%s\033[32"%(triggerid['triggerid'],triggerid['description'],triggerid['priority'],triggerid['expression'])
                         else:
                                print "triggerids:  \033[31m%s\033[0m \t description : \033[31m%s\033[32m\tpriority ：\033[31m%s\033[32m\texpression ： \033[31m%s\033[32"%(triggerid['triggerid'],triggerid['description'],triggerid['priority'],triggerid['expression'])
                                self.triggerID = triggerid['triggerid'] 
                                return triggerid['triggerid']  
 
        def trigger_create(self, triggerName, expressionD, priorityNum):
            if self.trigger_get(triggerName):
                print "\033[041m该触发器已经添加!\033[0m"
                sys.exit(1)

            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method":"trigger.create",
                               "params":{
                                         "description": triggerName,
                                         "expression": expressionD,
                                         "priority": priorityNum
                                         },
                               "auth": self.user_login(),
                               "id":1
                              })
            request = urllib2.Request(self.url, data)
            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                print "添加触发器 : \033[42m%s\031[0m \tid :\033[31m%s\033[0m" % (triggerName, response['result']['triggerids'])

        def web_get(self,webName=''):
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method":"httptest.get",
                               "params":{
                                         "output": "extend",
                                         "filter": {
                                                    "description": webName
                                                   }
                                         },
                               "auth":self.user_login(),
                               "id":1,
                               })

            request = urllib2.Request(self.url,data)
            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                #print result.read()
                response = json.loads(result.read())
                result.close()
                #print response()
                for httptestid in response['result']:
                         if  len(webName)==0:
                                print "httptestids:  \033[31m%s\033[0m\tname : %s\033[32m\tstatus ：%s\t\033[32mhostid : \
%s"%(httptestid['httptestid'],httptestid['name'],httptestid['status'],httptestid['hostid'])
                         else:
                                print "httptestids:  \033[31m%s\033[0m\tname : %s\033[32m\tstatus ：%s\t\033[32mhostid : \
%s"%(httptestid['httptestid'],httptestid['name'],httptestid['status'],httptestid['hostid'])
                                self.httptestID = httptestid['httptestid']
                                return httptestid['httptestid']


        def web_create(self, hostName, webName, url,status_codes,no):
            if self.web_get(webName):
                print "\033[041mWEB场景已经添加!\033[0m"
                sys.exit(1)
                  
            hostId=self.host_get(hostName)
            print "hostId : %s" % (hostId)
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method":"httptest.create",
                               "params":{
                                         "hostid": hostId,
                                         "name": webName,
                                         "steps": [
                                             {
                                                 "name": webName,
                                                 "url": url,
                                                 "status_codes": status_codes,
                                                 "no": no
                                                  }
                                         ]
                                         },
                               "auth": self.user_login(),
                               "id":1
                               })
            request = urllib2.Request(self.url, data)
            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                print "添加WEB场景 : \033[42m%s\031[0m \tid : \033[31m%s\033[0m" % (webName, response['result']['httptestids'])
 

        def template_get(self,templateName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method": "template.get", 
                               "params": { 
                                          "output": "extend", 
                                          "filter": { 
                                                     "name":templateName                                                        
                                                     } 
                                          }, 
                               "auth":self.user_login(), 
                               "id":1, 
                               })
              
            request = urllib2.Request(self.url, data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                   
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                response = json.loads(result.read()) 
                result.close() 
                #print response
                for template in response['result']:                
                    if len(templateName)==0:
                        print "template_id : %s \t template_name : \033[31m%s\033[0m\t" % (template['templateid'],template['name'])
                    else:
                        self.templateID = response['result'][0]['templateid'] 
                        print "Template Name :  \033[31m%s\033[0m "%templateName
                        return response['result'][0]['templateid']

        def hostgroup_create(self,hostgroupName):
            if self.hostgroup_get(hostgroupName):
                print "hostgroup  \033[42m%s\033[0m is exist !"%hostgroupName
                sys.exit(1)
            data = json.dumps({
                              "jsonrpc": "2.0",
                              "method": "hostgroup.create",
                              "params": {
                              "name": hostgroupName
                              },
                              "auth": self.user_login(),
                              "id": 1
                              })
            request=urllib2.Request(self.url,data)
 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                   
            try: 
                result = urllib2.urlopen(request)
            except URLError as e: 
                print "Error as ", e 
            else: 
                response = json.loads(result.read()) 
                result.close()
                print "\033[042m 添加主机组:%s\033[0m  hostgroupID : %s"%(hostgroupName,response['result']['groupids'])
        

        def template_create(self,templateName,groupName):
            if self.template_get(templateName):
                print "template  \033[42m%s\033[0m is exist !"%templateName
                sys.exit(1)
            groupID=self.hostgroup_get(groupName)
            data = json.dumps({
                              "jsonrpc": "2.0",
                              "method": "template.create",
                              "params": {
                                  "host": templateName,
                                  "groups": groupID
                              },
                              "auth": self.user_login(),
                              "id": 1
                              })
            request=urllib2.Request(self.url,data)

            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                print "\033[042m 添加模板:%s\033[0m  templateID : %s"%(templateName,response['result']['templateids'])

 
        def interface_get(self,hostName='',itype=''):
            hostID=self.host_get(hostName)
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method": "hostinterface.get",
                               "params": {
                                          "output": "extend",
                                          "hostids": hostID,
                                          "filter": {
                                                     "type":itype
                                                     }
                                          },
                               "auth":self.user_login(),
                               "id":1,
                               })

            request = urllib2.Request(self.url, data)
            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                #print response
                for interface in response['result']:
                    if len(hostName)==0:
                        print "interfaceid :  \033[31m%s\033[0m "%interface['interfaceid']
                    else:
                        self.interfaceID = response['result'][0]['interfaceid']
                        print "interfaceid :  \033[31m%s\033[0m "%self.interfaceID
                        return interface['interfaceid']


        def application_get(self,applicationName,hostName):
            hostID=self.host_item(hostName)
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method": "application.get",
                               "params": {
                                          "output": "extend",
                                          "hostids": hostID,
                                          "filter": {
                                                     "name":applicationName
                                                     }
                                          },
                               "auth":self.user_login(),
                               "id":1,
                               })

            request = urllib2.Request(self.url, data)
            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                #print response
                for applications in response['result']:
                    if len(hostName)==0:
                        print "Need hostName"
                    else:
                        print "applicationid:  \033[31m%s\033[0m "%applications['applicationid']
                        return response['result'][0]['applicationid']

        def item_get(self,itemName=''):
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method": "item.get",
                               "params": {
                                          "output": "extend",
                                          "filter": {
                                                     "name":itemName
                                                     }

                                          },
                               "auth":self.user_login(),
                               "id":1,
                               })

            request = urllib2.Request(self.url, data)
            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                #print response
                for item in response['result']:
                    if len(itemName)==0:
                        print "itemid: \033[31m%s\033[0m \t hostid : \033[31m%s\033[0m \t itemName : \033[31m%s\033[0m \t key : \033[31m%s\033[0m"\
%(item['itemid'],item['hostid'],item['name'],item['key_'])
                    else:
                        print "itemid:  \033[31m%s\033[0m \t itemName : \033[31m%s\033[0m\tkey : \033[31m%s\033[0m"\
%(item['itemid'],item['name'],item['key_'])
                        return item['itemid']

        def item_create(self,itemName, hostName, applicationName,key,type_,value_type,itype,delay):
            applicationID=self.application_get(applicationName,hostName)
            hostID=self.host_item(hostName)
            interfaceid=self.interface_get(hostName,itype)
            if self.item_get(itemName):
                print "item  \033[42m%s\033[0m is exist !"%itemName
                sys.exit(1)
            data = json.dumps({
                              "jsonrpc": "2.0",
                              "method": "item.create",
                              "params": {
                              "name": itemName,
                              "key_": key,
                              "hostid": hostID,
                              "type": type_,
                              "value_type": value_type,
                              "interfaceid": interfaceid,
                              "applications": applicationID,
                              "delay": delay
                              },
                              "auth": self.user_login(),
                              "id": 1
                              })
            request=urllib2.Request(self.url,data)

            for key in self.header:
                request.add_header(key, self.header[key])

            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "Error as ", e
            else:
                response = json.loads(result.read())
                result.close()
                print "\033[042m 添加监控项:%s\033[0m  itemID : %s"%(itemName,response['result']['itemids'])


                      
        def host_create(self, hostip, hostgroupName, templateName): 
            if self.host_get(hostip):
                print "\033[041m该主机已经添加!\033[0m"
                sys.exit(1)
 
            group_list=[]
            template_list=[]
            for i in hostgroupName.split(','):
                var = {}
                var['groupid'] = self.hostgroup_get(i)
                group_list.append(var)
            for i in templateName.split(','):
                var={}
                var['templateid']=self.template_get(i)
                template_list.append(var)
 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method":"host.create", 
                               "params":{ 
                                         "host": hostip, 
                                         "interfaces": [ 
                                         { 
                                         "type": 1, 
                                         "main": 1, 
                                         "useip": 1, 
                                         "ip": hostip, 
                                         "dns": "", 
                                         "port": "10050"
                                          } 
                                         ], 
                                       "groups": group_list,
                                       "templates": template_list,
                                         }, 
                               "auth": self.user_login(), 
                               "id":1                  
            }) 
            request = urllib2.Request(self.url, data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                   
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                response = json.loads(result.read()) 
                result.close() 
                print "添加主机 : \033[42m%s\031[0m \tid :\033[31m%s\033[0m" % (hostip, response['result']['hostids']) 
 
 
 
        def host_disable(self,hostip):
                data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": {
                "hostid": self.host_get(hostip),
                "status": 1
                },
                "auth": self.user_login(),
                "id": 1
                })
                request = urllib2.Request(self.url,data)
                for key in self.header:
                        request.add_header(key, self.header[key]) 
                try: 
                        result = urllib2.urlopen(request)
                except URLError as e: 
                        print "Error as ", e 
                else: 
                        response = json.loads(result.read()) 
                        result.close()
                        print '----主机现在状态------------'
                        print self.host_get(hostip)
                     
 
        def host_delete(self,hostid):
            hostid_list=[]
            #print type(hostid)
            for i in hostid.split(','):
                var = {}
                var['hostid'] = self.host_get(i)
                hostid_list.append(var)          
            data=json.dumps({
                                "jsonrpc": "2.0",
                                "method": "host.delete",
                                "params": hostid_list,
                    "auth": self.user_login(),
                    "id": 1
                    })
 
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
            try: 
                result = urllib2.urlopen(request) 
            except Exception,e: 
                print  e
            else: 
 
                result.close() 
                print "主机 \033[041m %s\033[0m  已经删除 !"%hostid 

        def file_parse(self,filename,option):
            if option=='item':
                with open(filename,"r") as f:
                    content = f.readlines()
                    for i in content:
                        l = i.split("    ")
                        itemName = l[0].rstrip()
                        hostName = l[1].rstrip()
                        applicationName = l[2].rstrip()
                        key = l[3].rstrip()
                        type_ = l[4].rstrip()
                        value_type = l[5].rstrip()
                        itype = l[6].rstrip()
                        delay = l[7].rstrip()
                        print "itemName: %s"%itemName
#                        try:
                        print self.item_create(itemName, hostName, applicationName,key,type_,value_type,itype,delay)
#                        except Exception as e:
#                            print str(e)

if __name__ == "__main__":
        zabbix=zabbix_api()
        parser=argparse.ArgumentParser(description='zabbix  api ',usage='%(prog)s [options]')
        parser.add_argument('-H','--host',nargs='?',dest='listhost',default='host',help='查询主机')
        parser.add_argument('-G','--group',nargs='?',dest='listgroup',default='group',help='查询主机组')
        parser.add_argument('-R','--trigger',nargs='?',dest='listtrigger',default='trigger',help='查询触发器')
        parser.add_argument('-r','--add-trigger',nargs=3,dest='addtrigger',metavar=("Web test failed","{192.168.0.135:vfs.file.cksum[/etc/passwd].diff(0)}>1","3"),help='增加触发器')
        parser.add_argument('-W','--web',nargs='?',dest='listweb',default='web',help='查询WEB场景')
        parser.add_argument('-w','--add-web',nargs=5,dest='addwebs',metavar=('192.168.0.135',"Web connect test","http://192.168.0.100/zabbix/zabbix.php?action=dashboard.view",200,1),help='增加WEB场景控项')
        parser.add_argument('-I','--items',nargs='?',dest='listitem',default='items',help='查询监控项')
        parser.add_argument('-i','--add-item',nargs=8,dest='additems',metavar=('filesystem free space','192.168.0.135','CPU','vfs.fs.size[/usr,free]','1','0','1','300'),help='增加监控项')
        parser.add_argument('-T','--template',nargs='?',dest='listtemp',default='template',help='查询模板信息')
        parser.add_argument('-t','--add-template',nargs=2,dest='addtemps',metavar=('mytest',"Linux Server"),help='增加模板')
        parser.add_argument('-A','--add-group',nargs=1,dest='addgroup',help='添加主机组')
        #parser.add_argument('-C','--add-host',dest='addhost',nargs=3,metavar=('192.168.2.1', 'test01,test02', 'Template01,Template02'),help='添加主机,多个主机组或模板使用分号')
        parser.add_argument('-C','--add-host',dest='addhost',nargs=3,metavar=('60.28.211.88',"All Linux Server,线上服","Template OS Linux,Template ICMP Ping"),help='添加主机,多个主机组或模板使用分号')
        parser.add_argument('-d','--disable',dest='disablehost',nargs=1,metavar=('192.168.2.1'),help='禁用主机')
        parser.add_argument('-D','--delete',dest='deletehost',nargs='+',metavar=('192.168.2.1'),help='删除主机,多个主机之间用分号')
        parser.add_argument('-f','--file',dest='filename',nargs=2,metavar=('items.text','item'),help='输入参数文件,选项类型')
        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv)==1:
                print parser.print_help()
        else:
                args=parser.parse_args()
 
                if args.listitem != 'items' :
                        if args.listitem:
                                zabbix.item_get(args.listitem)
                        else:
                                zabbix.item_get()
                if args.listhost != 'host' :
                        if args.listhost:
                                zabbix.host_get(args.listhost)
                        else:
                                zabbix.host_get()
                if args.listtrigger != 'trigger' :
                        if args.listtrigger:
                                zabbix.trigger_get(args.listtrigger)
                        else:
                                zabbix.trigger_get()				
                if args.listgroup !='group':
                        if args.listgroup:
                                zabbix.hostgroup_get(args.listgroup)
                        else:
                                zabbix.hostgroup_get()
                if args.listtemp != 'template':
                        if args.listtemp:
                                zabbix.template_get(args.listtemp)
                        else:
                                zabbix.template_get()

                if args.listweb != 'web':
                        if args.listweb:
                                zabbix.web_get(args.listweb)
                        else:
                                zabbix.web_get()
                if args.filename:
                        zabbix.file_parse(args.filename[0],args.filename[1])	
                if args.additems:
                        zabbix.item_create(args.additems[0],args.additems[1],args.additems[2],args.additems[3],args.additems[4],args.additems[5],args.additems[6],args.additems[7])	
                if args.addgroup:
                        zabbix.hostgroup_create(args.addgroup[0])	
                if args.addtemps:
                        zabbix.template_create(args.addtemps[0],args.addtemps[1])	
                if args.addwebs:
                        zabbix.web_create(args.addwebs[0],args.addwebs[1],args.addwebs[2],args.addwebs[3],args.addwebs[4])	
                if args.addtrigger:
                        zabbix.trigger_create(args.addtrigger[0],args.addtrigger[1],args.addtrigger[2])	
                if args.addhost:
                        zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2])
                if args.disablehost:
                        zabbix.host_disable(args.disablehost)
                if args.deletehost:
                        zabbix.host_delete(args.deletehost[0])

