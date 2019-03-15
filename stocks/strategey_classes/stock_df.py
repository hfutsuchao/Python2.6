#coding:utf-8
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class GetDf(object):
    def __init__(self,code,db_file='../stock_CN_data.db'):
        self.__code = code
        self.__db_file = db_file
        DB_CONNECT_STRING = 'sqlite:///' + self.__db_file
        self.engine = create_engine(DB_CONNECT_STRING,echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

    def __get_df(self):
        df = pd.read_sql('select * from day_k_data where code="' + self.__code + '" order by date asc;',self.engine)
        self.session.close()
        return df

    def __get_greeks(self):
        df = pd.read_sql('select * from option_greeks where `16Root`="' + self.__code + '";',self.engine)
        self.session.close()
        return df[(df['17Strike']==40.0) & (df['18Puts']=='Jul 21, 2017')][['date','15IV','24IV']].set_index('date')

    def __getattr__(self,attr):
        if attr == 'df':
            return self.__get_df()
        if attr == 'greeks':
            return self.__get_greeks()
def main():
    t = GetDf('MOMO',db_file='../stock_option_data.db')
    df = t.greeks
    #print df[(df['17Strike']==40.0) & (df['18Puts']=='Jul 21, 2017')][['date','15IV','24IV']].set_index('date')
    print df
    
if __name__ == '__main__':
    main()