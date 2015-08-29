from html import Html

class GJLG(Html):
    params = {"UserName":"suchao","Domain":"@ganji.com","Password":"hFuT814155356134"}
    url = "http://sso.ganji.com/Account/LogOn"
    def sso(self):
        crm = Html()
        crm.post(self.url,self.params,"")
        return crm

'''crm = GJLG()
print crm.sso()'''