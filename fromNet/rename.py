#coding:utf-8
import os,sys;
def rename():
	path="/Users/NealSu/Downloads/soft/gktgd/寒蝉鸣泣之时合集/寒蝉鸣泣之时·礼/";
	filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
	for files in filelist:#遍历所有文件
		print files
		Olddir=os.path.join(path,files);#原来的文件路径
		print Olddir
		if os.path.isdir(Olddir):#如果是文件夹则跳过
			continue;
		filename=os.path.splitext(files)[0];#文件名
		filetype=os.path.splitext(files)[1];#文件扩展名
		if filetype == '.ass':
			filename = filename.replace(".SC]","")
		elif filetype == '.mp4':
			filename = filename.replace("[YYDM-11FANS][Higurashi no Naku Koro ni Rei]","")
		Newdir=os.path.join(path,filename+filetype);#新的文件路径
		print Newdir
		os.rename(Olddir,Newdir);#重命名
rename();