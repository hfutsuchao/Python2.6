# -*- coding: utf-8 -*-
from Tkinter import *
root = Tk()

lb1 = Label(root,text = 'shareName1',fg = 'red')
lb2 = Label(root,text = 'shareName1',fg = 'green')

lb1.grid(row = 0,column = 0)
lb2.grid(row = 1,column = 0)

#Button(root,text = 'forget last',command = forgetLabel).grid(row = 1)

root.mainloop()