function urlencode(str){
        var ret="";
        var strSpecial="!"#$%&'()*+,/:;<=>?[]^`{|}~%";
        for(var i=0;i<str.length;i++){
                var chr = str.charAt(i);
                var c=str2asc(chr);
                tt += chr+":"+c+"n";
                if(parseInt("0x"+c) > 0x7f){
                        ret+="%"+c.slice(0,2)+"%"+c.slice(-2);
                }else{
                        if(chr==" ")
                                ret+="+";
                        else if(strSpecial.indexOf(chr)!=-1)
                                ret+="%"+c.toString(16);
                        else
                                ret+=chr;
                }
        }
        return ret;
}
