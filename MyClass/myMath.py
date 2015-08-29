import math

class MyMath():
    
    def __init__(self):
        pass
    
    def dicSUM(self,dic):
        for key in dic:
            if type(dic[key]) is dict:
                dic[key] = self.dicSUM(dic[key])
            elif type(dic[key]) is list:
                tmpDic,dic[key] = dic[key],0
                for value in tmpDic:
                    if type(value) not in [str,list,dict]:
                        dic[key] = dic[key] + value
                    else:
                        dic[key] = tmpDic
                        break
        return dic
    
    def dicAVG(self,dic):
        for key in dic:
            if type(dic[key]) is dict:
                dic[key] = self.dicAVG(dic[key])
            elif type(dic[key]) is list:
                tmpDic,length,dic[key] = dic[key],len(dic[key]),0
                for value in tmpDic:
                    if type(value) not in [str,list,dict]:
                        dic[key] = dic[key] + value
                    else:
                        dic[key] = tmpDic
                        break
                if (type(dic[key]) in [int,float]) and (length!=0):
                    dic[key] = dic[key]/float(length)
        return dic
    
    
    
if __name__ == '__main__':
    test = MyMath()
    print test.dicAVG({'a':{'b':['1',2,3,4,50]},'c':{'d':[1,2,3,4,50]}})