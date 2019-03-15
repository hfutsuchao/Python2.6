#coding:utf-8
import pandas as pd

class QuantS(object):
    def __init__(self):
        pass
        #self.__code = code
        #self.__start_date = start_date  #date_this
        #self.__end_date = end_date
        #self.__norm_type = norm_type
        #self.__quota_index = quota_index
        #self.__lost = lost
        #self.__start_date_open = 0
        #self.__end_date_open = 0
        #self.__rate = {}
        #self.__df = pd.DataFrame()
        #self.__df = self.__get_df() # -> date,open,close,high,low,volume

    def trade_records_C(self,trade_types,rate,end_date,end_date_open):
        for strategy_name in trade_types['buy']:
            rate[strategy_name] = {}
            rate[strategy_name]['profit'] = {}
            rate[strategy_name]['profit']['total'] = 1.0
            rate[strategy_name]['trade'] = {}
            for i in range(len(trade_types['buy'][strategy_name])):
                buy_date = trade_types['buy'][strategy_name][i].keys()[0]
                try:
                    sell_date = trade_types['sell'][strategy_name][i].keys()[0]
                except:
                    sell_date = end_date
                try:
                    rate[strategy_name]['profit']['total'] = rate[strategy_name]['profit']['total'] * (trade_types['sell'][strategy_name][i].values()[0] * (1 - 0.002) / trade_types['buy'][strategy_name][i].values()[0])
                    rate[strategy_name]['profit'][buy_date] = rate[strategy_name]['profit']['total']
                    rate[strategy_name]['trade'][buy_date] = [buy_date, trade_types['buy'][strategy_name][i].values()[0], sell_date, trade_types['sell'][strategy_name][i].values()[0]]
                except Exception,e:
                    if len(trade_types['buy'][strategy_name]) == len(trade_types['sell'][strategy_name]):
                        rate[strategy_name]['profit']['total'] = rate[strategy_name]['profit']['total'] * (end_date_open * (1 - 0.002) / trade_types['sell'][strategy_name][i].values()[0])
                    else:
                        rate[strategy_name]['profit']['total'] = rate[strategy_name]['profit']['total'] * (end_date_open * (1 - 0.002) / trade_types['buy'][strategy_name][i].values()[0])
                    rate[strategy_name]['profit'][end_date] = rate[strategy_name]['profit']['total']
                    rate[strategy_name]['trade'][end_date] = [buy_date, trade_types['buy'][strategy_name][i].values()[0], 'lastday', end_date_open]
        return sorted(rate.items(),key=lambda x:x[1]['profit']['total'],reverse=True)

    def __trade_records_CP(self,trade_types,rate):
        pass

    def plot_profit(self,strategy_name='all'):
        pass
        for code in rate:
            best_strategy_code = rate[code][0][0]
            rate_dic = dict(rate[code])
            based_profit = pd.DataFrame(rate_dic['based']).drop('total',axis=0)
            if strategy_name:
                best_strategy_profit = pd.DataFrame(rate_dic[strategy_name]).fillna(method='pad').drop('total',axis=0)
                best_strategy_code = strategy_name
            else:
                if rate[code][0][0] == 'based':
                    best_strategy_profit = pd.DataFrame(rate_dic[rate[code][1][0]]).fillna(method='pad').drop('total',axis=0)
                else:
                    best_strategy_profit = pd.DataFrame(rate_dic[rate[code][0][0]]).fillna(method='pad').drop('total',axis=0)
            profit_all = pd.concat([based_profit['profit'], best_strategy_profit['profit']], axis=1).fillna(method='pad')
            profit_all.plot()
            plt.legend(('based_profit', 'best_strategy_profit'), loc='upper left')
            plt.title(code + '_' + best_strategy_code)
            plt.savefig('/Users/NealSu/Downloads/profit_pic/' + code + '_' + best_strategy_code + '.jpg')
            plt.close('all')
            try:
                print code
                print best_strategy_profit['trade']
            except:
                pass      

    def strategy_choose(self,rate):
        strategy_sum = {}
        best_strategy = {}
        for code in rate:
            rate_dic = dict(rate[code])
            best_strategy_code = rate[code][0][0]
            if best_strategy_code not in best_strategy:
                best_strategy[best_strategy_code] = 1
            else:
                best_strategy[best_strategy_code] = best_strategy[best_strategy_code] + 1
            for strategy_name in rate_dic:
                if strategy_name not in strategy_sum:
                    strategy_sum[strategy_name] = rate_dic[strategy_name]['profit']['total']
                else:
                    strategy_sum[strategy_name] = strategy_sum[strategy_name] + rate_dic[strategy_name]['profit']['total']
        best_strategy = sorted(best_strategy.items(),key=lambda x:x[1],reverse=True)
        strategy_sum = sorted(strategy_sum.items(),key=lambda x:x[1],reverse=True)
        return (best_strategy,strategy_sum)

    def strategy_profit(self,rate,strategy_name):
        #print rate
        #t = dict(rate['WB'])[strategy_name]['trade']
        p = dict(rate['WB'])[strategy_name]['profit']['total']
        print strategy_name,p
        
    def __getattr__(self):
        if attr == 'best_strategy':
            return self.strategy_choose()[1]

def main():
    from trade_point_corr_pm import GetTradePoint
    from stock_df import GetDf
    df = GetDf('JD',db_file='../stock_US_data.db').df.set_index('date')[['open','close','high','low','volume']]
    t = GetTradePoint(df,'2016-01-04','2017-06-15',norm_type='pm')
    trade_types = t.trade_point
    end_date_open = t.end_date_open
    rate = t.rate
    end_date = t.end_date
    s = QuantS()
    rs = {}
    rs['WB'] = s.trade_records_C(trade_types,rate,end_date,end_date_open)
    sn = s.strategy_choose(rs)[0][0][0]
    s.strategy_profit(rs,sn)

if __name__ == '__main__':
    main()