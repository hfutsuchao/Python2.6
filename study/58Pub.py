#coding:utf-8
from html import Html

gjLogin = 'http://fangvip.ganji.com/auth.php?do=login'

gj = Html()
gj.get(gjLogin,'')
params = {
          'next':'',
            'no_cookie_test':'1',
            'password':'abc123',
            'username':'hfutsuchao@163.com'
          }
print gj.post(gjLogin,params,'')

Login58 = 'https://passport.58.com/dounionlogin'
gj.clear()
gj = Html()
gj.get(Login58,'')
params = {
          'cd':'8231',
'isweak':'0',
'mcresult':'186210094',
'p1':'3b5097066bf8c23328f2705cf7e22978',
'p2':'0935f368d58dc668582876b25a03c042',
'p3':'6171355f65ac657b8497d91ae0954c0a68bd7a711f169186fc6f2e0c43ba87d9a88fc591a90d541ffd04257ed6fb5629d6dc527097cae53d1ed3180baf456c57d87f6ad8548d54a6dffe12f1c0781a0007825cdc7e0c56a571af05da2ba6892c19ca0515221026063dbdba82891258c5c15443f342261fe6c25ee0bc9a0b422e',
'password':'password',
'path':'http://sy.58.com/?pts=1377088972251',
'ptk':'b4914e19797147beaef723f64d415fb2',
'timesign':'1377088999501',
'username':'huangqiaoyun5858'
          }

print gj.post(Login58,params,'')
print gj.post(Login58,params,'')
