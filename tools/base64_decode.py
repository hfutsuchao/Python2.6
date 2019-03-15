#coding:utf-8

import urllib
import sys

def base64_decode(codes):
	result = []
	for line in codes:
		result.append(urllib.unquote(line))
	return result

def main():
	try:
		codes = open(sys.argv[1],'r').readlines()
		decoded = base64_decode(codes)
	except:
		print 'Please input decode file'
	if len(sys.argv) == 3:
		r = open(sys.argv[2],'w')
		r.write(r.join('\n'))

if __name__ == '__main__':
	main()