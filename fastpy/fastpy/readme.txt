高性能python http服务器+web框架

源代码只有400多行

另有开源pb rpc框架： http://www.oschina.net/p/python-fastrpc

性能比较如下

tornado 4kqps 多进程1wqps 
nginx+tornado 9kqps
nginx+uwsgi 8kqps （注意：没说比nginx快，只是这几个web框架不行） 

django和webpy 性能不是一个级别的

本server 3.2w qps 
没用任何python加速

不相信的可以自己压测下哦
已经真实使用到自己的多个项目之中，效果明显
有需要优化的地方或者建议欢迎联系 qq 512284622


fastpy 是高性能 Python HTTP 服务器。

用户文档：

1、启动：
   指定监听端口即可启动
   python fastpy.py 8992

2、快速编写cgi,支持运行时修改,无需重启server

   在fastpy.py同一目录下
   随便建一个python 文件
   例如:
   example.py:
   #-*- coding:utf-8 -*-
   import sys
   #定义一个同名example类
   #定义一个tt函数：
   reload(sys)
   sys.setdefaultencoding('utf8')
   FastpyAutoUpdate=True
   class example():
       def tt(self, request, response_head):
           #print request.form
           #print request.getdic
           #fileitem = request.filedic["upload_file"]
           #fileitem.filename
           #fileitem.file.read()
           return "ccb"+request.path

   则访问该函数的url为 http://ip:port/example.tt
   修改后保存，即可访问，无需重启
   FastpyAutoUpdate 属性可控制需不需要热部署
   FastpyAutoUpdate=true 支持热部署，修改无需重启
   FastpyAutoUpdate=false 则不支持热部署，修改需要重启
   tt函数必须带两个参数
   request：表示请求的数据 默认带以下属性
      headers: 头部 （字典）
      form:  post参数，包括form表单 （字典）
      getdic: url参数 （字典）
      filedic: form表单中文件 （字典）
      rfile: 原始http content内容  （字符串）
      action: python文件名 (这里为example)
      method: 函数方法    （这里为tt）
      command:  （get or post）
      path: url （字符串）
      http_version: http版本号 （http 1.1）
   response_head: 表示response内容的头部
      例如如果要返回用gzip压缩
      则增加头部
      response_head["Content-Encoding"] = "gzip"
      
    除了直接return作为response内容外
    fastpy还支持 request.ret(res) 的方式返回内容，以支持异步调用
    例如：
    def readfile(request, response_head):
        content = open("a.txt").read()
        request.ret(content)
    class example():
        def tt(self, request, response_head):
            #do some thind prepare
            thread.start_new_thread(readfile,(request,response_head))
    新起一个线程去读文件，然后原来的处理线程就可以继续去处理别的请求了，
    等到文件读完调用request.ret(res)返回给客户端

3、下载文件
   默认静态文件(包括html，js、css、图片、文件等)放在static文件夹下
   html和js、css会自动压缩加速
   例如把a.jpg放到static文件夹下
   访问的url为 http://ip:port/static/a.jpg
   支持etag 客户端缓存功能
   (server 使用sendfile进行文件发送，不占内存且快速)

4、支持网页模板编写
   创建一个模板 template.html
   <HTML>
       <HEAD><TITLE>$title</TITLE></HEAD>
       <BODY>
           $contents
       </BODY>
   </HTML>

   则对应的函数：
   def template(request,response_head):
       t = Template(file="template.html")
       t.title  = "my title"
       t.contents  = "my contents"
       return str(t)
   模板实现使用了python最快速Cheetah开源模板,
   性能约为webpy django thinkphp等模板的10倍以上:
   http://my.oschina.net/whp/blog/112296

5、支持http/https透明代理
   python proxy.py 8995
   启动后再浏览器配置代理即可使用，可以弥补nginx 不支持https代理的不足

6、设计模式：
     每个线程一个实例：
         fastpy是多进程内再多线程的模式，每个线程一个example 类对象.

     每个进程一个实例：
         如果想让某个对象或变量一个进程只定义一个，
         可以使用单例模式：

class example(Singleton):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(example,cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            # do something when create 
        return cls._instance


     所有进程一个实例:
         因为fastpy是多进程的，如果想让所有进程所有线程也只使用一个对象
         可以直接使用python的多进程接口
         mgr = multiprocessing.Manager()
         ip_dic = mgr.dict()
         这样每个进程的每个线程里都共用这个ip_dic变量