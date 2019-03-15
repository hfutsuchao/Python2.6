#coding:utf-8
import pandas as pd
from commfunction import today,date_add

df = pd.read_csv('./cluedetail.csv')

td = today()
td = date_add(td,-2)
thisweek_start = date_add(td,-8)
thisweek_end = date_add(td,-2)
lastweek_start = date_add(thisweek_start,-7)
lastweek_end = date_add(thisweek_end,-7)
lastmonth_start = date_add(thisweek_start,-31)
lastmonth_end = date_add(thisweek_end,-31)

df_thisweek = df[(df['date']>=thisweek_start) & (df['date']<=thisweek_end)].groupby(['city']).count()
df_thisweek['date'] = thisweek_start + '~' + thisweek_end
df_lastweek = df[(df['date']>=lastweek_start) & (df['date']<=lastweek_end)].groupby(['city']).count()
df_lastweek['date'] = lastweek_start + '~' + lastweek_end
df_lastmonth = df[(df['date']>=lastmonth_start) & (df['date']<=lastmonth_end)].groupby(['city']).count()
df_lastmonth['date'] = lastmonth_start + '~' + lastmonth_end
df_thismonth = df[(df['date']>=lastmonth_start) & (df['date']<=lastmonth_end)].groupby(['city']).count()
df_thismonth['date'] = lastmonth_start + '~' + lastmonth_end

df_all = pd.concat([df_thisweek,df_lastweek,df_lastmonth],axis=0,join='inner')
print df_all
df_all.to_csv('./cityclue.csv')
