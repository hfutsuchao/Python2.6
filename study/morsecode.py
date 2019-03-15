# -*- coding:utf-8 -*-
__author__  = 'kiven'
__date__    = '2014-06-04'
__version__ = '1.0.0'
# 摩斯密码表(自己可定义加密方式...)
CODE = {
        # 26个字母
        'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
 
        # 10个数字
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',
 
        # 16个标点符号
        ',': '--..--', '.': '.-.-.-', ':': '---...', ';': '-.-.-.',
        '?': '..--..', '=': '-...-',  "'": '.----.', '/': '-..-.',
        '!': '-.-.--', '-': '-....-', '_': '..--.-', '(': '-.--.',
        ')': '-.--.-', '$': '...-..-','&': '. . . .','@': '.--.-.'
 
        # 下面还可自行添加密码字典
 
}
# print CODE
# 反转字典(作为解密摩斯密码的字典)
UNCODE = dict(map(lambda t:(t[1],t[0]),CODE.items()))
# print UNCODE
 
'''
将字符串转换成摩斯密码
params:需要转换的字符串
'''
def stringToMorseAlphabet(msg):
    # message用于保存加密结果
    message = ''
    # msg = raw_input('Message:')
    # msg = 'this is test'
    print msg + '   ///对应的摩斯密码为///',
    for c in msg:
        if c == ' ':
            message += ' '
        else:
            # upper():将所有小写字母转换成大写字母
            message += CODE[c.upper()] + ' '
    return message
 
'''
将摩斯密码还原成字符串
params:需要还原的摩斯码
'''
def morseAlphabetToString(morseCode):
    # message用于保存解密结果
    message = ''
    list = morseCode.split(' ')
    # print list
    print morseCode + '   ///对应的明文为///',
    for s in list:
        if s == '':
            message += ' '
        else:
            message += UNCODE[s]
    return message
 
 
# Test
# print stringToMorseAlphabet('I love you')
#print morseAlphabetToString(stringToMorseAlphabet('what the fuck!'))

def main():
    msg = raw_input('MESSAGE: ')
    print stringToMorseAlphabet(msg)
if __name__ == "__main__":
    main()
