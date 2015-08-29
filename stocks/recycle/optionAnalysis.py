from html import Html

header = {
          'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Cookie':"__utma=243156864.1660532569.1377423359.1380900067.1380937282.6; __utmz=243156864.1380900067.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=sogotrade%20%E6%89%8B%E6%9C%BA; PSSO=%09%c3%a5%c2%aa-%c3%b9%60%c2%8dQ%c3%96c%c2%adZ%c3%94%19%c2%b3%e2%80%9c%16%c3%a2%c3%b4%c2%a7%25%e2%80%9dg%e2%80%a1%c3%973%c3%a5H%e2%84%a2%c3%bfS%1bo%22%3e%c3%95%17B%c3%98K%13%c3%8b%c6%92O%e2%80%98%c5%beob%c3%bf%22y%3e%5c%1eu%0ck%5c%10%23%c3%95%5bq%e2%80%a6%e2%80%98%c3%81!%c2%a5%3fp67%02%0e%c3%83%c2%a1%e2%80%9a%c3%9cY5%c2%bd%c5%a1%c2%aa%e2%80%98_4%c3%8c%c3%be%c3%99%c2%b9%c3%a7%c3%ac%c3%89%60%40%c3%b9HbW%c3%afq%c3%b7%c2%a3k%0a%0c%c3%80%c3%bc%1eG%16%c3%86%e2%84%a2%184V%c2%a3.q%c5%a1%e2%84%a2%09%e2%80%98%e2%80%9c%c3%971%c3%b6%c2%ad%c2%bfum%03%c3%a15%c3%9dZ%05%c3%a5H%c2%ba%c2%aaW%c2%a1%c2%b5%c2%ab%c3%b9f%c3%94%c2%b9%c3%a8%c3%af%c3%93%c3%99%e2%80%9ey%c3%b7E%05%c2%bb%c3%9e%e2%80%9a%07%257W%c3%ad%c3%9da%c3%ab%c2%a6%c3%a0%19%7d%c3%bc1%c2%ae%23%c2%bb%c2%a4%c3%9b%c2%8fD%c3%be%5b%1aPu8W7%0f%c3%99%11%02%00O%c3%a4jq%c2%be%07%c3%a5%c2%b0%c3%b2%c3%9a%c2%aa%c3%8d%40%c3%96%c2%bf%c2%bd%c3%aa%c3%b2%e2%80%93%11%c2%8fUh%c2%a0k%c3%b4%10%3dC%1a%c2%ac%c3%97%5e%c3%a9Rb%02%00%c3%a1%c5%a0%c2%a8rSOg%c3%afH'%c2%aeU%c2%bc%c2%a2%c3%a1%16Fa%15%00%c3%80%c3%93%c2%a6; __utmc=243156864; BureauSwitcher=SOGO; ASP.NET_SessionId=xnr3eggz0qu5h0bb1u1as2ik; TradeBottomTabIndex=0; activeSettingPageIndex=0; activeSettingLinkIndex=7; ctl00_mc_ac_QuickQuotePane_QuickQuote1_stockChartGOOG=0; StockSelectAuthCookie=304528A8B083E3E772E22662F4C99DA8E72A0D67F3F75CF5000F6EA223D9CC0E9B76551EE7871F0FFBB1EF474DF00054668CF4A8CC2A8E288A65746E333D925BDC804CE2956D602A288D9D2A1CE618DDC8E3BD2C2360D17D2A72AB88B13714AB88D347F96D538E9FF678002B59DD87BCE4000D49E70AA928E07B0B0FB6A208A6ED9D81CF44D5313C053DBE3505F02EAAEE084428; UserCulture=zh-cn; CurrentCulture=en-us",
'Host':'options.sogotrade.com',
'Referer':'https://stp.sogotrade.com/Trade.aspx?',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:23.0) Gecko/20100101 Firefox/23.0'
          }

post = {
        'chainType':'2',
'expiration':'"131221R"',
'isRotated':'false',
'showBinary':'true',
'showNonStandard':'true',
'strike':'null',
'strikes':'null',
'strikesRange':'"1"',
'underlyingSymbol':'"BIDU"'
        }

urlHandle = Html()

url = 'http://options.sogotrade.com/Chain.aspx'

url = 'https://options.sogotrade.com/Trade.aspx'

print urlHandle.get(url,header)