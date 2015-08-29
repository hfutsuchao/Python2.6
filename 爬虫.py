import urllib2
import sgmllib

class Entry:
    author=''
    content=''
    pic=''
    up = 0
    down = 0
    tag = ''
    comment = 0
    def to_string(self):
        return '[Entry: author=%s content=%s pic=%s tag=%s up=%d down=%d comment=%d]'\
            %(self.author,self.content,self.pic,self.tag,self.up,self.down,self.comment)

class MyHTMLParser(sgmllib.SGMLParser):
    #所有用到的声明
    #note all the datas
    datas = []
    # all the entries
    entries = []
    #the entry now
    entry = Entry()
    #last Unclosed tag
    div_tag_unclosed = ''
    
    def start_div(self,attrs):
        for name,value in attrs:
            if name =='class' and value == 'content':
                self.div_tag_unclosed = 'content'
            elif name=='class' and value == 'tags' :
                self.div_tag_unclosed = 'tags'
            elif name=='class' and value=='up':
                self.div_tag_unclosed = 'up'
            elif name=='class' and value == 'down':
                self.div_tag_unclosed = 'down'
            elif name=='class' and value=='comment':
                self.div_tag_unclosed = 'comment'
            elif name=='class' and value=='author':
                self.div_tag_unclosed = 'author'
                self.entry = Entry()
            elif name=='class' and value=='thumb':
                self.div_tag_unclosed = 'thumb'
                
    def end_div(self):
        if self.div_tag_unclosed == 'content' :
            self.div_tag_unclosed =''
            self.entry.content =  self.datas.pop().strip()
    def start_a(self,attrs):pass
    def start_img(self,attrs):
        if self.div_tag_unclosed == 'thumb':
            for name,value in attrs:
                if name=='src':
                    self.div_tag_unclosed =''
                    self.entry.img = value.strip() 
    def end_img(self):pass
    def end_a(self):
        if self.div_tag_unclosed == 'author':
            self.div_tag_unclosed =''
            self.entry.author = self.datas.pop().strip()
        if self.div_tag_unclosed == 'tags':
            self.div_tag_unclosed =''
            self.entry.tag = self.datas.pop().strip()
        elif self.div_tag_unclosed == 'up':
            self.div_tag_unclosed =''
            self.entry.up = int(self.datas.pop().strip())
        elif self.div_tag_unclosed == 'down':
            self.div_tag_unclosed =''
            self.entry.down = int(self.datas.pop().strip())
        elif self.div_tag_unclosed == 'comment':
            self.div_tag_unclosed =''
            self.entry.comment = int(self.datas.pop().strip())
            self.entries.append(self.entry)
    def handle_data(self, data):
#        print 'data',data
        self.datas.append(data)

#request the url
response = urllib2.urlopen('http://www.qiushibaike.com/8hr')
all = response.read()

#parse HTML
parser = MyHTMLParser()
parser.feed(all)
#print all the entries
for entry in parser.entries:
    print entry.to_string()
