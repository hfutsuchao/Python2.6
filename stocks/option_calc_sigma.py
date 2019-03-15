#coding:utf-8
import numpy as np
from scipy.stats import norm
import datetime,commfunction

# 设定参数
r = 0.03975 # risk-free interest rate
expire_day = 'Jul 21, 2017' # time to expire
t = float(commfunction.date_today_delta(expire_day,format='%b %d, %Y'))/365  # time to expire (30 days)
q = 0 # dividend yield
S0 = 40.59 # underlying price
X = 39 # strike price
mktprice_call = 2.56 # market price
#mktprice_put = 5.7 # market price

# 用二分法求implied volatility，暂只针对call option
sigma = 0.65487 # initial volatility

def call_implied_sigma(S0,X,r,t,sigma,mktprice,q=0):
    C = 0
    upper = 1
    lower = 0
    while abs(C-mktprice)>1e-4:
        d1 = (np.log(S0/X)+(r-q+sigma**2/2)*t)/(sigma*np.sqrt(t))
        d2 = d1-sigma*np.sqrt(t)
        C = S0*np.exp(-q*t)*norm.cdf(d1)-X*np.exp(-r*t)*norm.cdf(d2)
        if C-mktprice>0: 
            upper = sigma
            sigma = (sigma+lower)/2
        else:
            lower = sigma
            sigma = (sigma+upper)/2
    return sigma

def put_implied_sigma(S0,X,r,t,sigma,mktprice,q=0):
    P = 0
    upper = 1
    lower = 0
    while abs(P-mktprice)>1e-3:
        d1 = (np.log(S0/X)+(r-q+sigma**2/2)*t)/(sigma*np.sqrt(t))
        d2 = d1-sigma*np.sqrt(t)
        P = X*np.exp(-r*t)*(1-norm.cdf(d2))-S0*np.exp(-q*t)*(1-norm.cdf(d1))
        if P-mktprice>0: 
            upper = sigma
            sigma = (sigma+lower)/2
        else:
            lower = sigma
            sigma = (sigma+upper)/2
    return sigma
print call_implied_sigma(S0,X,r,t,sigma,mktprice_call,q) # implied volatility
#print put_implied_sigma(S0,X,r,t,sigma,mktprice_put,q) # implied volatility