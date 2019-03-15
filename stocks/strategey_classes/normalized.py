#coding:utf-8
import pandas as pd
import numpy as np

class GetNormalized(object):
    def __init__(self,df,norm_type='max'):
        self.__df = df
        self.__norm_type = norm_type

    def get_normlized(self,norm_type=''):
        normalized = {}
        if not norm_type:
            norm_type=self.__norm_type
        if norm_type == 'max' or norm_type == 'norm':
            df_norm = self.__df.copy()
            for column in df_norm.columns:
                df_norm[column] = df_norm[column] / abs(df_norm[column]).max()
            normalized['max'] = df_norm.copy()
        if norm_type == 'pm' or norm_type == 'norm':
            df_norm = self.__df.copy()
            for column in df_norm.columns:
                df_norm[column].ix[df_norm[column] < 0] = -1
                df_norm[column].ix[df_norm[column] > 0] = 1
            normalized['pm'] = df_norm.copy()
        return normalized

    def __getattr__(self,attr):
        if attr == 'max':
            return self.get_normlized(attr)['max']
        elif attr == 'pm':
            return self.get_normlized(attr)['pm']
        else:
            return self.get_normlized(attr)

def main():
    from stock_df import GetDf
    df = GetDf('WB',db_file='../stock_US_data.db').df.set_index('date')[['open','close','high','low','volume']]
    t = GetNormalized(df)
    print t.pm

if __name__ == '__main__':
    main()